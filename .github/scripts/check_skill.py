#!/usr/bin/env python3
"""Validate the skill the way installers and agents read it: frontmatter, sizes and internal links."""
import glob, os, re, sys
import yaml

ROOT = os.path.join(os.path.dirname(__file__), '..', '..')
SKILL = os.path.join(ROOT, 'skills', 'motion-pilot')
errors = []

text = open(os.path.join(SKILL, 'SKILL.md'), encoding='utf-8').read()
m = re.match(r'^---\n(.*?)\n---\n', text, re.S)
if not m:
    errors.append('SKILL.md: missing YAML frontmatter')
else:
    meta = yaml.safe_load(m.group(1))
    name, desc = meta.get('name', ''), meta.get('description', '')
    if not re.fullmatch(r'[a-z0-9]+(-[a-z0-9]+)*', name or ''): errors.append(f'name {name!r}: lowercase letters, digits and hyphens only')
    if len(name) > 64: errors.append('name: over 64 characters')
    if name != os.path.basename(SKILL): errors.append(f'name {name!r} must match the folder name')
    if not desc: errors.append('description: missing')
    elif len(desc) > 1024: errors.append(f'description: {len(desc)} characters, the limit is 1024')
lines = text.count('\n')
if lines > 500: errors.append(f'SKILL.md: {lines} lines; keep it under 500 and move depth into references/')

# every backticked path inside the skill must exist
for f in [os.path.join(SKILL, 'SKILL.md')] + glob.glob(os.path.join(SKILL, 'references', '**', '*.md'), recursive=True):
    for p in re.findall(r'`((?:references/|scripts/|engine/|templates/|reference-implementations/|process/|craft/|genres/|taste/|tech/|brands/)[^`\s]*)`', open(f, encoding='utf-8').read()):
        p = p.rstrip('.,')
        if '<' in p or '*' in p: continue
        if not any(os.path.exists(os.path.join(SKILL, c)) or glob.glob(os.path.join(SKILL, c) + '*') for c in (p, 'references/' + p)):
            errors.append(f'{os.path.relpath(f, ROOT)}: missing path {p}')

if errors:
    print('\n'.join(errors)); sys.exit(1)
print(f'skill ok: {name}, description {len(desc)} characters, SKILL.md {lines} lines')
