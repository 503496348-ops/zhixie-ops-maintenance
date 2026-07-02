## 44. 审计脚本read_file行号导致frontmatter和章节标题误判（2026-06-24）

**问题**：对无限循环(Neverend)做质量审计时，SKILL.md frontmatter检查和`## 工作流`章节检查均报失败，但实际文件内容正确（从零clone验证`head -5 SKILL.md`确认以`---`开头，`grep '## 工作流'`确认存在）。

**根因**：审计脚本用`read_file(path)`读取SKILL.md，返回内容每行带`N|`前缀（如`1|---`、`74|## 工作流`）。v3严格模式的检查：
- `content.strip().startswith("---")` → 实际是`1|---` → 失败
- `re.search(r'^## 工作流', content, re.M)` → 实际是`74|## 工作流` → 失败

**修复**：审计脚本读取文件后必须先strip行号前缀：
```python
import re

def strip_line_numbers(content: str) -> str:
    """Strip read_file line-number prefixes before regex checks."""
    lines = content.split('\n')
    return '\n'.join(re.sub(r'^\d+\|', '', line) for line in lines)

# 读取后立即strip
raw = read_file(path)['content']
content = strip_line_numbers(raw)

# 然后才能做正则检测
has_frontmatter = content.strip().startswith("---")
has_workflow = bool(re.search(r'^## 工作流', content, re.M))
```

**同理影响**：has_triggers、has_technical、is_readme_style——所有基于正则的结构检测。

**铁律**：审计脚本任何基于`read_file`输出的正则匹配，必须先strip行号前缀。或改用`terminal('cat file')`读取原始内容。

## 45. 新产品上线流程检查清单（2026-06-24）

**场景**：从零创建第24款产品"无限循环 Neverend"，发现多处注册遗漏。

**完整检查清单**：
1. ✅ 创建GitHub仓库 + 推送代码
2. ✅ SKILL.md（frontmatter + triggers + 工作流 + 技术参考 + Pitfalls）
3. ✅ README.md（安装 + 使用 + FAQ + 架构 + 技术栈）
4. ⚠️ **更新`references/product-list.md`**——添加产品行 + 更新总数 + 更新日期
5. ⚠️ **更新`references/competitors.md`**——如果涉及新分类，添加竞品行
6. ⚠️ **审计品牌引用**——扫描所有.md/.py文件中的第三方仓库名/原作者名/Stars引用
7. ⚠️ **质量审计**——跑审计评分，B级及以下必须补强到A级再上线
8. ⚠️ **从零clone验证**——push后必须重新clone验证内容

**常见遗漏**：
- 忘记更新product-list.md的总数（23→24）
- 忘记在competitors.md添加新分类的竞品
- README.md致谢/技术栈中引用了竞品仓库链接
- .env.example中的密码占位符被审计标记为模板残留

**铁律**：新产品上线必须过7步检查清单。漏一步 = 数据不一致 = 下次日报/审计出错。
