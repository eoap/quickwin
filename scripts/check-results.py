"""Verify real Lake Almanor outputs from all four Quickwin notebooks."""
from pathlib import Path
import numpy as np
import pystac
import rasterio
from rasterio.warp import transform_bounds
root = Path(__file__).resolve().parents[1]
for directory in (root / 'practice-labs', root / 'runs', root / 'runs/cwl-cli', root / 'runs/cwl-workflow'):
    catalog = pystac.Catalog.from_file(str(directory / 'catalog.json'))
    items = list(catalog.get_all_items())
    assert items, f'Empty catalog: {directory}'
    for item in items:
        for asset in item.assets.values():
            with rasterio.open(asset.get_absolute_href()) as src:
                assert src.crs and src.width > 0 and src.height > 0
                west, south, east, north = transform_bounds(src.crs, 'EPSG:4326', *src.bounds)
                assert west < -120.74 and east > -121.399 and south < 40.472 and north > 39.834, src.bounds
                values = np.unique(src.read(1))
                assert set(values).issubset({0, 1}) and len(values) == 2, values
            print(f'Accepted real georeferenced water mask: {asset.get_absolute_href()}')
