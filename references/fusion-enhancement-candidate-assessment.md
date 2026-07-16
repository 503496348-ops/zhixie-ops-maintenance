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


## Wave-6 进展（2026-07-15）
- 已执行：`mem0ai/mem0` 的 P1 试点。已完成：
  - hermes-doctor：新增 `scripts/mem0_bridge.py`，并在 `scripts/doctor.py` 增加 `mem0 compatibility bridge` 检查。
  - pipixia-doctor：新增 `scripts/mem0_bridge.py`，并在 `scripts/doctor.py` 增加 `mem0 compatibility bridge` 检查。
  - 产物提交：`hermes-doctor` 分支 `feat/mem0-bridge-wave-6`（commit `2b6be75`）与 `pipixia-doctor` 分支 `feat/mem0-bridge-wave-6`（commit `5c15297`）。
- 已执行：`excalidraw/excalidraw -> nichecraft`
  - 产物提交：`nichecraft` 分支 `feat/excalidraw-bridge-wave-6`（commit `e573109`）。
  - 改造点：新增 `scripts/excalidraw_bridge.py`，在 `scripts/doctor.py` 增加桥接 smoke，`scripts/nichecraft_api.py` 新增 `/diag/excalidraw`，并补充 `package.json` 与 `product_convergence.json`。
- 统一验收完成：`check:syntax`、`pytest test_one_click_open_box.py`、`product_convergence_gate --json`。
- 已完成当前可执行清单：`NVIDIA/SkillSpector`、`huggingface/diffusers`、`botpress/botpress`、`assafelovic/gpt-researcher`、`huggingface/transformers`。
- minddistill 映射项（`huggingface/transformers`）对应 `minddistill` 的最小闭环桥接已补齐（分支 `feat/transformers-bridge-wave-6`）。
- 仍维持观察/复核 3 项与仅记录 3 项状态，不入本批执行。
- 当前提案文档：`references/fusion-candidate-wave-6-review.md`。

## Wave-7 复核起点（2026-07-16）
- 按“先复核不改动”策略推进。
- 本轮复核三项：
  - `Comfy-Org/ComfyUI -> fractovision`
  - `vrtmrz/obsidian-livesync -> neverend`
  - `Auriti-Labs/geo-optimizer-skill -> minddistill`
- 观察结论：三类提交当前均非直接服务/API 层增量（偏版本、发布、前端构建/文案），暂不进入实现。
- 详细记录：`references/fusion-candidate-wave-7-review.md`。

## Wave-8 复核补录（2026-07-16）
- 再次复核结论：三项 `watching` 仍未形成可直接落地的产品服务/API 增量，继续保留观察。
- 复核依据：`Comfy-Org/ComfyUI` 仍为版本与视频测试修复；`vrtmrz/obsidian-livesync` 仍为发布与依赖/文案/测试配置更新；`Auriti-Labs/geo-optimizer-skill` 仍为前端索引与构建脚本更新。
- 记录文件：`references/fusion-candidate-wave-8-review.md`。
- 执行策略：继续在每次 `继续` 前做一次全链路 DRY-RUN 验证后再决定是否升级执行。


## Wave-9 执行落地（2026-07-16）
- 已按你同意的 6 个可融合候选执行并完成主线合并：
  - mem0ai/mem0 → hermes-doctor（`2b6be75`）
  - mem0ai/mem0 → pipixia-doctor（`5c15297`）
  - excalidraw/excalidraw → nichecraft（`e573109`）
  - huggingface/transformers → minddistill（`2dea1a6`）
  - botpress/botpress → easyrhythm（`f0699d4`）
  - assafelovic/gpt-researcher → fission-creative（`0f5bc8e`）
  - NVIDIA/SkillSpector → hermes-security-suite（`17f3a24` 已位于 main）
- 对应验收命令：
  - `PYTHONPATH=. pytest -q <对应 test_*.py>`（全部通过）
  - `PYTHONPATH=. python3 scripts/product_convergence_gate.py --json`（全部 ok=true）
- 竞品候选池状态：以上 6 项 `status` 已同步为 `implemented`。
- 继续观察项：
  - Comfy-Org/ComfyUI、vrtmrz/obsidian-livesync、Auriti-Labs/geo-optimizer-skill
