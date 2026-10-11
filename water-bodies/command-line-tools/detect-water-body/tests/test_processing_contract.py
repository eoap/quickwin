"""Unit fixtures for error handling and scientific array semantics, not EO acceptance data."""

from datetime import UTC, datetime

import numpy as np
import pystac
from click.testing import CliRunner

from detect_water_body.main import main, normalized_difference, read_item, threshold


def test_missing_band_is_reported_before_dereferencing_asset(tmp_path):
    item = pystac.Item("missing-band", None, None, datetime(2021, 1, 1, tzinfo=UTC), {})
    path = tmp_path / "item.json"
    item.save_object(dest_href=str(path))
    result = CliRunner().invoke(
        main,
        [
            "--input-item",
            str(path),
            "--aoi",
            "-121.4,39.8,-120.7,40.5",
            "--epsg",
            "EPSG:4326",
            "--band",
            "green",
            "--band",
            "nir",
        ],
    )
    assert result.exit_code != 0
    assert isinstance(result.exception, ValueError)
    assert "Common band name green not found" in str(result.exception)


def test_staged_catalog_yields_actual_stac_item(tmp_path):
    catalog = pystac.Catalog("input", "staged unit fixture")
    item = pystac.Item("scene", None, None, datetime(2021, 1, 1, tzinfo=UTC), {})
    catalog.add_item(item)
    catalog.normalize_and_save(str(tmp_path), pystac.CatalogType.SELF_CONTAINED)
    assert read_item(str(tmp_path)).id == "scene"


def test_ndwi_and_threshold_ignore_nonfinite_values():
    green = np.array([1, 1, 9, 9, 0], dtype=np.float32)
    nir = np.array([9, 9, 1, 1, 0], dtype=np.float32)
    ndwi = normalized_difference(green, nir)
    np.testing.assert_allclose(ndwi[:4], [-0.8, -0.8, 0.8, 0.8])
    assert np.isnan(ndwi[4])
    np.testing.assert_array_equal(threshold(ndwi), [False, False, True, True, False])


def test_crop_preserves_pixels_and_spatial_transform(tmp_path):
    import rasterio
    from rasterio.transform import from_origin

    from detect_water_body.main import crop

    # Synthetic raster is only a unit fixture, never notebook acceptance input.
    pixels = np.arange(256, dtype=np.uint16).reshape(16, 16)
    source = tmp_path / "crop-unit.tif"
    with rasterio.open(
        source,
        "w",
        driver="GTiff",
        height=16,
        width=16,
        count=1,
        dtype="uint16",
        crs="EPSG:4326",
        transform=from_origin(0, 16, 1, 1),
    ) as dataset:
        dataset.write(pixels, 1)
    cropped, metadata = crop(pystac.Asset(str(source)), [2, 4, 10, 12], "EPSG:4326")
    np.testing.assert_array_equal(cropped[0], pixels[4:12, 2:10])
    assert cropped.dtype == np.float32
    assert metadata["transform"] == from_origin(2, 12, 1, 1)
    assert metadata["width"] == metadata["height"] == 8
