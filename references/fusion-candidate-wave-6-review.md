# Wave-6 复盘与下一批执行建议（2026-07-15）

目标：在已完成竞品日报/产品日报口径固化后，推进可融合候选的下一步行动。当前依据：
- `references/fusion-enhancement-execution-plan.json`
- 最新一次 DRY_RUN 证据：`references/orchestrator-run-result.json`
- 产品口径快照：`references/product-repo-card`（25 个产品，产品 Issue 验证：`products_total 25` / `products_with_issues {}`）

## 本轮待行动：可融合候选

### 已完成（6 项）

1. `mem0ai/mem0 -> hermes-doctor、pipixia-doctor`
   - 优先级：**P1**（score 6）
   - 完成时间：2026-07-15 21:12
   - 完成动作：新增 `scripts/mem0_bridge.py` 并接入 `scripts/doctor.py`
   - 产物：分别在两仓库创建并合并分支 `feat/mem0-bridge-wave-6`（未提 PR）

2. `excalidraw/excalidraw -> nichecraft`
   - 优先级：**P1**（score 6）
   - 完成时间：2026-07-15 22:08
   - 完成动作：新增 `scripts/excalidraw_bridge.py`，并接入 `scripts/doctor.py`、`scripts/nichecraft_api.py`，补充 `package.json` 与 `product_convergence.json`
   - 产物：`nichecraft` 分支 `feat/excalidraw-bridge-wave-6`

3. `NVIDIA/SkillSpector -> hermes-security-suite`
   - 优先级：**P2**（score 4）
   - 完成时间：2026-07-15 22:45
   - 完成动作：新增 `scripts/skillspector_bridge.py`，并接入 `scripts/doctor.py`、`scripts/hermes_security_suite_api.py`，补充 `package.json` 与 `product_convergence.json`，增加冒烟与桥接测试
   - 产物：`hermes-security-suite` 分支 `feat/skillspector-bridge-wave-6`

4. `huggingface/diffusers -> ideasphere`
   - 优先级：**P2**（score 4）
   - 完成时间：2026-07-15（历史补充）
   - 完成动作：在 `ideasphere` 内已存在 `modules/diffusers_engine/*` 与 `video_processor` 的 diffusers 能力映射，且当前 doctor/gate/smoke 已通过。
   - 产物：`ideasphere` 主仓主线（`b3fe3aa`）

5. `assafelovic/gpt-researcher -> fission-creative`
   - 优先级：**P2**（score 4）
   - 完成时间：2026-07-15（本轮）
   - 完成动作：新增 `scripts/gpt_researcher_bridge.py` 与 `tests/test_gpt_researcher_bridge.py`；补齐 `package.json` 与 `product_convergence.json` 的可见脚本/smoke 目标，完成 doctor/gate/compile/pytest（含新测试）验证。
   - 产物：`fission-creative` 分支 `feat/gpt-researcher-bridge-wave-6`

6. `botpress/botpress -> easyrhythm`
   - 优先级：**P2**（score 4）
   - 完成时间：2026-07-16（本轮）
   - 完成动作：新增 `python-backend/adapters/botpress.py` 并补齐 `adapters/__init__.py` + `adapters/router.py` 适配入口，完成 doctor/gate/smoke/pytest 验证。
   - 产物：`easyrhythm` 分支 `feat/botpress-bridge-wave-6`

### 待执行（1 项）

以下 1 项保持 `status=pending_review`，优先级按 `score` + 对应产品缺口一致性排序：

1. `huggingface/transformers -> minddistill、minddistill`
   - 优先级：**P2**（score 4）
   - 下一步：该项与 minddistill 重复映射，需先合并为单一工单避免重复复核。

## 观察/复核项（3 项，保留）

- `Comfy-Org/ComfyUI -> fractovision`
- `vrtmrz/obsidian-livesync -> neverend`
- `Auriti-Labs/geo-optimizer-skill -> minddistill`

## 仅记录项（3 项，暂不进入执行）

- `AUTOMATIC1111/stable-diffusion-webui -> fractovision`
- `linuxserver/docker-obsidian -> neverend`
- `aaron-he-zhu/seo-geo-claude-skills -> minddistill`

## 统一验收门禁（每条执行前）

- 单条代码变更前必须先补齐：`doctor` pass、`check:syntax`、`pytest test_one_click_open_box.py`
- 每条执行后必须同步 DRY_RUN：
  - `scripts/ops-product-monitor-orchestrator.py --with-audit --with-fusion-plan --dry-run`
  - `scripts/product-repo-card.py --dry-run`
  - `scripts/audit-products.py`
- 必要时更新：`references/fusion-enhancement-execution-plan.json/.md` 与 `references/fusion-enhancement-candidate-assessment.md`.
