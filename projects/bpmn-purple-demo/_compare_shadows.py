"""Check backup master vs current master and output PPTX themes."""
import zipfile
from lxml import etree

DML = 'http://schemas.openxmlformats.org/drawingml/2006/main'

def check_pptx_effects(path, label):
    print(f'\n=== {label} ===')
    print(f'File: {path}')
    with zipfile.ZipFile(path) as z:
        parts = z.namelist()
        theme_parts = [n for n in parts if n.endswith('.xml')]
        found = 0
        for part in theme_parts:
            root = etree.fromstring(z.read(part))
            for lst in root.iter(f'{{{DML}}}effectLst'):
                children = list(lst)
                if children:
                    tags = [c.tag.split('}')[-1] for c in children]
                    print(f'  {part}: {tags}')
                    found += 1
        if found == 0:
            print('  (no effectLst with children found)')
        # Also check effectRef usage
        for part in theme_parts:
            root = etree.fromstring(z.read(part))
            refs = {el.get('idx') for el in root.iter(f'{{{DML}}}effectRef')}
            nonzero = refs - {None, '0'}
            if nonzero:
                print(f'  {part}: effectRef nonzero={nonzero}')

MASTER = '/Volumes/work/Workspace/A-Deck/skills/pptx/master-library/light-cloudwise-purple/cloudwise-master.pptx'
BACKUP = MASTER + '.shadow-bak'
OUTPUT = '/Volumes/work/Workspace/A-Deck/projects/bpmn-purple-demo/bpmn-purple-demo.pptx'

check_pptx_effects(BACKUP, 'BACKUP (original master)')
check_pptx_effects(MASTER, 'CURRENT MASTER (after fix attempt)')
check_pptx_effects(OUTPUT, 'OUTPUT PPT (generated)')
