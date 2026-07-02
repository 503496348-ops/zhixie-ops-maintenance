# 智械工坊-OPS维护

智械工坊产品矩阵的 OPS 维护技能包：产品仓库日报、竞品监控、产品质量审计、Cron/no_agent 运维、夜间只读审计与融合候选分诊。

## 组件

- `SKILL.md` — Hermes Skill 主入口，旧名 `product-repo-monitor` 已保留为历史关键词。
- `scripts/product-repo-card.py` — 产品仓库日报卡片生成与 dry-run。
- `scripts/competitor-monitor.py` — 竞品仓库监控，输出 schema-v2 快照。
- `scripts/audit-products.py` — 产品只读审计，输出 `audit-report.json`。
- `references/` — 产品清单、竞品清单、质量评分、cron 门禁、发布门禁与 OPS runbook。
- `tests/validate_package.py` — 包结构、脚本编译与敏感信息扫描。

## 快速验证

```bash
python3 -m py_compile scripts/*.py
python3 tests/validate_package.py
PRODUCT_MONITOR_DRY_RUN=1 python3 scripts/product-repo-card.py --dry-run
python3 scripts/competitor-monitor.py
python3 scripts/audit-products.py
```

## 安全边界

发布版不包含任何真实 Feishu/Lark/Bitable 租户标识、webhook、API key、chat id、base token 或 table id。需要部署到真实环境时，通过环境变量和本地 Hermes profile 提供凭据。

监控类 cron 推荐 `no_agent=true + script`，避免 LLM 二次改写数字或消耗 provider token。
