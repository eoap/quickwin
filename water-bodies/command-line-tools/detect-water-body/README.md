# Water-body detection processing

Install the wheel and run `detect-water-body --help`. Existing CWL can still run
`python -m app`. The CLI reads a STAC Item or staged catalog, crops two common
bands in the specified AOI CRS, computes NDWI and Otsu, and writes a GeoTIFF
plus a self-contained STAC catalog. Use an explicit CRS such as `EPSG:4326`.

Run `hatch run dev:check` and `hatch run test:test` with Python 3.12. Runtime and
development dependencies are hash-locked under `requirements/`.
