"""Tests for the PyTables consolidated Gaia catalogue (core/spatial/select)."""

from __future__ import annotations

import csv
import gzip
import json
import math
import tempfile
import unittest
from pathlib import Path

import numpy as np
import tables

from oasis_datasets.consolidate import build_plan, run_consolidate
from oasis_datasets.select import ConsolidatedCatalog

HEADER = ["source_id", "ra", "dec", "parallax", "pmra", "pmdec",
          "phot_g_mean_mag", "bp_rp", "phot_bp_mean_mag", "phot_rp_mean_mag"]


def make_csv(path: Path, n=300):
    rng = np.random.default_rng(42)
    rows = []
    # A compact cluster for deterministic cone/box tests.
    for i in range(n):
        if i < 100:
            ra = 83.8 + rng.normal(0, 0.2)
            dec = -5.4 + rng.normal(0, 0.2)
        else:
            ra = rng.uniform(0, 360)
            dec = math.degrees(math.asin(rng.uniform(-1, 1)))
        g = float(rng.uniform(4, 12))
        bp_rp = float(rng.uniform(-0.2, 2.0))
        rows.append([str(2**60 + i), f"{ra % 360:.12f}", f"{dec:.12f}",
                     "null" if i % 7 == 0 else f"{rng.uniform(0.1, 10):.8f}",
                     f"{rng.normal(0, 20):.8f}", f"{rng.normal(0, 20):.8f}",
                     f"{g:.6f}", f"{bp_rp:.6f}",
                     f"{g - 0.5 * bp_rp:.6f}", f"{g + 0.5 * bp_rp:.6f}"])
    with gzip.open(path, "wt", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(HEADER)
        writer.writerows(rows)
    return rows


class TestConsolidate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.dir = Path(cls.tmp.name)
        cls.csv = cls.dir / "gaia.csv.gz"
        cls.rows = make_csv(cls.csv)
        cls.plan, err = build_plan(
            source=cls.csv, dataset_path=None, app=cls.dir / "app",
            profile_spec="gaia_tier", dataset_id=None, region_spec=None,
            attributes=None, limit=None, name="testcat",
            column_profile="core", layout="spatial", order=5,
            index="source_id,phot_g_mean_mag")
        assert cls.plan is not None, err
        cls.rc = run_consolidate(cls.plan, lambda *a: None)
        cls.path = cls.plan.dest_h5

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_build_layout(self):
        self.assertEqual(self.rc, 0)
        self.assertTrue(self.path.is_file())
        with tables.open_file(self.path) as h5:
            t = h5.root.table
            self.assertEqual(t.nrows, len(self.rows))
            self.assertIn("ipix", t.dtype.names)
            self.assertIn("source_id", t.dtype.names)
            self.assertEqual(int(t.attrs.order), 5)
            self.assertEqual(str(t.attrs.layout), "spatial")
            ip = t.cols.ipix[:]
            self.assertTrue(np.all(ip[:-1] <= ip[1:]))
            self.assertIn("ipix_pixels", h5.root.index)
            self.assertIn("ipix_offsets", h5.root.index)
            self.assertEqual(h5.root.index.ipix_offsets[0], 0)
            self.assertEqual(h5.root.index.ipix_offsets[-1], t.nrows)
            self.assertTrue(t.cols.source_id.is_indexed)
            self.assertTrue(t.cols.phot_g_mean_mag.is_indexed)
            row = t.read_where(f"source_id == {int(self.rows[0][0])}")[0]
            self.assertAlmostEqual(float(row["ra"]),
                                   float(self.rows[0][1]), places=10)

    def test_select_id_and_where(self):
        cat = ConsolidatedCatalog(self.path)
        target = int(self.rows[0][0])
        sel = cat.select(ids=[target])
        self.assertEqual(len(sel), 1)
        self.assertEqual(int(sel.arrays["source_id"][0]), target)
        sel = cat.select(where="phot_g_mean_mag < 6",
                         columns=["source_id", "phot_g_mean_mag"])
        expected = [r for r in self.rows if float(r[6]) < 6]
        self.assertEqual(len(sel), len(expected))

    def test_select_cone_matches_bruteforce(self):
        ra0, dec0, radius = 83.8, -5.4, 1.0
        cat = ConsolidatedCatalog(self.path)
        sel = cat.select(cone=(ra0, dec0, radius),
                         columns=["source_id", "ra", "dec"])
        got = set(int(x) for x in sel.arrays["source_id"])
        expected = set()
        for r in self.rows:
            ra, dec = float(r[1]), float(r[2])
            dlon = math.radians(ra - ra0)
            dlat = math.radians(dec - dec0)
            a = (math.sin(dlat / 2) ** 2
                 + math.cos(math.radians(dec0)) * math.cos(math.radians(dec))
                 * math.sin(dlon / 2) ** 2)
            if math.degrees(2 * math.asin(min(1.0, math.sqrt(a)))) <= radius:
                expected.add(int(r[0]))
        self.assertEqual(got, expected)

    def test_select_box_and_limit(self):
        cat = ConsolidatedCatalog(self.path)
        sel = cat.select(box=(83.0, 84.6, -6.2, -4.6),
                         columns=["source_id", "ra", "dec"])
        for row in sel.arrays:
            self.assertTrue(83.0 <= float(row["ra"]) <= 84.6)
            self.assertTrue(-6.2 <= float(row["dec"]) <= -4.6)
        limited = cat.select(where="phot_g_mean_mag < 12", limit=7)
        self.assertEqual(len(limited), 7)
        empty = cat.select(cone=(0.0, 90.0, 0.001))
        self.assertEqual(len(empty), 0)
        self.assertEqual(empty.arrays.dtype.names,
                         tuple(cat.columns))

    def test_parallel_shards(self):
        shard_dir = self.dir / "shards"
        shard_dir.mkdir()
        for k in range(3):
            with gzip.open(shard_dir / f"part{k}.csv.gz", "wt", newline="") as fh:
                writer = csv.writer(fh)
                writer.writerow(HEADER)
                writer.writerows(self.rows[k::3])
        schema = self.dir / "schema.json"
        schema.write_text(json.dumps({
            "source_id": "i8", "ra": "f8", "dec": "f8",
            "parallax": "f8", "pmra": "f8", "pmdec": "f8",
            "phot_g_mean_mag": "f8", "bp_rp": "f8",
            "phot_bp_mean_mag": "f8", "phot_rp_mean_mag": "f8",
        }), encoding="utf-8")
        plan, err = build_plan(
            source=shard_dir, dataset_path=None, app=self.dir / "parallelapp",
            profile_spec="gaia_tier", dataset_id=None, region_spec=None,
            attributes=None, limit=None, name="parallel",
            column_profile="core", layout="spatial", order=5,
            index="source_id", jobs=2, schema=str(schema))
        self.assertIsNotNone(plan, err)
        self.assertEqual(len(plan.source_files), 3)
        self.assertEqual(run_consolidate(plan, lambda *a: None), 0)
        cat = ConsolidatedCatalog(plan.dest_h5)
        self.assertEqual(cat.rows, len(self.rows))
        self.assertEqual(len(cat.select(ids=[int(self.rows[-1][0])])), 1)

    def test_csr_layout(self):
        schema = self.dir / "schema_csr.json"
        schema.write_text(json.dumps({
            "source_id": "i8", "ra": "f8", "dec": "f8",
            "parallax": "f8", "pmra": "f8", "pmdec": "f8",
            "phot_g_mean_mag": "f8", "bp_rp": "f8",
            "phot_bp_mean_mag": "f8", "phot_rp_mean_mag": "f8",
        }), encoding="utf-8")
        plan, err = build_plan(
            source=self.csv, dataset_path=None, app=self.dir / "csrapp",
            profile_spec="gaia_tier", dataset_id=None, region_spec=None,
            attributes=None, limit=None, name="csr",
            column_profile="core", layout="csr", order=5,
            index="source_id", jobs=1, schema=str(schema))
        self.assertIsNotNone(plan, err)
        self.assertEqual(run_consolidate(plan, lambda *a: None), 0)
        with tables.open_file(plan.dest_h5) as h5:
            self.assertEqual(str(h5.root.table.attrs.layout), "csr")
            self.assertIn("ipix_rowids", h5.root.index)
            self.assertEqual(len(h5.root.index.ipix_rowids), len(self.rows))
        cat = ConsolidatedCatalog(plan.dest_h5)
        self.assertEqual(cat.rows, len(self.rows))
        self.assertEqual(len(cat.select(ids=[int(self.rows[0][0])])), 1)
        sel = cat.select(cone=(83.8, -5.4, 1.0),
                         columns=["source_id", "ra", "dec"])
        self.assertGreater(len(sel), 0)
        for row in sel.arrays:
            sep = __import__("math").degrees(2 * __import__("math").asin(min(
                1.0, (__import__("math").sin(__import__("math").radians(float(row["dec"]) - -5.4) / 2) ** 2
                      + __import__("math").cos(__import__("math").radians(-5.4))
                      * __import__("math").cos(__import__("math").radians(float(row["dec"])))
                      * __import__("math").sin(__import__("math").radians(float(row["ra"]) - 83.8) / 2) ** 2) ** 0.5)))
            self.assertLessEqual(sep, 1.0 + 1e-9)
        where = cat.select(cone=(83.8, -5.4, 1.0),
                           where="phot_g_mean_mag < 8")
        self.assertLessEqual(len(where), len(sel))

    def test_fits_roundtrip(self):
        try:
            from astropy.table import Table
            from astropy.io import fits  # noqa: F401
        except Exception:
            self.skipTest("astropy not installed")
        rows = self.rows[:20]
        cols = {}
        for j, name in enumerate(HEADER):
            if name == "source_id":
                cols[name] = np.array([int(r[j]) for r in rows], dtype=np.int64)
            else:
                vals = []
                for r in rows:
                    try:
                        vals.append(float(r[j]) if r[j] != "null" else np.nan)
                    except ValueError:
                        vals.append(np.nan)
                cols[name] = np.array(vals, dtype=np.float64)
        fits_path = self.dir / "gaia.fits"
        Table(cols).write(fits_path, overwrite=True)
        plan, err = build_plan(
            source=fits_path, dataset_path=None, app=self.dir / "fitsapp",
            profile_spec="gaia_tier", dataset_id=None, region_spec=None,
            attributes=None, limit=None, name="fitscat",
            column_profile="core", layout="spatial", order=5,
            index="source_id")
        self.assertIsNotNone(plan, err)
        self.assertEqual(run_consolidate(plan, lambda *a: None), 0)
        cat = ConsolidatedCatalog(plan.dest_h5)
        self.assertEqual(cat.rows, 20)
        self.assertEqual(len(cat.select(ids=[int(rows[0][0])])), 1)


if __name__ == "__main__":
    unittest.main()
