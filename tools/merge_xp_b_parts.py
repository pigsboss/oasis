#!/usr/bin/env python3
"""Merge per-file sparse B pixel sums into a dense npix x 343 HDF5 array."""
from __future__ import annotations
import argparse, json, re, time
from pathlib import Path
import numpy as np
import h5py

NPIX=50331648; NW=343

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--parts', required=True)
    ap.add_argument('--log', required=True)
    ap.add_argument('--out', required=True)
    args=ap.parse_args()
    parts=sorted(Path(args.parts).glob('*.npz'))
    print('parts',len(parts),flush=True)
    bmap=np.zeros((NPIX,NW),dtype=np.float32)
    total_src=0; total_pix=0; t0=time.time()
    for i,p in enumerate(parts):
        z=np.load(p)
        pix=z['pix'].astype(np.int64); flux=z['flux']
        if pix.size:
            np.add.at(bmap,pix,flux)
            total_pix += int(pix.size)
        if (i+1)%100==0:
            print(i+1,'elapsed',time.time()-t0,'entries',total_pix,flush=True)
    # parse B source counts from log tuples
    text=Path(args.log).read_text(errors='ignore')
    vals=re.findall(r"\('XpContinuousMeanSpectrum_[^']+',\s*(\d+),\s*(\d+)\)",text)
    total_b=sum(int(a) for a,b in vals)
    print('parts tuples',len(vals),'B sources',total_b,'pixel entries',total_pix,flush=True)
    with h5py.File(args.out,'w') as h:
        h.create_dataset('flux',data=bmap,chunks=(8192,NW),compression='lzf')
        h.attrs['npix']=NPIX; h.attrs['nwave']=NW
        h.attrs['b_sources']=total_b; h.attrs['pixel_entries']=total_pix
    print('wrote',args.out,flush=True)

if __name__=='__main__': main()
