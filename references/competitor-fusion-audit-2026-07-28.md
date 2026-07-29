# 竞品融合候选深审清单（2026-07-28）

- 审查：9 项
- 可融合：2；观察：2；无需融合：5

| 优先级 | 候选 | 结论 | 目标产品 | 核心判断 |
|---|---|---|---|---|
| P0 | `NVIDIA/SkillSpector` | 可融合 | `hermes-security-suite` | 2.5.0 新增执行核算、检查账本、抑制与报告闭环；现有 HSS 已有 SkillSpector bridge，但缺少逐检查 attempted/completed/skipped/suppressed 的完整性核算，直接影响“扫描成功”真值。 |
| P1 | `vrtmrz/obsidian-livesync` | 可融合 | `neverend` | LiveSync 1.0 合并带来 CLI/P2P compose smoke 与 harness CI。NeverEnd 已有快照比对和冲突检测，不应复制同步引擎；只提炼真实双端/P2P 故障注入与重连验收契约。 |
| P2 | `langgenius/dify` | 观察 | `hermes-doctor,pipixia-doctor` | 最新提交仅修复 MCP output_schema 可选字段兼容；hermes-doctor/pipixia-doctor 当前未发现 MCP/output_schema 接入点，先保留为未来协议兼容回归样例。 |
| P2 | `scrapy/scrapy` | 观察 | `energsolve` | 近期为缓存 DNS 端口与递归/媒体报告修复；对 EnergSolve 采集稳定性有间接参考，但未形成现有链路的可证缺口。 |
| N/A | `crewAIInc/crewAI` | 无需融合 | `barren-order` | WaitTool 是阻塞式等待工具；BarrenOrder 已具备持久化暂停/审批、恢复指纹、超时重试和工作流 resume，直接引入反而退化。 |
| N/A | `getzep/zep` | 无需融合 | `hermes-doctor,pipixia-doctor` | 最新核心变化是 Slack 作者 real_name 解析与评估文档，不对应 doctor 产品的上下文诊断缺口。 |
| N/A | `huggingface/diffusers` | 无需融合 | `ideasphere` | caption dropout 与 aspect ratio buckets 属于 LoRA 训练脚本增强；IdeaSphere 当前不是训练平台，缺少产品级收益。 |
| N/A | `huggingface/transformers` | 无需融合 | `minddistill` | 最新为 Mamba 模块化修复和 Kimi 转换清理，未触发 MindDistill 的内容蒸馏能力缺口。 |
| N/A | `tldraw/tldraw` | 无需融合 | `nichecraft` | 最新为 dotcom Browser Run 缩略图管线去重，属于上游站点内务，不对应 NicheCraft 白板/PPT 能力。 |

## 证据

- 最新提交与文件：`/root/projects/zhixie-ops-maintenance/references/competitor-latest-commit-evidence-2026-07-28.json`
- 产品能力事实：`/tmp/fusion-audit-20260728-products/*/product_convergence.json`
- 已纠偏候选池：`/root/.hermes/shared/skills/product-repo-monitor/references/competitor-candidate-pool.json`

## 落地顺序

1. P0：SkillSpector 执行核算闭环。
2. P1：LiveSync 仅提炼真实双端/P2P 验收，不复制同步引擎。
3. P2：Dify/Scrapy 等待产品触发条件；其余关闭本轮融合。
