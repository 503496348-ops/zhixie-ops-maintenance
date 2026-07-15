# 仓内融合增强候选评估（执行记录）

> 依据：`references/fusion-enhancement-execution-plan.json`

## 执行前提
- `references/fusion-enhancement-execution-plan.md` 已按 `build-fusion-enhancement-plan.py --validate` 生成。
- 本轮审计来源：`references/audit-report.json`
- 竞品分诊来源：`/root/.hermes/shared/skills/product-repo-monitor/references/competitor-candidate-pool.json`

## P1（优先执行）
- `langgenius/dify` → `hermes-doctor`, `pipixia-doctor`（缺口：已补齐 Web + SQLite 持久化底座）
- `crewAIInc/crewAI` → `barren-order`（缺口：数据库）
- `excalidraw/excalidraw` → `nichecraft`（缺口：数据库）
- `huggingface/diffusers` → `ideasphere`（缺口：Web框架, 数据库）
- `NVIDIA/SkillSpector` → `hermes-security-suite`（缺口：无明显缺口，需先 commit 语义回放）
- `mem0ai/mem0` → `hermes-doctor`, `pipixia-doctor`（缺口：已部分补齐；`hermes-doctor` 已完成）
- `botpress/botpress` → `easyrhythm`（缺口：数据库）
- `assafelovic/gpt-researcher` → `fission-creative`（缺口：待补齐）
- `huggingface/transformers` → `aestheflow`, `minddistill`（缺口：转入观察/人工复核）

## P1 执行约束
1. 每项先给出“最小可交付改造点”
2. 审计前后保持 `product-list.md` 与 `references/product-list` 口径一致
3. 先执行静态验证（文件与脚本）再触发外部仓库变更

## 本轮审计确认
- 总产品条目（审计脚本处理）：24
- 可交付/未归档主口径通过：仅 `aestheflow` 仍为克隆失败项（`huggingface/transformers` 已从“可融合候选”下调为“观察/人工复核”）
- 其它候选项当前无新增审计告警（在当前脚本口径内）

## 风险与回退
- 风险点：`aestheflow` repo 不存在，无法验证对该仓库的本地交付增强
- 回退点：恢复 `references/product-list.md` 与候选清单到上次稳定版本；清空本轮新增候选字段后重跑 `--validate` 与 orchestrator
