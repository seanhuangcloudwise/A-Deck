"""Examine where shadows are defined in the purple master PPTX."""
import zipfile
from lxml import etree

MASTER = '/Volumes/work/Workspace/A-Deck/skills/pptx/master-library/light-cloudwise-purple/cloudwise-master.pptx'
DML = 'http://schemas.openxmlformats.org/drawingml/2006/main'

with zipfile.ZipFile(MASTER) as z:
    # Check all XML parts for effect-related content
    xml_parts = [n for n in z.namelist() if n.endswith('.xml')]
    for part in xml_parts:
        data = z.read(part)
        root = etree.fromstring(data)
        # Find effectLst with content
        for el in root.iter(f'{{{DML}}}effectLst'):
            children = list(el)
            if children:
                print(f'\n{part} > effectLst has {len(children)} children:')
                print(etree.tostring(el, pretty_print=True).decode()[:600])
        # Find sp3d (bevel/3D that can produce shadow-like effects)
        for el in root.iter(f'{{{DML}}}sp3d'):
            print(f'\n{part} > sp3d: {etree.tostring(el).decode()[:300]}')
        # Find effStyleRef (style reference producing effects)
        for el in root.iter(f'{{{DML}}}effectRef'):
            idx = el.get('idx', '0')
            if idx != '0':
                print(f'\n{part} > effectRef idx={idx} (non-zero = has effect)')

print('\nDone.')
