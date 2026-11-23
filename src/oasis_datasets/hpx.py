"""HEALPix primitives for the OASIS sky prototype.

This module is deliberately self-contained (numpy only).  It implements the
parts of the HEALPix standard needed by the sky store and renderer:

* NESTED and RING pixel schemes, order/nside bookkeeping;
* :func:`ang2pix` / :func:`pix2ang` for both schemes;
* conversion between schemes through pixel centres (exact for centres);
* vectorised angular distance and disc candidate selection;
* NESTED hierarchy helpers (parent / children), which are used by the
  adaptive tile pyramid.

The NESTED formulas were transcribed from the reference HEALPix C
implementation (``pix2ang_nest.c`` / ``ang2pix_nest.c``) and are validated
against ``healpy`` in ``tests/test_hpx.py``.  RING formulas follow
``pix2ang_ring.c`` / ``ang2pix_ring.c``.  Both are BSD/GPL-compatible
reference algorithms; this file is an independent numpy transcription.

Conventions
-----------
* ``theta`` is the colatitude in [0, pi]; ``phi`` is the longitude in
  [0, 2*pi).  ``ra``/``dec`` helpers use degrees and the ICRS convention.
* ``nside`` must be a power of two for the NESTED helpers.  RING works for
  any positive nside, but the sky store only uses powers of two so that a
  tile has four children at the next order.
"""

from __future__ import annotations

import math

import numpy as np

__all__ = [
    "MAX_NSIDE",
    "nside2order",
    "order2nside",
    "validate_nside",
    "nside2npix",
    "npix2nside",
    "nside2pixarea_sr",
    "nside2resol_deg",
    "max_tile_radius_rad",
    "max_tile_radius_deg",
    "ang2pix_nest",
    "pix2ang_nest",
    "ang2pix_ring",
    "pix2ang_ring",
    "ang2pix",
    "pix2ang",
    "nest2ring",
    "ring2nest",
    "pix2vec_nest",
    "vec2pix_nest",
    "nested_parent",
    "nested_children",
    "nested_children_range",
    "angular_distance_deg",
    "disc_candidates",
    "query_disc_centers",
]

#: Largest nside used by the reference implementation (2**13).
MAX_NSIDE = 8192

#: Lowest corner of each HEALPix face, in units of nside (0-based faces).
_JRLL = np.array([2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4], dtype=np.int64)
#: Longitude index of the lowest corner, in units of nside/2 (0-based faces).
_JPLL = np.array([1, 3, 5, 7, 0, 2, 4, 6, 1, 3, 5, 7], dtype=np.int64)

#: Conservative centre-to-boundary radius of a HEALPix pixel, in units of
#: 1/nside radians.  The measured maximum is ~1.0687/nside; 1.08 is safe.
_TILE_RADIUS_FACTOR = 1.08


# ── resolution bookkeeping ──────────────────────────────────────────
def validate_nside(nside: int) -> int:
    nside = int(nside)
    if nside < 1 or nside > MAX_NSIDE:
        raise ValueError(f"nside must be in [1, {MAX_NSIDE}], got {nside}")
    return nside


def nside2order(nside: int) -> int:
    nside = validate_nside(nside)
    if nside & (nside - 1):
        raise ValueError(f"nside must be a power of two for NESTED, got {nside}")
    return int(round(math.log2(nside)))


def order2nside(order: int) -> int:
    order = int(order)
    if order < 0 or order > 13:
        raise ValueError(f"order must be in [0, 13], got {order}")
    return 1 << order


def nside2npix(nside: int) -> int:
    nside = validate_nside(nside)
    return 12 * nside * nside


def npix2nside(npix: int) -> int:
    npix = int(npix)
    nside = int(round(math.sqrt(npix / 12.0)))
    if nside * nside * 12 != npix:
        raise ValueError(f"{npix} is not a valid HEALPix npix")
    return validate_nside(nside)


def nside2pixarea_sr(nside: int) -> float:
    nside = validate_nside(nside)
    return 4.0 * math.pi / (12.0 * nside * nside)


def nside2resol_deg(nside: int) -> float:
    """Approximate angular resolution (sqrt(pixel area)) in degrees."""
    nside = validate_nside(nside)
    return math.degrees(math.sqrt(nside2pixarea_sr(nside)))


