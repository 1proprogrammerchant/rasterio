from rasterio.io import WarpWrapper


def test_wrap_file():
    """A warp wrapper's dataset has the expected properties"""
    with WarpWrapper('tests/data/RGB.byte.tif', dst_crs='EPSG:3857') as warped:
        with warped.open() as dataset:
            assert dataset.crs == 'EPSG:3857'
            assert tuple(round(x, 1) for x in dataset.bounds) == (
                -8789636.7, 2700460.0, -8524406.4, 2943560.2)
            assert dataset.name == 'tests/data/RGB.byte.tif'
            assert dataset.indexes == (1, 2, 3)
            assert dataset.nodatavals == (0, 0, 0)
            assert dataset.dtypes == ('uint8', 'uint8', 'uint8')
            assert dataset.read().shape == (3, 736, 803)


def test_wrap_s3():
    """A warp wrapper's dataset has the expected properties"""
    L8TIF = "s3://landsat-pds/L8/139/045/LC81390452014295LGN00/LC81390452014295LGN00_B1.TIF"
    with WarpWrapper(L8TIF, dst_crs='EPSG:3857') as warped:
        with warped.open() as dataset:
            assert dataset.crs == 'EPSG:3857'
            assert tuple(round(x, 1) for x in dataset.bounds) == (
                9556764.6, 2345109.3, 9804595.9, 2598509.1)
            assert dataset.name == 's3://landsat-pds/L8/139/045/LC81390452014295LGN00/LC81390452014295LGN00_B1.TIF'
            assert dataset.indexes == (1,)
            assert dataset.nodatavals == (None,)
            assert dataset.dtypes == ('uint16',)
            assert dataset.shape == (7827, 7655)
