# Post-Push 验证清单

每次修改产品仓库后必须执行以下验证，缺一环=未完成。

## 1. Push前检查

- [ ] `git branch -r` 确认远程默认分支名（main vs master）
- [ ] product-list.md中的分支名与实际一致
- [ ] SKILL.md无行号前缀（`^\d+\|`）
- [ ] commit message不含敏感词（清除/清理/原作者）

## 2. Push后验证（从零clone）

```python
import subprocess, os, tempfile, re
from pathlib import Path

tmpdir = tempfile.mkdtemp()
dest = os.path.join(tmpdir, repo_name)
subprocess.run(['git','clone','--depth','1',
    f'https://github.com/{org}/{repo}.git', dest], timeout=30)

content = Path(os.path.join(dest, 'SKILL.md')).read_text()
```

## 3. 六项内容检查

| # | 检查项 | 正则/方法 | 通过条件 |
|---|--------|----------|---------|
| 1 | frontmatter | `content.strip().startswith('---')` | ✅ |
| 2 | triggers | `'triggers:' in content` | ✅ |
| 3 | 工作流章节 | `re.search(r'^## 工作流\|## Workflow', content, re.M)` | ✅ |
| 4 | 技术架构章节 | `re.search(r'^## 技术架构\|## Technical', content, re.M)` | ✅ |
| 5 | 无行号前缀 | `not re.search(r'^\d+\|', content, re.M)` | ✅ |
| 6 | references | `re.search(r'references/\|📖', content)` | 建议有 |

## 4. 代码验证

```python
code_files = []
total_lines = 0
for root, dirs, files in os.walk(dest):
    dirs[:] = [d for d in dirs if d != '.git']
    for f in files:
        if f.endswith(('.py','.ts','.js','.go','.rs','.java')):
            lines = len(Path(os.path.join(root,f)).read_text(errors='ignore').split('\n'))
            code_files.append(f)
            total_lines += lines

print(f"代码: {len(code_files)}文件, {total_lines}行")
```

## 5. Git log验证

```bash
curl -s "https://api.github.com/repos/{org}/{repo}/commits?per_page=1" | \
  python3 -c "import sys,json; d=json.load(sys.stdin); print(d[0]['commit']['message'][:80])"
```

确认最新commit是你的修复commit，不是旧commit。

## 常见失败模式

| 症状 | 根因 | 修复 |
|------|------|------|
| push成功但clone后无变化 | 推到了错误分支（master vs main） | `git push origin HEAD:{correct_branch} --force` |
| SKILL.md有`1\|---` | read_file行号写入 | strip行号后重新push |
| 审计显示A但手动验证有缺 | 审计用关键词匹配太宽松 | 更新审计脚本为严格模式 |
| 审计clone到旧内容 | product-list.md分支名错误 | 修正product-list.md |
| 评分显示8.0但等级为B | 浮点精度（7.95→round=8.0） | 先round再判定等级 |
