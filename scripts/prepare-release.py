"""Replace development image references with the accepted published digest."""
import argparse
from pathlib import Path
import yaml
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--image', required=True)
args = parser.parse_args()
assert args.image.startswith('ghcr.io/eoap/quickwin/detect-water-body@sha256:')
for path in Path('.').glob('cwl*/*.cwl'):
    doc = yaml.safe_load(path.read_text())
    for process in doc.get('$graph', [doc]):
        if process['class'] == 'CommandLineTool':
            for category in ('requirements', 'hints'):
                docker = process.get(category, {}).get('DockerRequirement')
                if docker: docker['dockerPull'] = args.image
    path.write_text(yaml.safe_dump(doc, sort_keys=False))
