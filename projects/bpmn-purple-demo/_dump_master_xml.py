"""Dump raw master theme XML to find shadow source."""
import zipfile

MASTER = '/Volumes/work/Workspace/A-Deck/skills/pptx/master-library/light-cloudwise-purple/cloudwise-master.pptx'

with zipfile.ZipFile(MASTER) as z:
    parts = z.namelist()
    theme_parts = sorted(n for n in parts if 'theme' in n and n.endswith('.xml'))
    print(f'Theme parts in master ({len(theme_parts)}):')
    for t in theme_parts:
        content = z.read(t).decode('utf-8', errors='replace')
        # Check for shadow keywords
        shadow_count = content.count('outerShdw') + content.count('innerShdw') + content.count('reflection')
        effect_lst_count = content.count('effectLst')
        print(f'  {t}: outerShdw/reflection={shadow_count}, effectLst={effect_lst_count}')
        if shadow_count > 0:
            # Find the context
            idx = content.find('outerShdw')
            if idx >= 0:
                print(f'    Context: ...{content[max(0,idx-200):idx+300]}...')

    # Also check slideMaster for shapes with effectRef
    master_parts = sorted(n for n in parts if 'slideMaster' in n and n.endswith('.xml'))
    print(f'\nSlideMaster parts ({len(master_parts)}):')
    for m in master_parts:
        content = z.read(m).decode('utf-8')
        ref_count = content.count('effectRef')
        print(f'  {m}: effectRef={ref_count}')
        # Find non-zero effectRef
        import re
        matches = re.findall(r'effectRef[^>]*idx="([^"]+)"', content)
        nonzero = [m for m in matches if m != '0']
        if nonzero:
            print(f'    nonzero effectRef idx: {set(nonzero)}')
