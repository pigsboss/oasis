"""Tests for compact AllWISE/2MASS consolidation profiles."""

from __future__ import annotations

import bz2
import gzip
import shutil
import tempfile
import unittest
from pathlib import Path

import numpy as np
import tables

from oasis_datasets.consolidate import (ALLWISE_COLUMNS, build_plan,
                                        run_consolidate)


class TestNirConsolidate(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def _allwise(self):
        d = self.root / "WISE"
        d.mkdir()
        with bz2.open(d / "wise-allwise-cat-part01.bz2", "wt") as f:
            for i in range(3):
                vals = ["1"] * len(ALLWISE_COLUMNS)
                vals[ALLWISE_COLUMNS.index("designation")] = f"J{i:04d}"
                vals[ALLWISE_COLUMNS.index("ra")] = str(10.0 + i)
                vals[ALLWISE_COLUMNS.index("dec")] = "20.0"
                vals[ALLWISE_COLUMNS.index("source_id")] = f"S{i}"
                vals[ALLWISE_COLUMNS.index("coadd_id")] = f"C{i}"
                vals[ALLWISE_COLUMNS.index("ph_qual")] = "AAAA"
                vals[ALLWISE_COLUMNS.index("cc_flags")] = "0000"
                f.write("|".join(vals) + "|\n")
        return d

    def _2mass(self):
        d = self.root / "2MASS"
        d.mkdir()
        shutil.copy("/mnt/data/huo/Datasets/2MASS/twomass_psc_schema",
                    d / "twomass_psc_schema")
        with gzip.open(d / "psc_aaa.gz", "wt") as f:
            for i in range(3):
                vals = ["1"] * 60
                vals[0] = str(10.0 + i)
                vals[1] = "20.0"
                vals[5] = f"DES{i:03d}"
                vals[6] = "15.0"
                vals[10] = "14.0"
                vals[14] = "13.0"
                vals[18] = "AAA"
                vals[19] = "111"
                vals[20] = "000"
                f.write("|".join(vals) + "\n")
        return d

    def test_allwise_compact(self):
        src = self._allwise()
        plan, err = build_plan(
            source=src, dataset_path=None, app=self.root / "out",
            profile_spec="allwise_nir", dataset_id=None, region_spec=None,
            attributes=None, limit=None, name="wise_test",
            column_profile="core", layout="spatial", order=9,
            index=None, jobs=1, schema=None)
        self.assertIsNotNone(plan, err)
        self.assertEqual(run_consolidate(plan, lambda *a: None), 0)
        with tables.open_file(plan.dest_h5) as h:
            t = h.root.table
            self.assertEqual(t.nrows, 3)
            self.assertIn("designation", t.dtype.names)
            self.assertIn("w1mpro", t.dtype.names)
            self.assertNotIn("rchi2", t.dtype.names)

    def test_twomass_compact(self):
        src = self._2mass()
        plan, err = build_plan(
            source=src, dataset_path=None, app=self.root / "out2",
            profile_spec="twomass_nir", dataset_id=None, region_spec=None,
            attributes=None, limit=None, name="tm_test",
            column_profile="core", layout="spatial", order=9,
            index=None, jobs=1, schema=None)
        self.assertIsNotNone(plan, err)
        self.assertEqual(run_consolidate(plan, lambda *a: None), 0)
        with tables.open_file(plan.dest_h5) as h:
            t = h.root.table
            self.assertEqual(t.nrows, 3)
            self.assertIn("j_m", t.dtype.names)
            self.assertNotIn("j_m_stdap", t.dtype.names)


if __name__ == "__main__":
    unittest.main(verbosity=2)
