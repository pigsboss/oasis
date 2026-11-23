"""Tests for HEALPix bincount maps from consolidated tables."""

from __future__ import annotations

import csv
import gzip
import json
import tempfile
import unittest
from pathlib import Path

import numpy as np

from oasis_datasets import hpx
from oasis_datasets.consolidate import build_plan, run_consolidate
from oasis_datasets.hpxmap import build_map, write_healpix_fits

HEADER = ["source_id", "ra", "dec", "parallax", "pmra", "pmdec",
          "phot_g_mean_mag", "bp_rp", "phot_bp_mean_mag", "phot_rp_mean_mag"]


class TestHpxMap(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.dir = Path(cls.tmp.name)
        cls.csv = cls.dir / "sources.csv.gz"
        rng = np.random.default_rng(7)
        cls.rows = []
        with gzip.open(cls.csv, "wt", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(HEADER)
            for i in range(400):
                ra = float(rng.uniform(0, 360))
                dec = float(np.degrees(np.arcsin(rng.uniform(-1, 1))))
                g = float(rng.uniform(5, 12))
                bp_rp = float(rng.uniform(-0.2, 2.0))
                row = [str(2**60 + i), f"{ra:.12f}", f"{dec:.12f}",
                       "1.0", "0.0", "0.0", f"{g:.6f}", f"{bp_rp:.6f}",
                       f"{g - .5 * bp_rp:.6f}", f"{g + .5 * bp_rp:.6f}"]
                cls.rows.append(row)
                w.writerow(row)
        schema = cls.dir / "schema.json"
        schema.write_text(json.dumps({
            "source_id": "i8", "ra": "f8", "dec": "f8", "parallax": "f8",
            "pmra": "f8", "pmdec": "f8", "phot_g_mean_mag": "f4",
            "bp_rp": "f4", "phot_bp_mean_mag": "f4", "phot_rp_mean_mag": "f4",
        }), encoding="utf-8")
        cls.plan, err = build_plan(
            source=cls.csv, dataset_path=None, app=cls.dir / "app",
            profile_spec="gaia_tier", dataset_id=None, region_spec=None,
            attributes=None, limit=None, name="hpxcat",
            column_profile="core", layout="spatial", order=5,
            index="source_id", jobs=1, schema=str(schema))
        assert cls.plan is not None, err
        assert run_consolidate(cls.plan, lambda *a: None) == 0
        cls.path = cls.plan.dest_h5
        cls.ra = np.array([float(r[1]) for r in cls.rows])
        cls.dec = np.array([float(r[2]) for r in cls.rows])
        cls.g = np.array([float(r[6]) for r in cls.rows])
        cls.bp_rp = np.array([float(r[7]) for r in cls.rows])

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_count_coarse_uses_ipix(self):
        nside = 8
        res = build_map(self.path, nside=nside, quantity="count")
        npix = hpx.nside2npix(nside)
        expected = np.bincount(hpx.ang2pix_nest(
            nside, np.radians(90 - self.dec), np.radians(self.ra)), minlength=npix)
        np.testing.assert_array_equal(res.values, expected)

    def test_count_fine_uses_radec(self):
        nside = 64
        res = build_map(self.path, nside=nside, quantity="count")
        npix = hpx.nside2npix(nside)
        expected = np.bincount(hpx.ang2pix_nest(
            nside, np.radians(90 - self.dec), np.radians(self.ra)), minlength=npix)
        np.testing.assert_array_equal(res.values, expected)
        self.assertIn("ra/dec", res.meta["pixel_source"])

    def test_sum_and_mean(self):
        nside = 8
        npix = hpx.nside2npix(nside)
        pix = hpx.ang2pix_nest(nside, np.radians(90 - self.dec), np.radians(self.ra))
        vals = 10.0 ** (-0.4 * self.g)
        s = build_map(self.path, nside=nside, quantity="sum",
                      expr="10**(-0.4*phot_g_mean_mag)", unit="relative flux")
        np.testing.assert_allclose(s.values, np.bincount(pix, weights=vals, minlength=npix),
                                   rtol=1e-5, atol=1e-9)
        m = build_map(self.path, nside=nside, quantity="mean", expr="bp_rp")
        expected = np.divide(np.bincount(pix, weights=self.bp_rp, minlength=npix),
                             np.bincount(pix, minlength=npix),
                             out=np.zeros(npix), where=np.bincount(pix, minlength=npix) > 0)
        np.testing.assert_allclose(m.values, expected, rtol=1e-5, atol=1e-8)

    def test_weighted_mean_and_fits(self):
        nside = 8
        npix = hpx.nside2npix(nside)
        pix = hpx.ang2pix_nest(nside, np.radians(90 - self.dec), np.radians(self.ra))
        w = 10.0 ** (-0.4 * self.g)
        res = build_map(self.path, nside=nside, quantity="weighted_mean",
                        expr="bp_rp", weight_expr="10**(-0.4*phot_g_mean_mag)")
        num = np.bincount(pix, weights=self.bp_rp * w, minlength=npix)
        den = np.bincount(pix, weights=w, minlength=npix)
        expected = np.divide(num, den, out=np.zeros(npix), where=den != 0)
        np.testing.assert_allclose(res.values, expected, rtol=1e-5, atol=1e-8)
        out = write_healpix_fits(self.dir / "map.fits", res)
        raw = out.read_bytes()
        for token in (b"PIXTYPE", b"HEALPIX", b"ORDERING", b"NESTED",
                      b"NSIDE", b"QUANTITY", b"WEIGHTEX"):
            self.assertIn(token, raw)
        self.assertGreater(out.stat().st_size, 2880)


if __name__ == "__main__":
    unittest.main(verbosity=2)
