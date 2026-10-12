#!/bin/bash
set -euo pipefail
workspace=${QUICKWIN_WORKSPACE:-/workspace/quickwin}
cwltool --podman --outdir "$workspace/runs/workflow" "$workspace/cwl-workflow/app-water-body-cloud-native.cwl" "$workspace/cwl-workflow/params.yaml"
