"""Tests for interacting with color interpretation."""


import os

import pytest

import rasterio
from rasterio.enums import ColorInterp


def test_cmyk_interp(tmpdir):
    """A CMYK TIFF has cyan, magenta, yellow, black bands."""
    with rasterio.open('tests/data/RGB.byte.tif') as src:
        meta = src.meta
    meta['photometric'] = 'CMYK'
    meta['count'] = 4
    tiffname = str(tmpdir.join('foo.tif'))
    with rasterio.open(tiffname, 'w', **meta) as dst:
        assert dst.profile['photometric'] == 'cmyk'
        assert dst.colorinterp(1) == ColorInterp.cyan
        assert dst.colorinterp(2) == ColorInterp.magenta
        assert dst.colorinterp(3) == ColorInterp.yellow
        assert dst.colorinterp(4) == ColorInterp.black


@pytest.mark.skipif(
    os.environ.get('TRAVIS', os.environ.get('CI', 'false')).lower() != 'true',
    reason="Crashing on OS X with Homebrew's GDAL")
def test_ycbcr_interp(tmpdir):
    """A YCbCr TIFF has red, green, blue bands."""
    with rasterio.open('tests/data/RGB.byte.tif') as src:
        meta = src.meta
    meta['photometric'] = 'ycbcr'
    meta['compress'] = 'jpeg'
    meta['count'] = 3
    tiffname = str(tmpdir.join('foo.tif'))
    with rasterio.open(tiffname, 'w', **meta) as dst:
        assert dst.colorinterp(1) == ColorInterp.red
        assert dst.colorinterp(2) == ColorInterp.green
        assert dst.colorinterp(3) == ColorInterp.blue


@pytest.mark.parametrize("dtype", [rasterio.ubyte, rasterio.int16])
def test_set_colorinterp(path_rgba_byte_tif, tmpdir, dtype):

    """Test setting color interpretation by creating an image without CI
    and then setting to unusual values.  Also test with a non-uint8 image.
    """

    no_ci_path = str(tmpdir.join('no-ci.tif'))
    with rasterio.open(path_rgba_byte_tif) as src:
        meta = src.meta.copy()
        meta.update(
            height=10,
            width=10,
            dtype=dtype,
            photometric='minisblack',
            alpha='unspecified')
    with rasterio.open(no_ci_path, 'w', **meta):
        pass

    # This is should be the default color interpretation of the copied
    # image.  GDAL defines these defaults, not Rasterio.
    src_ci_map = {
        1: ColorInterp.gray,
        2: ColorInterp.undefined,
        3: ColorInterp.undefined,
        4: ColorInterp.undefined
    }

    dst_ci_map = {
        1: ColorInterp.alpha,
        2: ColorInterp.blue,
        3: ColorInterp.green,
        4: ColorInterp.red
    }
    with rasterio.open(no_ci_path, 'r+') as src:
        for bidx, ci in src_ci_map.items():
            assert src.colorinterp(bidx) == ci
        for bidx, ci in dst_ci_map.items():
            src.set_colorinterp(bidx, ci)
        for bidx, ci in dst_ci_map.items():
            assert src.colorinterp(bidx) == ci
