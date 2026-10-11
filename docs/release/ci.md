# Acceptance and publication

Every feature push and pull request installs the hash-locked Python 3.12
notebook environment, validates both standalone CWL v1.2 documents, and checks
metadata using transpiler-mate in a separate locked environment. CI executes
all four notebooks with real Sentinel-2 data around Lake Almanor and retains
executed notebooks as acceptance evidence. Bash command failures stop acceptance.
The scientific check verifies each lesson's STAC catalog, readable GeoTIFF assets,
geographic intersection with the lake, and binary water-mask values.

The container lesson builds the repository Dockerfile, with an immutable Python
base image, the Rasterio system dependency and hash-locked Python requirements.
The CWL lessons use that locally built image. Matching typed input examples are
provided alongside each CWL document.

Stable publication requires a manual `publish: true` workflow dispatch on main.
Publication waits for acceptance, refuses existing release/image tags, builds
and pushes the processing image to GHCR, and replaces development image names
in both release CWL documents with the published digest. It validates those
modified documents before publishing the release bundle, individual CWL files,
typed input jobs, environment lock and SHA256 checksums. It does not pack CWL.

```yaml title=".github/workflows/build.yaml"
--8<--
.github/workflows/build.yaml
--8<--
```

The module's release history is on [GitHub](https://github.com/eoap/quickwin/releases).
The processing image is published under `ghcr.io/eoap/quickwin/detect-water-body`.
