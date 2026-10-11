cwlVersion: v1.2
$namespaces:
  s: https://schema.org/
s:softwareVersion: 2.0.0
$graph:
- class: Workflow
  id: main
  label: Water body detection
  doc: Detect water around Lake Almanor using Sentinel-2 green and near-infrared bands,
    NDWI and Otsu thresholding.
  requirements:
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
        - '4326'
      - name: '#Band'
        type: enum
        symbols:
        - green
        - nir
    InlineJavascriptRequirement: {}
  inputs:
    aoi:
      label: aoi
      doc: Geographic bounding box in the input CRS.
      type: BBox
    epsg:
      label: epsg
      doc: Quoted EPSG code ("4326") selecting geographic longitude/latitude coordinates.
      type: CRS
      default: '4326'
    bands:
      label: bands
      doc: Green and near-infrared bands in NDWI order.
      type:
        type: array
        items: Band
      default:
      - green
      - nir
    item:
      doc: STAC Item URL.
      label: item
      type: URI
  outputs:
  - id: stac_catalog
    outputSource:
    - node_detect/stac-catalog
    type: Directory
    label: STAC catalog
    doc: Self-contained STAC catalog and georeferenced water mask.
  steps:
    node_detect:
      run: '#detect-water-body'
      in:
        item: item
        aoi: aoi
        epsg: epsg
        band: bands
      out:
      - stac-catalog
- class: CommandLineTool
  id: detect-water-body
  requirements:
    InlineJavascriptRequirement: {}
    EnvVarRequirement:
      envDef:
        PYTHONPATH: /app
    ResourceRequirement:
      coresMax: 1
      ramMax: 512
    NetworkAccess:
      networkAccess: true
  hints:
    DockerRequirement:
      dockerPull: localhost/detect-water-body:latest
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
        valueFrom: $("EPSG:" + self)
      label: epsg
      doc: Quoted EPSG code ("4326") selecting geographic longitude/latitude coordinates.
    band:
      type:
        type: array
        items: Band
        inputBinding:
          prefix: --band
      label: band
      doc: Green and near-infrared bands in NDWI order.
  outputs:
    stac-catalog:
      outputBinding:
        glob: .
      type: Directory
      label: STAC catalog
      doc: Self-contained STAC catalog and georeferenced water mask.
  label: Water body detection
  doc: Detect water around Lake Almanor using Sentinel-2 green and near-infrared bands,
    NDWI and Otsu thresholding.
s:codeRepository: https://github.com/eoap/quickwin
s:license: https://spdx.org/licenses/CC-BY-NC-SA-4.0
s:author:
- '@type': s:Person
  s:givenName: Parham
  s:familyName: Membari
  s:name: Parham Membari
  s:email: parham.membari@terradue.com
  s:affiliation: &id001
    '@type': s:Organization
    s:name: Terradue
    s:url: https://www.terradue.com
s:name: Quickwin water body detection
s:description: Detect water around Lake Almanor using real Sentinel-2 COG assets,
  NDWI and Otsu thresholding.
s:dateCreated: '2022-09-01'
s:publisher: *id001
s:softwareHelp:
  '@type': s:CreativeWork
  s:name: Quickwin learning module
  s:url: https://eoap.github.io/quickwin/
