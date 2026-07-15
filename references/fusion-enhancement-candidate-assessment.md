# 仓内融合增强候选评估（执行记录）

> 依据：`references/fusion-enhancement-execution-plan.json`

## 执行前提
- `references/fusion-enhancement-execution-plan.md` 已按 `build-fusion-enhancement-plan.py --validate` 生成。
- 本轮审计来源：`references/audit-report.json`
- 竞品分诊来源：`/root/.hermes/shared/skills/product-repo-monitor/references/competitor-candidate-pool.json`

## P1（优先执行）
- `langgenius/dify` → `hermes-doctor`, `pipixia-doctor`（缺口：已完成）
- `excalidraw/excalidraw` → `nichecraft`（缺口：已完成）
- `huggingface/diffusers` → `ideasphere`（缺口：已完成）
- `NVIDIA/SkillSpector` → `hermes-security-suite`（缺口：已完成）
- `mem0ai/mem0` → `hermes-doctor`, `pipixia-doctor`（缺口：已完成）
- `botpress/botpress` → `easyrhythm`（缺口：已完成）
- `assafelovic/gpt-researcher` → `fission-creative`（缺口：已完成）
- `huggingface/transformers` → `aestheflow`（观察/人工复核），`minddistill`（缺口：已完成）

## P1 执行约束
1. 每项先给出“最小可交付改造点”
2. 审计前后保持 `product-list.md` 与 `references/product-list` 口径一致
3. 先执行静态验证（文件与脚本）再触发外部仓库变更

## 本轮审计确认
- 总产品条目（审计脚本处理）：23
- 可交付/未归档主口径通过：已完成方案A/B隔离，`aestheflow` 改为映射补位后不再作为主失败项；`minddistill` 对应 `huggingface/transformers` 映射路径保留
- 其它候选项当前无新增审计告警（在当前脚本口径内）

## 外部新增技能补充（已评估）
- `yetone/kill-ai-slop`：建议优先挂接 `nichecraft`、`canvas-design`；次级 `artipen / fractovision / ideasphere`。
- `jakubkrehel/skills`：建议优先挂接 `nichecraft`、`canvas-design`；次级 `artipen / fractovision / ideasphere`。
- `方案B` 已执行：`Aestheflow` 增加映射补位行 `22d`，后续以 `minddistill` 承接内容分析缺口。

## 风险与回退
- 风险点：`aestheflow` 已转为映射补位（`22d`）并不进入主失败项；当前审计口径为 23 个主条目、F=0。

- `barren-order` 已补齐 `crewAIInc/crewAI` 映射方向的数据库持久化能力（sqlite）

- 回退点：恢复 `references/product-list.md` 与候选清单到上次稳定版本；清空本轮新增候选字段后重跑 `--validate` 与 orchestrator