def max_tile_radius_rad(nside: int) -> float:
    """Conservative upper bound for the centre-to-boundary angular radius."""
    nside = validate_nside(nside)
    return _TILE_RADIUS_FACTOR / nside


def max_tile_radius_deg(nside: int) -> float:
    return math.degrees(max_tile_radius_rad(nside))


# ── NESTED: bit interleaving helpers ────────────────────────────────
def _pix2xy(ipf: np.ndarray, order: int) -> tuple[np.ndarray, np.ndarray]:
    """De-interleave the Morton index into face-local (ix, iy)."""
    ix = np.zeros_like(ipf, dtype=np.int64)
    iy = np.zeros_like(ipf, dtype=np.int64)
    for i in range(order):
        ix |= ((ipf >> (2 * i)) & 1) << i
        iy |= ((ipf >> (2 * i + 1)) & 1) << i
    return ix, iy


def _xy2pix(ix: np.ndarray, iy: np.ndarray, order: int) -> np.ndarray:
    """Interleave face-local (ix, iy) into a Morton index."""
    out = np.zeros_like(ix, dtype=np.int64)
    for i in range(order):
        out |= ((ix >> i) & 1) << (2 * i)
        out |= ((iy >> i) & 1) << (2 * i + 1)
    return out


def _validate_angles(theta: np.ndarray, phi: np.ndarray) -> None:
    if not np.all(np.isfinite(theta)):
        raise ValueError("theta contains NaN/Inf")
    if not np.all(np.isfinite(phi)):
        raise ValueError("phi contains NaN/Inf")
    if np.any(theta < 0.0) or np.any(theta > np.pi):
        raise ValueError("theta (colatitude) must be in [0, pi]")


# ── NESTED: angular <-> pixel ───────────────────────────────────────
def ang2pix_nest(nside: int, theta, phi) -> np.ndarray:
    """Return NESTED pixel numbers for colatitude/longitude in radians.

    Parameters are broadcast; scalar inputs yield a 0-d integer array.
    """
    nside = validate_nside(nside)
    order = nside2order(nside)
    theta = np.asarray(theta, dtype=np.float64)
    phi = np.asarray(phi, dtype=np.float64)
    shape = np.broadcast(theta, phi).shape
    theta = np.broadcast_to(theta, shape)
    phi = np.broadcast_to(phi, shape)
    _validate_angles(theta, phi)

    z = np.cos(theta)
    za = np.abs(z)
    tt = np.mod(phi / (np.pi / 2.0), 4.0)

    # Equatorial region: |z| <= 2/3
    eq = za <= 2.0 / 3.0
    temp1 = nside * (0.5 + tt)
    temp2 = nside * z * 0.75
    jp_eq = np.floor(temp1 - temp2).astype(np.int64)
    jm_eq = np.floor(temp1 + temp2).astype(np.int64)
    ifp = jp_eq // nside
    ifm = jm_eq // nside
    face_eq = np.where(ifp == ifm, ifp | 4, np.where(ifp < ifm, ifp, ifm + 8))
    ix_eq = jm_eq & (nside - 1)
    iy_eq = nside - (jp_eq & (nside - 1)) - 1

    # Polar regions.
    ntt = np.floor(tt).astype(np.int64)
    ntt = np.where(ntt == 4, 3, ntt)
    tp = tt - ntt
    tmp = nside * np.sqrt(3.0 * (1.0 - za))
    jp_p = np.minimum(np.floor(tp * tmp).astype(np.int64), nside - 1)
    jm_p = np.minimum(np.floor((1.0 - tp) * tmp).astype(np.int64), nside - 1)
    north = z >= 0.0
    face_p = np.where(north, ntt, ntt + 8)
    ix_p = np.where(north, nside - jm_p - 1, jp_p)
    iy_p = np.where(north, nside - jp_p - 1, jm_p)

    face = np.where(eq, face_eq, face_p)
    ix = np.where(eq, ix_eq, ix_p)
    iy = np.where(eq, iy_eq, iy_p)
    return face * (nside * nside) + _xy2pix(ix, iy, order)


