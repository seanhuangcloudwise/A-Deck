"""Fix shadow removal — target the correct effectStyleLst tag name.

The theme XML uses <a:effectStyleLst> (not effectStyleList), and our
previous script correctly used that. But let's verify and brute-force
clear all outerShdw in every theme file inside the master PPTX.
"""
import zipfile, io, shutil
from lxml import etree

MASTER = '/Volumes/work/Workspace/A-Deck/skills/pptx/master-library/light-cloudwise-purple/cloudwise-master.pptx'
DML = 'http://schemas.openxmlformats.org/drawingml/2006/main'

SHADOW_TAGS = {
    f'{{{DML}}}outerShdw',
    f'{{{DML}}}innerShdw',
    f'{{{DML}}}prstShdw',
    f'{{{DML}}}reflection',
    f'{{{DML}}}glow',
    f'{{{DML}}}softEdge',
}

def clear_all_effects(xml_bytes, part_name):
    root = etree.fromstring(xml_bytes)
    removed = 0
    # Remove any shadow/effect children from ANY effectLst in the document
    for lst in root.iter(f'{{{DML}}}effectLst'):
        for child in list(lst):
            if child.tag in SHADOW_TAGS:
                lst.remove(child)
                removed += 1
                print(f'  Removed {child.tag.split("}")[-1]} from {part_name}')
    return etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True), removed

# First inspect what's in master
print('=== Master PPTX theme inspection ===')
with zipfile.ZipFile(MASTER) as z:
    all_parts = z.namelist()
    xml_parts = [n for n in all_parts if n.endswith('.xml')]
    print(f'Total XML parts: {len(xml_parts)}')
    for part in xml_parts:
        root = etree.fromstring(z.read(part))
        for lst in root.iter(f'{{{DML}}}effectLst'):
            children = list(lst)
            if children:
                print(f'  {part}: effectLst with {len(children)} children: {[c.tag.split("}")[-1] for c in children]}')

print('\n=== Applying fixes ===')
total = 0
with zipfile.ZipFile(MASTER, 'r') as zin:
    names = zin.namelist()
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as zout:
        for name in names:
            data = zin.read(name)
            if name.endswith('.xml'):
                new_data, n = clear_all_effects(data, name)
                total += n
                zout.writestr(name, new_data)
            else:
                zout.writestr(name, data)

with open(MASTER, 'wb') as f:
    f.write(buf.getvalue())

print(f'\nTotal removed: {total}')
print('Done.')
