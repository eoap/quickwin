#!/bin/bash
set -euo pipefail
workspace=${QUICKWIN_WORKSPACE:-/workspace/quickwin}
cwltool --podman --outdir "$workspace/runs/cli" "$workspace/cwl-cli/detect-water-body.cwl" "$workspace/cwl-cli/params.yaml"