def pix2ang_nest(nside: int, ipix) -> tuple[np.ndarray, np.ndarray]:
    """Return (theta, phi) of NESTED pixel centres in radians."""
    nside = validate_nside(nside)
    order = nside2order(nside)
    ipix = np.asarray(ipix, dtype=np.int64)
    npface = nside * nside
    face = ipix // npface
    ipf = ipix % npface
    if np.any(face < 0) or np.any(face > 11):
        raise ValueError("NESTED pixel number out of range")
    ix, iy = _pix2xy(ipf, order)

    jrt = ix + iy
    jpt = ix - iy
    jr = _JRLL[face] * nside - jrt - 1

    fact1 = 1.0 / (3.0 * nside * nside)
    fact2 = 2.0 / (3.0 * nside)
    nr = np.full(jr.shape, nside, dtype=np.int64)
    z = (2 * nside - jr) * fact2
    kshift = (jr - nside) % 2

    north = jr < nside
    south = jr > 3 * nside
    nr = np.where(north, jr, np.where(south, 4 * nside - jr, nr))
    z = np.where(north, 1.0 - nr * nr * fact1,
                 np.where(south, -1.0 + nr * nr * fact1, z))
    kshift = np.where(north | south, 0, kshift)

    theta = np.arccos(np.clip(z, -1.0, 1.0))
    jp = (_JPLL[face] * nr + jpt + 1 + kshift) // 2
    jp = np.where(jp > 4 * nside, jp - 4 * nside, jp)
    jp = np.where(jp < 1, jp + 4 * nside, jp)
    phi = (jp - (kshift + 1) * 0.5) * (np.pi / 2.0 / nr)
    return theta, phi


# ── RING: angular <-> pixel ─────────────────────────────────────────
def ang2pix_ring(nside: int, theta, phi) -> np.ndarray:
    """Return RING pixel numbers for colatitude/longitude in radians."""
    nside = validate_nside(nside)
    theta = np.asarray(theta, dtype=np.float64)
    phi = np.asarray(phi, dtype=np.float64)
    shape = np.broadcast(theta, phi).shape
    theta = np.broadcast_to(theta, shape)
    phi = np.broadcast_to(phi, shape)
    _validate_angles(theta, phi)

    z = np.cos(theta)
    za = np.abs(z)
    tt = np.mod(phi / (np.pi / 2.0), 4.0)
    nl2 = 2 * nside
    nl4 = 4 * nside
    ncap = nl2 * (nside - 1)
    npix = 12 * nside * nside

    ipix1 = np.zeros(shape, dtype=np.int64)
    eq = za <= 2.0 / 3.0

    # Equatorial region.
    jp = np.floor(nside * (0.5 + tt - z * 0.75)).astype(np.int64)
    jm = np.floor(nside * (0.5 + tt + z * 0.75)).astype(np.int64)
    ir = nside + 1 + jp - jm
    kshift = (ir % 2 == 0).astype(np.int64)
    ip = np.floor((jp + jm - nside + kshift + 1) / 2.0).astype(np.int64) + 1
    ip = np.where(ip > nl4, ip - nl4, ip)
    ipix1_eq = ncap + nl4 * (ir - 1) + ip

    # Polar regions.
    tp = tt - np.floor(tt)
    tmp = np.sqrt(3.0 * (1.0 - za))
    jp_p = np.floor(nside * tp * tmp).astype(np.int64)
    jm_p = np.floor(nside * (1.0 - tp) * tmp).astype(np.int64)
    ir_p = jp_p + jm_p + 1
    ip_p = np.floor(tt * ir_p).astype(np.int64) + 1
    ip_p = np.where(ip_p > 4 * ir_p, ip_p - 4 * ir_p, ip_p)
    ipix1_p = 2 * ir_p * (ir_p - 1) + ip_p
    ipix1_s = npix - 2 * ir_p * (ir_p + 1) + ip_p
    ipix1_p = np.where(z <= 0.0, ipix1_s, ipix1_p)

    ipix1 = np.where(eq, ipix1_eq, ipix1_p)
    return ipix1 - 1


