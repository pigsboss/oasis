#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""OASIS 共享文献库 · OpenAlex 工具（仅标准库，无第三方依赖）。

子命令：
  search   检索文献，打印候选摘要
  get      按 DOI / OpenAlex ID 取回单条记录：可保存元数据、下载 OA PDF、打印 BibTeX
  bib      由已保存的元数据生成 BibTeX（单文件 / --all / --out）

示例：
  python3 scripts/openalex.py search "optical interferometry review" --limit 10 --oa-only
  python3 scripts/openalex.py get doi:10.1051/0004-6361/201526405 --key duvert2017oifits --save --pdf
  python3 scripts/openalex.py bib --all --out bib/oasis.bib

目录约定（相对本脚本）：../meta/<key>.json、../pdf/<key>.pdf、../bib/oasis.bib
礼貌池：设置环境变量 OPENALEX_MAILTO=you@example.com 或使用 --mailto。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

API = "https://api.openalex.org"
LIB = Path(__file__).resolve().parent.parent
META = LIB / "meta"
PDF = LIB / "pdf"
STOPWORDS = {"the", "a", "an", "of", "on", "in", "for", "and", "with", "to", "at", "by", "from", "into"}
UA = "oasis-reference-library/0.1"


def _get(url: str, timeout: int = 30):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


def _api(path: str, params: dict | None = None):
    mailto = os.environ.get("OPENALEX_MAILTO")
    params = dict(params or {})
    if mailto:
        params.setdefault("mailto", mailto)
    url = f"{API}{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    return _get(url)


def _normalize_ident(ident: str) -> str:
    s = ident.strip()
    for pre in ("https://doi.org/", "http://doi.org/", "doi:"):
        if s.startswith(pre):
            s = s[len(pre):]
            break
    if s.startswith("https://openalex.org/"):
        return s.rsplit("/", 1)[-1]
    if s.startswith("10."):
        return "doi:" + s
    return s


def make_key(work: dict) -> str:
    fam = ""
    auths = work.get("authorships") or []
    if auths:
        author = auths[0].get("author") or {}
        fam = author.get("family_name") or ""
        if not fam:
            name = author.get("display_name") or ""
            fam = name.split()[-1] if name else ""
    fam = unicodedata.normalize("NFKD", fam.lower())
    fam = re.sub(r"[^a-z0-9]", "", fam)
    year = str(work.get("publication_year") or "")
    slug = ""
    for tok in re.findall(r"[A-Za-z0-9]+", (work.get("title") or "").lower()):
        if tok not in STOPWORDS and len(tok) >= 3:
            slug = tok
            break
    key = f"{fam}{year}{slug}"
    if not key:
        key = (work.get("id") or "unknown").rsplit("/", 1)[-1].lower()
    return key


def bibtex(work: dict, key: str | None = None) -> str:
    key = key or make_key(work)
    authors = " and ".join(
        a["author"]["display_name"] for a in work.get("authorships") or [] if a.get("author")
    )
    journal = ((work.get("primary_location") or {}).get("source") or {}).get("display_name") or ""
    b = work.get("biblio") or {}
    pages = ""
    if b.get("first_page"):
        pages = str(b["first_page"])
        if b.get("last_page"):
            pages += "-" + str(b["last_page"])
    doi = (work.get("doi") or "").replace("https://doi.org/", "")
    rec = {
        "title": (work.get("title") or "").replace("\n", " "),
        "author": authors,
        "journal": journal,
        "year": work.get("publication_year"),
        "volume": b.get("volume"),
        "number": b.get("issue"),
        "pages": pages,
        "doi": doi,
        "url": work.get("doi") or work.get("id"),
    }
    lines = [f"@article{{{key},"]
    for name, val in rec.items():
        if val in (None, ""):
            continue
        lines.append(f"  {name:8s} = {{{val}}},")
    lines.append("}")
    return "\n".join(lines)


def _download(url: str, dest: Path) -> None:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    dest.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(req, timeout=120) as r, open(dest, "wb") as f:
        while True:
            chunk = r.read(65536)
            if not chunk:
                break
            f.write(chunk)


def _is_pdf(path: Path) -> bool:
    try:
        with open(path, "rb") as f:
            return f.read(4) == b"%PDF"
    except OSError:
        return False


def _pdf_candidates(work: dict) -> list[str]:
    """候选 PDF 下载地址：优先 arXiv，其次 best OA，再次其余 locations。"""
    arxiv: list[str] = []
    other: list[str] = []
    best = (work.get("best_oa_location") or {}).get("pdf_url")
    if best:
        (arxiv if "arxiv.org" in best else other).append(best)
    for loc in work.get("locations") or []:
        pu = loc.get("pdf_url")
        lp = loc.get("landing_page_url") or ""
        if pu:
            (arxiv if "arxiv.org" in pu else other).append(pu)
        if "arxiv.org/abs/" in lp:
            aid = lp.split("arxiv.org/abs/", 1)[1]
            if aid and not aid.endswith(".pdf"):
                arxiv.append(f"https://arxiv.org/pdf/{aid}")
    out: list[str] = []
    seen: set[str] = set()
    for u in arxiv + other:
        if u not in seen:
            seen.add(u)
            out.append(u)
    return out


def _download_first(urls: list[str], dest: Path) -> Path | None:
    tmp = dest.parent / (dest.name + ".part")
    for url in urls:
        try:
            _download(url, tmp)
        except Exception as e:  # noqa: BLE001
            print(f"warning  : 下载失败 {url}（{e}）", file=sys.stderr)
            tmp.unlink(missing_ok=True)
            continue
        if _is_pdf(tmp):
            tmp.replace(dest)
            return dest
        print(f"warning  : 内容不是 PDF，跳过 {url}", file=sys.stderr)
        tmp.unlink(missing_ok=True)
    return None


