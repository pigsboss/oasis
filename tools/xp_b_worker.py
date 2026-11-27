#!/usr/bin/env python3
"""Calibrate XP continuous files to 343-point pixel sums for B tier."""
from __future__ import annotations
import argparse, gzip, os, shutil, sys, tempfile, time
from pathlib import Path
import numpy as np
import h5py
from gaiaxpy import calibrate

MAP_IDS = MAP_IPIX = A_IDS = None
OUT_DIR = None


def process(path, outdir):
    path = Path(path)
    out = Path(outdir) / (path.name.replace('.csv.gz', '.npz'))
    if out.exists():
        return path.name, -1, -1
    t0 = time.time()
    tmp = None
    if str(path).endswith('.gz'):
        fd, name = tempfile.mkstemp(suffix='.csv', prefix='xp_b_', dir='/tmp')
        os.close(fd); tmp = Path(name)
        with gzip.open(path, 'rb') as f, open(tmp, 'wb') as o:
            shutil.copyfileobj(f, o, 1024 * 1024)
        inp = str(tmp)
    else:
        inp = str(path)
    try:
        df, wl = calibrate(inp, save_file=False, truncation=True)
    finally:
        if tmp is not None:
            try: tmp.unlink()
            except OSError: pass
    sids = np.asarray(df['source_id'], dtype=np.int64)
    flux = np.stack(df['flux'].to_numpy()).astype(np.float32)
    pos = np.searchsorted(MAP_IDS, sids)
    ok = (pos < MAP_IDS.size)
    pos2 = pos[ok]; sel = np.flatnonzero(ok)
    ok2 = MAP_IDS[pos2] == sids[sel]
    sel = sel[ok2]; pos2 = pos2[ok2]
    ap = np.searchsorted(A_IDS, sids[sel])
    is_a = (ap < A_IDS.size) & (A_IDS[np.minimum(ap, A_IDS.size - 1)] == sids[sel])
    sel = sel[~is_a]; pos2 = pos2[~is_a]
    if sel.size == 0:
        np.savez(out, pix=np.empty(0, np.int32), flux=np.empty((0, 343), np.float32))
        return path.name, 0, 0
    pix = MAP_IPIX[pos2]
    uniq, inv = np.unique(pix, return_inverse=True)
    summed = np.zeros((uniq.size, 343), dtype=np.float32)
    np.add.at(summed, inv, flux[sel])
    np.savez(out, pix=uniq.astype(np.int32), flux=summed)
    return path.name, int(sel.size), int(uniq.size)


def process_task(path):
    return process(path, OUT_DIR)


def init_worker(map_path, a_path):
    global MAP_IDS, MAP_IPIX, A_IDS
    with h5py.File(map_path, 'r') as h:
        MAP_IDS = np.asarray(h['source_id'][:], dtype=np.int64)
        MAP_IPIX = np.asarray(h['ipix'][:], dtype=np.int32)
    A_IDS = np.load(a_path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--files', nargs='+', required=True)
    ap.add_argument('--map', required=True)
    ap.add_argument('--a-ids', required=True)
    ap.add_argument('--out-dir', required=True)
    ap.add_argument('--jobs', type=int, default=1)
    args = ap.parse_args()
    global OUT_DIR
    OUT_DIR = args.out_dir
    Path(args.out_dir).mkdir(parents=True, exist_ok=True)
    init_worker(args.map, args.a_ids)
    if args.jobs <= 1:
        for p in args.files:
            print(process(p, args.out_dir), flush=True)
        return
    import multiprocessing as mp
    ctx = mp.get_context('fork')
    with ctx.Pool(args.jobs) as pool:
        for r in pool.imap_unordered(process_task, args.files):
            print(r, flush=True)


if __name__ == '__main__':
    main()
