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

## Wave-3 执行补充（2026-07-15）
- 已完成 `nichecraft` 与 `canvas-design` 的外部技能能力入口改造（反AI风格静态扫描 + style-guard）。
- 对应输出文件：仓库内新增 `anti_ai_style_guard.py` / `anti_ai_sanity.mjs`，并接入各自 doctor 流程。

## Wave-4 执行补充（2026-07-15）
- 已完成 `artipen` 与 `fractovision` 的反AI风格静态扫描接入（`style-guard`），并接入 doctor 闭环。
- 对应输出文件：`artipen/scripts/anti_ai_style_guard.py`，`fractovision/scripts/anti_ai_style_guard.py`。
- 回归动作：新增脚本通过 `py_compile`、`check:syntax`、`pytest test_one_click_open_box.py` 验证。
- 状态：**已完成（主仓库推送）**

## 风险与回退
- 风险点：`aestheflow` 已转为映射补位（`22d`）并不进入主失败项；当前审计口径为 23 个主条目、F=0。

- `barren-order` 已补齐 `crewAIInc/crewAI` 映射方向的数据库持久化能力（sqlite）

- 回退点：恢复 `references/product-list.md` 与候选清单到上次稳定版本；清空本轮新增候选字段后重跑 `--validate` 与 orchestrator

## Wave-5 执行补充（2026-07-15）
- 已完成 `ideasphere` 反AI风格静态扫描接入（`style-guard`）与 doctor 闭环，并新增 `/diag/style` API 入口。
- 对应输出文件：`ideasphere/scripts/anti_ai_style_guard.py`，`ideasphere/scripts/ideasphere_api.py`。
- 回归动作：`py_compile`、`check:syntax`、`pytest test_one_click_open_box.py`、DRY_RUN 统一脚本验证均通过。
- 状态：**已完成（主仓库推送）**


## Wave-6 启动建议（2026-07-15）
- 已基于当前可融合候选清单生成下一批执行提案：`references/fusion-candidate-wave-6-review.md`。
- 当前待评审清单（8项）已分出执行优先：
  - P1：`mem0ai/mem0`、`crewAIInc/crewAI`
  - P2：其余 6 项（`excalidraw/excalidraw`、`NVIDIA/SkillSpector`、`huggingface/diffusers`、`botpress/botpress`、`assafelovic/gpt-researcher`、`huggingface/transformers`）
- 仍维持观察/复核 3 项与仅记录 3 项状态，不入本批执行。