def pix2ang_ring(nside: int, ipix) -> tuple[np.ndarray, np.ndarray]:
    """Return (theta, phi) of RING pixel centres in radians."""
    nside = validate_nside(nside)
    ipix = np.asarray(ipix, dtype=np.int64)
    npix = 12 * nside * nside
    if np.any(ipix < 0) or np.any(ipix >= npix):
        raise ValueError("RING pixel number out of range")
    ipix1 = ipix + 1
    nl2 = 2 * nside
    nl4 = 4 * nside
    ncap = 2 * nside * (nside - 1)
    fact1 = 1.5 * nside
    fact2 = 3.0 * nside * nside

    theta = np.empty(ipix.shape, dtype=np.float64)
    phi = np.empty(ipix.shape, dtype=np.float64)

    # North polar cap.
    north = ipix1 <= ncap
    hip = ipix1 / 2.0
    fihip = np.floor(hip)
    iring = np.floor(np.sqrt(hip - np.sqrt(fihip))).astype(np.int64) + 1
    iphi = ipix1 - 2 * iring * (iring - 1)
    theta_n = np.arccos(np.clip(1.0 - iring * iring / fact2, -1.0, 1.0))
    phi_n = (iphi - 0.5) * np.pi / (2.0 * iring)
    theta = np.where(north, theta_n, theta)
    phi = np.where(north, phi_n, phi)

    # Equatorial region.
    eq = (~north) & (ipix1 <= nl2 * (5 * nside + 1))
    ip = ipix1 - ncap - 1
    iring_e = ip // nl4 + nside
    iphi_e = (ip % nl4) + 1
    fodd = 0.5 * (1 + ((iring_e + nside) % 2))
    theta_e = np.arccos(np.clip((nl2 - iring_e) / fact1, -1.0, 1.0))
    phi_e = (iphi_e - fodd) * np.pi / (2.0 * nside)
    theta = np.where(eq, theta_e, theta)
    phi = np.where(eq, phi_e, phi)

    # South polar cap.
    south = ~(north | eq)
    ip_s = npix - ipix1 + 1
    hip_s = ip_s / 2.0
    fihip_s = np.floor(hip_s)
    iring_s = np.floor(np.sqrt(hip_s - np.sqrt(fihip_s))).astype(np.int64) + 1
    iphi_s = 4 * iring_s + 1 - (ip_s - 2 * iring_s * (iring_s - 1))
    theta_s = np.arccos(np.clip(-1.0 + iring_s * iring_s / fact2, -1.0, 1.0))
    phi_s = (iphi_s - 0.5) * np.pi / (2.0 * iring_s)
    theta = np.where(south, theta_s, theta)
    phi = np.where(south, phi_s, phi)
    return theta, phi


# ── generic entry points ────────────────────────────────────────────
def ang2pix(nside: int, theta, phi, nest: bool = True) -> np.ndarray:
    return ang2pix_nest(nside, theta, phi) if nest else ang2pix_ring(nside, theta, phi)


def pix2ang(nside: int, ipix, nest: bool = True):
    return pix2ang_nest(nside, ipix) if nest else pix2ang_ring(nside, ipix)


def nest2ring(nside: int, ipix) -> np.ndarray:
    """Convert NESTED pixel numbers to RING via pixel centres.

    A pixel centre always lies inside its own pixel, so applying the other
    scheme's ``ang2pix`` to the centre is exact for centres (and therefore for
    the pixel identity).  This is slower than a closed-form conversion but is
    simple, vectorised, and easy to verify against the reference library.
    """
    theta, phi = pix2ang_nest(nside, ipix)
    return ang2pix_ring(nside, theta, phi)


def ring2nest(nside: int, ipix) -> np.ndarray:
    theta, phi = pix2ang_ring(nside, ipix)
    return ang2pix_nest(nside, theta, phi)


# ── vector helpers ──────────────────────────────────────────────────
def pix2vec_nest(nside: int, ipix) -> np.ndarray:
    """Return unit vectors (N, 3) for NESTED pixel centres."""
    theta, phi = pix2ang_nest(nside, ipix)
    return np.stack([np.sin(theta) * np.cos(phi),
                     np.sin(theta) * np.sin(phi),
                     np.cos(theta)], axis=-1)


def vec2pix_nest(nside: int, vec) -> np.ndarray:
    vec = np.asarray(vec, dtype=np.float64)
    x, y, z = vec[..., 0], vec[..., 1], vec[..., 2]
    norm = np.sqrt(x * x + y * y + z * z)
    theta = np.arccos(np.clip(z / norm, -1.0, 1.0))
    phi = np.mod(np.arctan2(y, x), 2.0 * np.pi)
    return ang2pix_nest(nside, theta, phi)


# ── NESTED hierarchy ────────────────────────────────────────────────
def nested_parent(ipix, levels: int = 1) -> np.ndarray:
    """Parent pixel ``levels`` orders above ``ipix`` (NESTED)."""
    levels = int(levels)
    if levels < 0:
        raise ValueError("levels must be non-negative")
    ipix = np.asarray(ipix, dtype=np.int64)
    return ipix >> (2 * levels)