def cmd_search(args) -> None:
    params = {
        "search": args.query,
        "per-page": str(max(1, min(args.limit, 50))),
        "select": "id,doi,title,publication_year,authorships,primary_location,open_access,cited_by_count",
    }
    if args.oa_only:
        params["filter"] = "is_oa:true"
    res = _api("/works", params)
    if args.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return
    print(f"共 {res['meta']['count']} 条结果，显示前 {len(res['results'])} 条：")
    for i, w in enumerate(res["results"], 1):
        oa = "OA" if (w.get("open_access") or {}).get("is_oa") else "--"
        doi = (w.get("doi") or "").replace("https://doi.org/", "")
        venue = ((w.get("primary_location") or {}).get("source") or {}).get("display_name") or ""
        first = ""
        if w.get("authorships"):
            first = (w["authorships"][0].get("author") or {}).get("display_name", "")
        wid = (w.get("id") or "").rsplit("/", 1)[-1]
        print(f"[{i:2d}] {w.get('publication_year')}  {oa:2s}  {w.get('title')}")
        print(f"      {first} · {venue} · doi:{doi} · 被引 {w.get('cited_by_count')} · {wid}")


def cmd_get(args) -> None:
    ident = _normalize_ident(args.ident)
    work = _api(f"/works/{urllib.parse.quote(ident, safe=':./')}")
    key = args.key or make_key(work)
    oa = work.get("open_access") or {}
    best = work.get("best_oa_location") or {}
    print(f"key      : {key}")
    print(f"title    : {work.get('title')}")
    print(f"year     : {work.get('publication_year')}")
    print(f"doi      : {(work.get('doi') or '').replace('https://doi.org/', '')}")
    print(f"OA       : {oa.get('is_oa')}  status={oa.get('oa_status')}  license={best.get('license') or '-'}")
    if best.get("pdf_url"):
        print(f"OA PDF   : {best['pdf_url']}")
    if args.save:
        META.mkdir(parents=True, exist_ok=True)
        p = META / f"{key}.json"
        p.write_text(json.dumps(work, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"saved    : {p.relative_to(LIB)}")
    if args.pdf:
        dest = PDF / f"{key}.pdf"
        if dest.exists() and _is_pdf(dest) and not args.force:
            print(f"pdf      : {dest.relative_to(LIB)}（已存在，跳过；--force 可重下）")
        else:
            if dest.exists() and not _is_pdf(dest):
                dest.unlink()
                print(f"清理     : 移除无效 PDF {dest.relative_to(LIB)}")
            saved = _download_first(_pdf_candidates(work), dest)
            if saved:
                print(f"pdf      : {saved.relative_to(LIB)}")
            else:
                print("pdf      : 未获得有效 PDF（候选均失败；仅保留元数据）")
    print()
    print(bibtex(work, key))


def cmd_bib(args) -> None:
    files: list[Path] = []
    if args.all:
        files = sorted(META.glob("*.json"))
    else:
        for f in args.files:
            p = Path(f)
            if not p.is_absolute() and not p.exists():
                cand = META / (f if f.endswith(".json") else f + ".json")
                if cand.exists():
                    p = cand
            files.append(p)
    if not files:
        print("没有可用的元数据文件（meta/*.json）。", file=sys.stderr)
        sys.exit(1)
    entries = []
    for f in files:
        work = json.loads(Path(f).read_text(encoding="utf-8"))
        entries.append(bibtex(work, Path(f).stem))
    out = "\n\n".join(entries) + "\n"
    if args.out:
        dest = Path(args.out)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(out, encoding="utf-8")
        print(f"wrote {len(entries)} entries -> {dest}")
    else:
        print(out)


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(
        description="OASIS 共享文献库 OpenAlex 工具", formatter_class=argparse.RawDescriptionHelpFormatter
    )
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("search", help="检索文献")
    s.add_argument("query")
    s.add_argument("--limit", type=int, default=10)
    s.add_argument("--oa-only", action="store_true", help="仅开放获取")
    s.add_argument("--json", action="store_true", help="输出原始 JSON")
    s.add_argument("--mailto", default=None)
    s.set_defaults(func=cmd_search)

    g = sub.add_parser("get", help="取回单条记录（DOI / OpenAlex ID）")
    g.add_argument("ident", help="doi:10.xxx / 10.xxx / W123456 / https://doi.org/...")
    g.add_argument("--key", default=None, help="指定文献 key（默认自动生成）")
    g.add_argument("--save", action="store_true", help="保存完整元数据到 meta/<key>.json")
    g.add_argument("--pdf", action="store_true", help="下载开放获取 PDF 到 pdf/<key>.pdf（优先 arXiv 回退）")
    g.add_argument("--force", action="store_true", help="强制重下 PDF（覆盖已有文件）")
    g.add_argument("--mailto", default=None)
    g.set_defaults(func=cmd_get)

    b = sub.add_parser("bib", help="生成 BibTeX")
    b.add_argument("files", nargs="*", help="meta/*.json 路径或 key")
    b.add_argument("--all", action="store_true", help="处理 meta/ 下全部条目")
    b.add_argument("--out", default=None, help="写入文件（默认打印）")
    b.set_defaults(func=cmd_bib)

    args = ap.parse_args(argv)
    mailto = getattr(args, "mailto", None)
    if mailto:
        os.environ["OPENALEX_MAILTO"] = mailto
    try:
        args.func(args)
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}: {e.url}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"网络错误: {e.reason}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
