"""CLI commands for the inventory lifecycle (M1).

Commands: inventory validate | propose <file> | review list|approve|reject | migrate-config
All runtime output is English (CODING_STANDARDS §2.2).
"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml
from oasis_catalog.config import ConfigError, load_config, resolve_config_path

from . import inventory as inv_mod
from . import migrate as migrate_mod
from . import reviewlog
from .sync import load_storages


def paths(args) -> tuple[Path, Path, Path]:
    cfg_path = resolve_config_path(args.config)
    return cfg_path, cfg_path.parent / "inventory.yaml", cfg_path.parent / reviewlog.LOG_NAME


def registered_storage_ids(cfg_path: Path, cfg) -> set[str]:
    ids = set(load_storages(cfg_path))
    # bootstrap default when the storages section is absent (matches live homelab)
    if not ids:
        ids = {"macbook_ssd", "raid5_archive", "zfs_nas"}
    return ids


def load_all(args):
    cfg_path, inv_path, log_path = paths(args)
    try:
        cfg = load_config(cfg_path)
    except ConfigError as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(2)
    inv = inv_mod.load_inventory(inv_path)
    return cfg_path, inv_path, log_path, cfg, inv


def cmd_inventory(args) -> int:
    cfg_path, inv_path, log_path, cfg, inv = load_all(args)
    if args.inventory_command != "validate":
        print("usage: inventory validate", file=sys.stderr)
        return 2
    storage_ids = registered_storage_ids(cfg_path, cfg)
    errors, warnings = inv_mod.validate_inventory(inv, storage_ids)
    log_count, log_errors = reviewlog.validate_log(log_path)
    print(f"inventory: {inv_path}")
    print(f"  datasets: {len(inv.datasets)}  proposals: {len(inv.proposals)}  storages: {len(storage_ids)}")
    print(f"  review-log: {log_count} entries, {len(log_errors)} error(s)")
    for warning in warnings:
        print(f"  WARN  {warning}")
    for error in errors + log_errors:
        print(f"  ERROR {error}")
    if errors or log_errors:
        return 2
    print("validate: OK" + (f" ({len(warnings)} warning(s))" if warnings else ""))
    return 0


def cmd_propose(args) -> int:
    cfg_path, inv_path, log_path, cfg, inv = load_all(args)
    source = Path(args.file).expanduser()
    if not source.exists():
        print(f"error: file not found: {source}", file=sys.stderr)
        return 2
    entry = yaml.safe_load(source.read_text(encoding="utf-8")) or {}
    storage_ids = registered_storage_ids(cfg_path, cfg)
    errors, warnings = inv_mod.validate_entry(entry, "proposal", storage_ids, f"proposal '{entry.get('id')}'")
    if not entry.get("reason"):
        errors.append("proposal: reason required")
    existing_ids = {e.get("id") for e in inv.datasets} | {p.get("id") for p in inv.proposals}
    if entry.get("id") in existing_ids:
        errors.append(f"proposal id '{entry.get('id')}' already exists (V-06)")
    for warning in warnings:
        print(f"WARN  {warning}")
    if errors:
        for error in errors:
            print(f"ERROR {error}", file=sys.stderr)
        return 2
    inv_mod.propose(inv, entry)
    inv_mod.save_inventory(inv)
    reviewlog.append_log(log_path, "propose", f"dataset:{entry.get('id')}",
                         note=str(entry.get("reason", ""))[:200])
    print(f"proposed: {entry.get('id')} -> {inv_path}")
    return 0


def cmd_review(args) -> int:
    cfg_path, inv_path, log_path, cfg, inv = load_all(args)
    if args.review_command == "list":
        print(f"proposals ({len(inv.proposals)}):")
        for item in inv.proposals:
            print(f"  - {item.get('id'):28s} {item.get('reason', '')[:80]}")
        print("recent review-log (last 5):")
        for entry in reviewlog.read_log(log_path, tail=5):
            print(f"  {entry.get('ts', '?')}  {entry.get('action', '?'):10s} {entry.get('target', '?')}")
        return 0

    action = args.review_command
    entry_id = args.id
    note = args.note or ""
    try:
        if action == "approve":
            inv_mod.approve(inv, entry_id)
        elif action == "reject":
            item = inv_mod.reject(inv, entry_id)
            note = note or str(item.get("reason", ""))[:200]
        else:
            print(f"unknown review action '{action}'", file=sys.stderr)
            return 2
    except KeyError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    inv_mod.save_inventory(inv)
    reviewlog.append_log(log_path, action, f"dataset:{entry_id}", note=note)
    print(f"review {action}: {entry_id}")
    return 0


def cmd_migrate_config(args) -> int:
    cfg_path, inv_path, log_path = paths(args)
    try:
        cfg = load_config(cfg_path)
    except ConfigError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    if not cfg.datasets:
        print("nothing to migrate (legacy config.datasets is empty)")
        return 1
    if inv_path.exists() and not args.force:
        print(f"inventory already exists: {inv_path} (use --force to overwrite)")
        return 1
    payload, logs = migrate_mod.build_inventory(cfg, registered_storage_ids(cfg_path, cfg))
    # validate the generated inventory before writing
    inv = inv_mod.Inventory(path=inv_path, version=payload["inventory_version"],
                            datasets=payload["datasets"], proposals=payload["proposals"])
    storage_ids = registered_storage_ids(cfg_path, cfg)
    errors, warnings = inv_mod.validate_inventory(inv, storage_ids)
    text = inv_mod.dump_inventory(inv)
    if args.dry_run:
        print("---- inventory.yaml (preview) ----")
        print(text)
        print("---- review-log entries (preview) ----")
        for entry in logs:
            print(f"  {entry['action']:10s} {entry['target']}  ({entry['note']})")
        for warning in warnings:
            print(f"WARN  {warning}")
        for error in errors:
            print(f"ERROR {error}")
        return 2 if errors else 0
    if errors:
        for error in errors:
            print(f"ERROR {error}", file=sys.stderr)
        return 2
    inv_mod.save_inventory(inv)
    for entry in logs:
        reviewlog.append_log(log_path, entry["action"], entry["target"], note=entry["note"])
    print(f"migrated {len(inv.datasets)} datasets -> {inv_path}")
    print(f"review-log: {log_path} ({len(logs)} entries appended)")
    for warning in warnings:
        print(f"WARN  {warning}")
    return 0


def register(sub, common) -> dict:
    """Attach inventory-lifecycle commands to the CLI; returns handlers."""
    p_inv = sub.add_parser("inventory", parents=[common], help="inventory registry operations")
    inv_sub = p_inv.add_subparsers(dest="inventory_command", required=True)
    inv_sub.add_parser("validate", parents=[common], help="validate inventory + review-log")

    p_prop = sub.add_parser("propose", parents=[common], help="submit an out-of-inventory dataset proposal")
    p_prop.add_argument("file", help="proposal YAML file (single entry with 'reason')")

    p_rev = sub.add_parser("review", parents=[common], help="single-owner review workflow")
    rev_sub = p_rev.add_subparsers(dest="review_command", required=True)
    rev_sub.add_parser("list", parents=[common], help="list proposals + recent log")
    p_appr = rev_sub.add_parser("approve", parents=[common], help="approve a proposal")
    p_appr.add_argument("id")
    p_appr.add_argument("--note", default="")
    p_rej = rev_sub.add_parser("reject", parents=[common], help="reject a proposal")
    p_rej.add_argument("id")
    p_rej.add_argument("--note", default="")

    p_mig = sub.add_parser("migrate-config", parents=[common],
                           help="migrate legacy config.datasets -> inventory.yaml")
    p_mig.add_argument("--dry-run", action="store_true", help="preview only")
    p_mig.add_argument("--force", action="store_true", help="overwrite an existing inventory")

    return {
        "inventory": cmd_inventory,
        "propose": cmd_propose,
        "review": cmd_review,
        "migrate-config": cmd_migrate_config,
    }