def nested_children(ipix, levels: int = 1) -> np.ndarray:
    """All descendants ``levels`` orders below ``ipix`` (NESTED).

    Shape is ``(..., 4**levels)``.  The four children of a pixel at order
    ``o`` are ``4*ipix + k`` for k in 0..3, which follows directly from the
    face-local Morton index and holds across face boundaries.
    """
    levels = int(levels)
    if levels < 0:
        raise ValueError("levels must be non-negative")
    ipix = np.asarray(ipix, dtype=np.int64)
    nchild = 4 ** levels
    base = ipix * nchild
    return base[..., None] + np.arange(nchild, dtype=np.int64)


def nested_children_range(ipix, levels: int = 1) -> tuple[np.ndarray, np.ndarray]:
    """Return (start, stop) ranges of descendants in NESTED order."""
    levels = int(levels)
    if levels < 0:
        raise ValueError("levels must be non-negative")
    ipix = np.asarray(ipix, dtype=np.int64)
    nchild = 4 ** levels
    start = ipix * nchild
    return start, start + nchild


# ── geometry ────────────────────────────────────────────────────────
def angular_distance_deg(ra1, dec1, ra2, dec2) -> np.ndarray:
    """Great-circle distance in degrees (haversine, broadcasting)."""
    ra1 = np.radians(np.asarray(ra1, dtype=np.float64))
    dec1 = np.radians(np.asarray(dec1, dtype=np.float64))
    ra2 = np.radians(np.asarray(ra2, dtype=np.float64))
    dec2 = np.radians(np.asarray(dec2, dtype=np.float64))
    dlon = ra2 - ra1
    dlat = dec2 - dec1
    a = (np.sin(dlat / 2.0) ** 2
         + np.cos(dec1) * np.cos(dec2) * np.sin(dlon / 2.0) ** 2)
    return np.degrees(2.0 * np.arcsin(np.sqrt(np.clip(a, 0.0, 1.0))))


def disc_candidates(ra: float, dec: float, radius_deg: float,
                    tile_ra, tile_dec, tile_radius_deg) -> np.ndarray:
    """Indices of tiles whose bounding disc intersects a query disc.

    This is the broad phase used by the tile store: it is a superset of the
    tiles that can contain sources inside the query disc.  The caller applies
    the exact per-source filter afterwards.
    """
    sep = angular_distance_deg(ra, dec, np.asarray(tile_ra), np.asarray(tile_dec))
    return np.where(sep <= float(radius_deg) + np.asarray(tile_radius_deg))[0]


def query_disc_candidates(nside: int, ra: float, dec: float,
                          radius_deg: float, pixels=None) -> np.ndarray:
    """Sparse-table broad phase: pixels whose centres may touch the disc.

    Adds the pixel centre-to-boundary radius so a source inside the disc is
    never missed by the sparse ipix offsets.  The caller filters exactly by
    source RA/Dec afterwards.
    """
    if pixels is None:
        pixels = np.arange(nside2npix(nside), dtype=np.int64)
    else:
        pixels = np.asarray(pixels, dtype=np.int64)
    theta, phi = pix2ang(nside, pixels, nest=True)
    pix_dec = 90.0 - np.degrees(theta)
    pix_ra = np.degrees(phi)
    sep = angular_distance_deg(ra, dec, pix_ra, pix_dec)
    return pixels[sep <= float(radius_deg) + max_tile_radius_deg(nside)]


def query_disc_centers(nside: int, ra: float, dec: float, radius_deg: float,
                       nest: bool = True) -> np.ndarray:
    """Reference query: pixels whose *centres* lie inside the disc.

    This is an O(npix) brute-force implementation used for tests and for
    small nside.  It intentionally follows the ``healpy.query_disc`` centre
    convention; the production query works at tile level and then filters
    sources exactly.
    """
    npix = nside2npix(nside)
    theta, phi = pix2ang(nside, np.arange(npix), nest=nest)
    pix_dec = 90.0 - np.degrees(theta)
    pix_ra = np.degrees(phi)
    sep = angular_distance_deg(ra, dec, pix_ra, pix_dec)
    return np.where(sep <= float(radius_deg))[0]
