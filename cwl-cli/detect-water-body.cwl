cwlVersion: v1.2
class: CommandLineTool
id: detect-water-body
requirements:
  EnvVarRequirement:
    envDef:
      PYTHONPATH: /app
  ResourceRequirement:
    coresMax: 1
    ramMax: 512
  DockerRequirement:
    dockerPull: localhost/detect-water-body:latest
  SchemaDefRequirement:
    types:
    - name: '#URI'
      type: record
      fields:
      - name: value
        type: string
        doc: Absolute STAC Item URL.
    - name: '#BBox'
      type: record
      fields:
      - name: west
        type: double
        doc: Western longitude.
      - name: south
        type: double
        doc: Southern latitude.
      - name: east
        type: double
        doc: Eastern longitude.
      - name: north
        type: double
        doc: Northern latitude.
    - name: '#CRS'
      type: enum
      symbols:
      - EPSG:4326
    - name: '#Band'
      type: enum
      symbols:
      - green
      - nir
  InlineJavascriptRequirement: {}
baseCommand:
- python
- -m
- app
arguments: []
inputs:
  item:
    type: URI
    inputBinding:
      prefix: --input-item
      valueFrom: $(self.value)
    label: item
    doc: STAC Item URL.
  aoi:
    type: BBox
    inputBinding:
      prefix: --aoi
      valueFrom: $( [self.west,self.south,self.east,self.north].join(",") )
    label: aoi
    doc: Geographic bounding box in the input CRS.
  epsg:
    type: CRS
    inputBinding:
      prefix: --epsg
    label: epsg
    doc: Coordinate reference system of the bounding box.
  band:
    type:
      type: array
      items: Band
      inputBinding:
        prefix: --band
    label: band
    doc: Green and near-infrared bands in NDWI order.
outputs:
  water-body:
    outputBinding:
      glob: .
    type: Directory
    label: STAC catalog
    doc: Self-contained STAC catalog and georeferenced water mask.
$namespaces:
  s: https://schema.org/
  EPSG: http://www.opengis.net/def/crs/EPSG/0/
s:softwareVersion: 2.0.0
s:codeRepository: https://github.com/eoap/quickwin
s:license: https://spdx.org/licenses/CC-BY-NC-SA-4.0
s:author:
- class: s:Person
  s:name: Parham Membari
  s:email: parham.membari@terradue.com
label: Water body detection
doc: Detect water around Lake Almanor using Sentinel-2 green and near-infrared bands,
  NDWI and Otsu thresholding.
