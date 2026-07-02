# 仓库发布门禁

## 发布前

- `python3 -m py_compile scripts/*.py`
- 产品日报 dry-run：确认产品数、仓库数、星标数、send_status。
- 竞品日报：确认分类数、唯一仓库数、成功检查数、错误数、schema_version。
- 产品审计：确认 total_products 与 product-list.md 一致。
- `grep -RInE` 扫描 API key、token、webhook、Feishu/Lark/Bitable 连接标识。
- 检查 `^[0-9]+\|` 行号污染、重复 frontmatter、重复章节。

## 发布后远端复验

```bash
rm -rf /tmp/verify-zhixie-ops-maintenance
git clone https://github.com/503496348-ops/zhixie-ops-maintenance /tmp/verify-zhixie-ops-maintenance
cd /tmp/verify-zhixie-ops-maintenance
python3 -m py_compile scripts/*.py
python3 tests/validate_package.py
git status --short
```

验收报告必须包含远端 commit SHA、脚本编译、包结构、敏感信息扫描和 dry-run/审计/竞品输出摘要。
