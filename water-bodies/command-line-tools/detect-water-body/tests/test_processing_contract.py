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
