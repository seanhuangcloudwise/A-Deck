"""Remove shadow/glow effects from light-cloudwise-purple master PPTX."""
import zipfile, io, shutil
from lxml import etree

MASTER = '/Volumes/work/Workspace/A-Deck/skills/pptx/master-library/light-cloudwise-purple/cloudwise-master.pptx'
BACKUP = MASTER + '.shadow-bak'
DML = 'http://schemas.openxmlformats.org/drawingml/2006/main'

SHADOW_TAGS = {
    f'{{{DML}}}outerShdw',
    f'{{{DML}}}innerShdw',
    f'{{{DML}}}prstShdw',
    f'{{{DML}}}glow',
    f'{{{DML}}}reflection',
    f'{{{DML}}}softEdge',
}


def strip_effects(xml_bytes):
    root = etree.fromstring(xml_bytes)
    removed = 0
    # 1. Remove shadow children from all effectLst elements
    for lst in root.iter(f'{{{DML}}}effectLst'):
        for child in list(lst):
            if child.tag in SHADOW_TAGS:
                lst.remove(child)
                removed += 1
    # 2. In theme fmtScheme effectStyleList: clear all effect styles
    for style in root.iter(f'{{{DML}}}effectStyle'):
        lst = style.find(f'{{{DML}}}effectLst')
        if lst is not None:
            for child in list(lst):
                if child.tag in SHADOW_TAGS:
                    lst.remove(child)
                    removed += 1
    return (etree.tostring(root, xml_declaration=True,
                           encoding='UTF-8', standalone=True),
            removed)


shutil.copy2(MASTER, BACKUP)
print(f'Backup created: {BACKUP}')

total = 0
with zipfile.ZipFile(MASTER, 'r') as zin:
    names = zin.namelist()
    targets = [n for n in names
               if any(k in n for k in ('theme', 'slideMaster', 'slideLayout'))
               and n.endswith('.xml')]
    print(f'Scanning {len(targets)} XML parts in master PPTX...')

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as zout:
        for name in names:
            data = zin.read(name)
            if name in targets:
                new_data, n = strip_effects(data)
                if n:
                    print(f'  {name}: removed {n} effect element(s)')
                    total += n
                zout.writestr(name, new_data)
            else:
                zout.writestr(name, data)

with open(MASTER, 'wb') as f:
    f.write(buf.getvalue())

print(f'\nTotal elements removed: {total}')
print('Master PPTX saved.')
