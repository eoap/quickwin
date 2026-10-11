"""Validate real transpiler-mate OCI metadata for both standalone documents."""
from pathlib import Path
import subprocess,json
for relative, entry, kind in [('cwl-cli/detect-water-body.cwl','detect-water-body','CommandLineTool'),('cwl-workflow/app-water-body-cloud-native.cwl','main','Workflow')]:
    target = Path('/tmp') / (Path(relative).stem + '.annotations.json')
    subprocess.run(['transpiler-mate','cwl2oci','--image-source','https://github.com/eoap/quickwin','--image-revision',subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'--output',str(target),relative+'#'+entry],check=True)
    data=json.loads(target.read_text())['$manifest']
    assert data['org.opencontainers.image.version']=='2.0.0'
    assert data['org.cwl.spec']=='v1.2' and data['org.cwl.type']==kind
    assert data['org.cwl.entrypoint'].split('#')[-1]==entry
    print(f'Accepted transpiler-mate metadata: {relative}')
