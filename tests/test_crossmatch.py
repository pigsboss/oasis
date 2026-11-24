"""Tests for generic HDF5 spatial cross-match."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import numpy as np
import tables

from oasis_datasets import hpx
from oasis_datasets.crossmatch import crossmatch_tables


class TestCrossmatch(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)
        rng = np.random.default_rng(4)
        left = rng.uniform([0, -60], [360, 60], size=(400, 2))
        right = np.vstack([
            left[:120] + rng.normal(0, 1e-5, size=(120, 2)),
            rng.uniform([0, -60], [360, 60], size=(2000, 2)),
        ])
        self.left_ra, self.left_dec = left[:, 0], left[:, 1]
        self.right_ra, self.right_dec = right[:, 0], right[:, 1]
        self.left = self.dir / "left.h5"
        self.right = self.dir / "right.h5"
        dt = np.dtype([("source_id", "i8"), ("ra", "f8"), ("dec", "f8")])
        with tables.open_file(self.left, "w") as h:
            t = h.create_table("/", "table", dt)
            a = np.empty(400, dtype=dt)
            a["source_id"] = np.arange(400)
            a["ra"] = self.left_ra
            a["dec"] = self.left_dec
            t.append(a)
        with tables.open_file(self.right, "w") as h:
            t = h.create_table("/", "table", dt)
            a = np.empty(2120, dtype=dt)
            a["source_id"] = np.arange(2120)
            a["ra"] = self.right_ra
            a["dec"] = self.right_dec
            t.append(a)

    def tearDown(self):
        self.tmp.cleanup()

    def test_nearest_matches_bruteforce(self):
        out = self.dir / "m.h5"
        res = crossmatch_tables(self.left, self.right, out, radius_arcsec=5,
                                left_id="source_id", right_id="source_id")
        self.assertEqual(res.matches, 120)
        with tables.open_file(out) as h:
            m = h.root.matches[:]
        self.assertEqual(len(m), 120)
        # brute-force check each left's nearest distance
        for row in m:
            i, j, sep = int(row["left_index"]), int(row["right_id"]), row["sep_arcsec"]
            allsep = hpx.angular_distance_deg(
                self.left_ra[i], self.left_dec[i],
                self.right_ra, self.right_dec) * 3600
            self.assertLessEqual(sep, 5.0 + 1e-6)
            self.assertAlmostEqual(sep, allsep[j], places=6)

    def test_csv(self):
        out = self.dir / "m.csv"
        res = crossmatch_tables(self.left, self.right, out, radius_arcsec=5,
                                fmt="csv")
        self.assertEqual(res.matches, 120)
        self.assertEqual(len(out.read_text().splitlines()), 121)


if __name__ == "__main__":
    unittest.main(verbosity=2)
