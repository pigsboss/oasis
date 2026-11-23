"""Tests for the 343-point spectral cube builder."""

from __future__ import annotations

import csv
import gzip
import json
import tempfile
import unittest
from pathlib import Path

import numpy as np
import tables

from oasis_datasets import hpx
from oasis_datasets.consolidate import build_plan, run_consolidate
from oasis_datasets.spectra import (BP_RP_GRID, TEMPLATES, WAVELENGTH,
                                    build_spectral_cube, template_indices)

HEADER = ["source_id", "ra", "dec", "parallax", "pmra", "pmdec",
          "phot_g_mean_mag", "bp_rp", "phot_bp_mean_mag", "phot_rp_mean_mag"]


class TestSpectralCube(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.dir = Path(cls.tmp.name)
        cls.csv = cls.dir / "sources.csv.gz"
        rng = np.random.default_rng(11)
        rows = []
        with gzip.open(cls.csv, "wt", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(HEADER)
            for i in range(300):
                ra = float(rng.uniform(0, 360))
                dec = float(np.degrees(np.arcsin(rng.uniform(-1, 1))))
                g = float(rng.uniform(4, 13))
                bp_rp = float(rng.uniform(-0.4, 3.0))
                row = [str(2**60 + i), f"{ra:.12f}", f"{dec:.12f}",
                       "1.0", "0.0", "0.0", f"{g:.6f}", f"{bp_rp:.6f}",
                       f"{g - .5 * bp_rp:.6f}", f"{g + .5 * bp_rp:.6f}"]
                rows.append(row)
                w.writerow(row)
        cls.rows = rows
        schema = cls.dir / "schema.json"
        schema.write_text(json.dumps({
            "source_id": "i8", "ra": "f8", "dec": "f8", "parallax": "f8",
            "pmra": "f8", "pmdec": "f8", "phot_g_mean_mag": "f4",
            "bp_rp": "f4", "phot_bp_mean_mag": "f4", "phot_rp_mean_mag": "f4",
        }), encoding="utf-8")
        cls.plan, err = build_plan(
            source=cls.csv, dataset_path=None, app=cls.dir / "app",
            profile_spec="gaia_tier", dataset_id=None, region_spec=None,
            attributes=None, limit=None, name="speccat",
            column_profile="core", layout="spatial", order=5,
            index="source_id", jobs=1, schema=str(schema))
        assert cls.plan is not None, err
        assert run_consolidate(cls.plan, lambda *a: None) == 0
        cls.nside = 64
        cls.cube = cls.dir / "cube.h5"
        cls.res = build_spectral_cube(cls.plan.dest_h5, cls.cube,
                                      nside=cls.nside, chunk_rows=64,
                                      buffer_parents=8)
        cls.ra = np.array([float(r[1]) for r in rows])
        cls.dec = np.array([float(r[2]) for r in rows])
        cls.g = np.array([float(r[6]) for r in rows])
        cls.bp_rp = np.array([float(r[7]) for r in rows])

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_shape_wavelength(self):
        with tables.open_file(self.cube) as h5:
            flux = h5.root.spectra.flux
            self.assertEqual(flux.shape, (hpx.nside2npix(self.nside), 343))
            np.testing.assert_allclose(h5.root.spectra.wavelength[:], WAVELENGTH)
            np.testing.assert_array_equal(h5.root.spectra.count[:].sum(), 300)

    def test_cube_values_match_templates(self):
        npix = hpx.nside2npix(self.nside)
        child = hpx.ang2pix_nest(self.nside, np.radians(90 - self.dec),
                                 np.radians(self.ra))
        tidx, _ = template_indices(self.bp_rp)
        w = 10.0 ** (-0.4 * (self.g - 6.5))
        with tables.open_file(self.cube) as h5:
            flux = h5.root.spectra.flux[:]
            count = h5.root.spectra.count[:]
        for p in np.unique(child)[:10]:
            mask = child == p
            expected = (w[mask, None] * TEMPLATES[tidx[mask]]).sum(axis=0)
            np.testing.assert_allclose(flux[p], expected, rtol=2e-5, atol=1e-5)
            self.assertEqual(int(count[p]), int(mask.sum()))
        self.assertTrue(np.isfinite(flux).all())

    def test_provenance(self):
        with tables.open_file(self.cube) as h5:
            attrs = json.loads(h5.root._v_attrs.consolidate)
            self.assertTrue(attrs["inferred"])
            self.assertEqual(attrs["model"], "blackbody_bp_rp")
            self.assertEqual(attrs["quality"], 4)
            self.assertEqual(attrs["xp_fraction"], 0.0)
            self.assertEqual(int(h5.root.spectra.quality[0]), 4)


if __name__ == "__main__":
    unittest.main(verbosity=2)
