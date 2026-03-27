"""Inspect generated PPTX for shadow effects on shapes."""
import zipfile
from lxml import etree

OUTPUT = '/Volumes/work/Workspace/A-Deck/projects/bpmn-purple-demo/bpmn-purple-demo.pptx'
DML = 'http://schemas.openxmlformats.org/drawingml/2006/main'
PML = 'http://schemas.openxmlformats.org/presentationml/2006/main'

shadow_tags = {
    f'{{{DML}}}outerShdw',
    f'{{{DML}}}innerShdw',
    f'{{{DML}}}prstShdw',
    f'{{{DML}}}glow',
}

found_any = False
with zipfile.ZipFile(OUTPUT) as z:
    slides = sorted(n for n in z.namelist() if n.startswith('ppt/slides/slide') and n.endswith('.xml'))
    # also check master
    masters = [n for n in z.namelist() if 'slideMaster' in n and n.endswith('.xml')]
    themes = [n for n in z.namelist() if 'theme' in n and n.endswith('.xml')]

    # Check theme effectStyleList
    for t in themes:
        root = etree.fromstring(z.read(t))
        for i, style in enumerate(root.iter(f'{{{DML}}}effectStyle')):
            lst = style.find(f'{{{DML}}}effectLst')
            if lst is not None:
                children = list(lst)
                print(f'Theme {t} effectStyle[{i}] children: {[c.tag.split("}")[-1] for c in children]}')

    # Check effRef idx in masters
    for m in masters:
        root = etree.fromstring(z.read(m))
        refs = [(el.get('idx'), el.getparent().tag) for el in root.iter(f'{{{DML}}}effectRef')]
        print(f'\nMaster effectRef indices: {set(r[0] for r in refs)}')

    # Check first couple slides for actual shadow elements
    for slide in slides[:3]:
        root = etree.fromstring(z.read(slide))
        n_shadows = 0
        for el in root.iter():
            if el.tag in shadow_tags:
                n_shadows += 1
                found_any = True
        # also check effectRef
        refs = [el.get('idx') for el in root.iter(f'{{{DML}}}effectRef')]
        nonzero = [r for r in refs if r and r != '0']
        print(f'{slide}: {n_shadows} direct shadows, effectRef nonzero: {set(nonzero)}')

if not found_any:
    print('\nNo direct shadow XML in slides. Shadows may come from effectRef->theme chain.')
    print('Checking theme effectStyleList content...')
    with zipfile.ZipFile(OUTPUT) as z:
        for t in themes:
            root = etree.fromstring(z.read(t))
            for lst in root.iter(f'{{{DML}}}effectStyleLst'):
                print(etree.tostring(lst, pretty_print=True).decode()[:2000])
