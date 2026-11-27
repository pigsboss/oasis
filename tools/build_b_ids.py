#!/usr/bin/env python3
"""Extract B IDs = has_xp_continuous & not has_xp_sampled from full Gaia table."""
from __future__ import annotations
import time
from pathlib import Path
import numpy as np
import tables

P='/mnt/data/huo/Datasets/Gaia/gdr3/gaia_blosc5.h5'
OUT='/mnt/data/huo/Datasets/Gaia/gdr3/consolidated/xp_b_ids.npy'

with tables.open_file(P,'r') as h:
    t=h.root.full
    n=int(t.nrows)
    print('read continuous',flush=True); t0=time.time()
    c=np.asarray(t.cols.has_xp_continuous[:],dtype=bool)
    print('read sampled',flush=True)
    s=np.asarray(t.cols.has_xp_sampled[:],dtype=bool)
    print('read ids',flush=True)
    ids=np.asarray(t.cols.source_id[:],dtype=np.int64)
mask=c & ~s
out=ids[mask]; out.sort()
np.save(OUT,out)
print('total',n,'B',out.size,'elapsed',time.time()-t0,flush=True)
