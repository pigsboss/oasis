#!/usr/bin/env python3
"""Build a source_id -> ipix lookup sorted by source_id."""
from __future__ import annotations
import argparse, time
from pathlib import Path
import numpy as np
import tables
import h5py
from oasis_datasets import hpx

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--core',default='/mnt/data/huo/Datasets/Gaia/gdr3/consolidated/gaia_dr3_core_spatial.h5')
    ap.add_argument('--out',required=True)
    args=ap.parse_args()
    with tables.open_file(args.core,'r') as h:
        t=h.root.table
        n=int(t.nrows)
        print('read ids',flush=True); t0=time.time()
        sid=np.asarray(t.cols.source_id[:],dtype=np.int64)
        print('read ipix',time.time()-t0,flush=True)
        ra=np.asarray(t.cols.ra[:],dtype=np.float64)
        dec=np.asarray(t.cols.dec[:],dtype=np.float64)
        ipix=np.asarray(hpx.ang2pix_nest(2048, np.radians(90.0-dec),
                                         np.radians(np.mod(ra,360.0))),dtype=np.int32)
        del ra, dec
    print('sort',flush=True); order=np.argsort(sid,kind='stable')
    sid=sid[order]; ipix=ipix[order]
    out=Path(args.out); out.parent.mkdir(parents=True,exist_ok=True)
    with h5py.File(out,'w') as h:
        h.create_dataset('source_id',data=sid)
        h.create_dataset('ipix',data=ipix)
        h.attrs['rows']=n; h.attrs['nside']=2048
    print('wrote',out,n,flush=True)
if __name__=='__main__': main()
