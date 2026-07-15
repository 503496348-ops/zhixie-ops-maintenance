# Wave-6 复盘与下一批执行建议（2026-07-15）

目标：在已完成竞品日报/产品日报口径固化后，推进可融合候选的下一步行动。当前依据：
- `references/fusion-enhancement-execution-plan.json`
- 最新一次 DRY_RUN 证据：`references/orchestrator-run-result.json`
- 产品口径快照：`references/product-repo-card`（25 个产品，产品 Issue 验证：`products_total 25` / `products_with_issues {}`）

## 本轮待行动：可融合候选（7 项）

以下 7 项保持 `status=pending_review`，优先级按 `score` + 对应产品缺口一致性排序：

1. `mem0ai/mem0 -> hermes-doctor, pipixia-doctor`
   - 优先级：**P1**（score 6）
   - 下一步：抽样验收 `hermes-doctor` 的历史 `memory` 能力链路，确认是否还存在可直接引入 mem0 的 API/数据抽象。

2. `excalidraw/excalidraw -> nichecraft`
   - 优先级：**P2**（score 6）
   - 下一步：核对 `nichecraft` 现有反 AI 静态风格能力是否覆盖竞品核心能力差距（已完成 Wave-4/5 体系可复用）。

3. `NVIDIA/SkillSpector -> hermes-security-suite`
   - 优先级：**P2**（score 4）
   - 下一步：以“安全审计可解释性”与“告警证据持久化”为对齐点，先确认 `hermes-security-suite` 可直接接收 `SkillSpector` 的检测项。

4. `huggingface/diffusers -> ideasphere`
   - 优先级：**P2**（score 4）
   - 下一步：先对比当前 `ideasphere` 生成链路与 `diffusers` 的采样/模型配置能力边界，确认是否为“参数化入口复用”还是“仅风格层增强”。

5. `botpress/botpress -> easyrhythm`
   - 优先级：**P2**（score 4）
   - 下一步：确认 `easyrhythm` 是否在会话流/对话脚本层存在可插拔策略，避免重复改动到 runtime。

6. `assafelovic/gpt-researcher -> fission-creative`
   - 优先级：**P2**（score 4）
   - 下一步：评估 `fission-creative` 的长文生成后处理链路与 `gpt-researcher` 的事实来源与来源追溯字段是否可对齐。

7. `huggingface/transformers -> minddistill, minddistill`
   - 优先级：**P2**（score 4）
   - 下一步：目前该项仍重复映射同一产品两次（`minddistill`），复盘时先拆分为一次性归并条目，避免重复工单。

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
- 必要时更新：`references/fusion-enhancement-execution-plan.json/.md` 与 `references/fusion-enhancement-candidate-assessment.md`。