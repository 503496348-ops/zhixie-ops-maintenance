#!/usr/bin/env python3
from pathlib import Path
import re, py_compile, sys
root = Path(__file__).resolve().parents[1]
required = [
    'SKILL.md', 'README.md',
    'scripts/product-repo-card.py', 'scripts/competitor-monitor.py', 'scripts/audit-products.py',
    'references/product-list.md', 'references/competitors.md',
    'references/local-fusion-map.md', 'references/ops-maintenance-runbook.md',
    'references/repository-release-checklist.md',
]
missing = [p for p in required if not (root/p).exists()]
if missing:
    raise SystemExit(f'missing required files: {missing}')
skill=(root/'SKILL.md').read_text(encoding='utf-8')
assert 'name: zhixie-ops-maintenance' in skill
assert '智械工坊-OPS维护' in skill
assert 'version: "6.1"' in skill
for script in (root/'scripts').glob('*.py'):
    py_compile.compile(str(script), doraise=True)
patterns = [
    r'ghp_[A-Za-z0-9]{20,}', r'sk-[A-Za-z0-9_-]{20,}', r'oc_[0-9a-fA-F]{20,}',
    'DB3H' + 'bJuFDaygPmsQ0A4carfynMd', 'tblO' + 'PRO5zVx0yCdn', r'link_token=[A-Za-z0-9_-]+'
]
violations=[]
for p in root.rglob('*'):
    if p.is_file() and p.suffix.lower() in {'.md','.py','.json','.txt','.yml','.yaml'} and '.git' not in p.parts:
        s=p.read_text(encoding='utf-8', errors='ignore')
        for pat in patterns:
            if re.search(pat, s): violations.append(f'{p.relative_to(root)}:{pat}')
if violations:
    raise SystemExit('sensitive pattern violations:\n'+'\n'.join(violations))
if re.search(r'^\d+\|', skill, re.M):
    raise SystemExit('line-number pollution in SKILL.md')
print('validate_package: PASS')
