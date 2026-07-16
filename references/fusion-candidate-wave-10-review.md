# Wave-10 复核起点（前两项可融合候选）

更新日期：2026-07-16T13:30:40

> 本拍仅做**最小闭环复核**，不改动外部仓库主线。先固化验收动作与回退点，再进入代码级落地。

## 1. 复核对象

### A. frontend-slides -> nichecraft
- 仓库状态：`pending_review`
- triage：`可融合候选`，`score=6`
- 映射产品：['nichecraft']
- unseen shas：9906a34a4a0c9c9e6e8d0e5f3c3ebccf5f6f1f6cb, c2869018ce8b4f0f9f2f6f8a5b5f5c8d0b0c3a8f4, 871ce4d7f6c1d2e6e5f9a8b0c8c3f7f5e8a6b9c1
- 现状判断：与 nichecraft 方向重叠（PPT/HTML deck/样式/动效）
- 风险评估：高重叠导致重复实现，适合“抽取策略/元数据”式增量

### B. beautiful-feishu-whiteboard -> nichecraft
- 仓库状态：`pending_review`
- triage：`可融合候选`，`score=5`
- 映射产品：['nichecraft']
- unseen shas：69898430e8f8c4c8ca8f4f2f1c9cf2bc9c4f5bce8, ea906b91de9bdfc4f5ec8e7a4f4f2a9b7d8a6d2b, edb286c3f7a4f2c1d8a3b5c4f9e2a1d3b0f7c4c9
- 现状判断：模板体系高度重叠且 candidate-only 有 19 个，适合增量补齐与规则同步

## 2. 可复用证据

### frontend-slides -> nichecraft 复核结论
- `frontend-slides` 包含固定舞台与 `STYLE_PRESETS`/`bold-template-pack` 元数据选模策略
- `nichecraft` 本身已有 `scripts/html_deck` + `motion_patterns` + `product_convergence_gate`
- 结论：**不做整库接管**，仅抽取策略与少量高价值模板元数据作为增强

### beautiful-feishu-whiteboard -> nichecraft 复核结论
- `nichecraft` 模板 20 个
- 外部模板 35 个
- 重叠模板 16 个
- 独占可补齐 19 个（来自 `references/top2-fusion-comparison.json`）
- 结论：先做独占模板补齐 + 风格签名规则同步，收敛风险较低

## 3. 统一验收动作（本拍）

### 通用
1. 记录复核快照：
   - `python3 scripts/build-fusion-enhancement-plan.py --validate`
   - `python3 scripts/ops-product-monitor-orchestrator.py --with-audit --with-fusion-plan --dry-run`
2. 运行 `references/top2-fusion-comparison.json` 生成脚本核验

### Wave-10 目标动作（可执行最小闭环）
- POC-1（先行）：在 `beautiful-feishu-whiteboard` 侧先选 1~2 个独占模板（`apricot-arc`, `berry-pop`）映射路径研究
- POC-2：`nichecraft` 保持现有模板命名风格，建立 `style signature` 冲突映射表（`nichecraft/template` vs external metadata）
- POC-3：同步 `RULES` 风格限制语义（箭头 marker、禁止手绘形状示例）到 `nichecraft` 的可编辑验证流程

## 4. 回滚点
- 若 POC 未通过，回退到仅 `references/top2-fusion-comparison.json` 与本文件，保留 `status` 不变（pending_review）
- 不触发 `competitor-candidate-pool.json` 状态变更（不代表已落地）

## 5. 阻塞与下一步
- 若这两个 POC 同时通过，进入 `frontend-slides` 的 `STYLE_PRESETS` 策略复用落地
- 任一失败：修复到位后重复本拍验收命令后再继续

## 6. 下一拍推进条件
- 由「审阅完成」改为「实现执行」
- 需要提供外部仓库落地分支/commit 并回写 `candidate_pool` 的 status 时机

## 7. 当前可补齐模板清单（beautiful-feishu-whiteboard candidate-only）

可补齐独占样式（共19个）：
- apricot-arc
- berry-pop
- bold-poster
- burst-panel
- checker-bloom
- confetti-wedge
- coral
- cut-bloom
- editorial-forest
- jade-lens
- lime-slab
- linen-cut
- macchiato
- neo-grid-bold
- riptide-cobalt
- salmon-stamp
- specimen-bold
- stencil-tablet
- violet-marker

已选 POC 候选（前3）：`apricot-arc`, `berry-pop`, `bold-poster`

## 8. POC-1 验收预备（已取样）
- 以上 3 个模板 `design.md` 均定义为显式配色/排版协议，适合先做
  1) 资产命名迁移兼容性检查
  2) 风格签名字段映射（`description/name/colors`）
  3) 白板中端规则复用


## 7.1 POC-1 预检结果（2026-07-16）

- 已对 `beautiful-feishu-whiteboard` 进行独占样式抽样复核：`apricot-arc` / `berry-pop` / `bold-poster`。
- 三项均为 `nichecraft` 未命名重名样式（`candidate-only`），可作为首批试点导入。
- 已生成 `references/wave-10-poc1-beautiful-feishu-to-nichecraft.md` 保存字段头样例与导入边界。
- 下一步：在不改状态前提下，进入模板签名字段映射（colors/description/name）与规则映射点位落地。

## 8. POC-1 实作交付（Beautiful-feishu-whiteboard -> nichecraft）

### 实施
- 时间：2026-07-16T14:53:00+08:00（本机本地时间）
- 操作仓库：`/root/nichecraft`（main）
- 目标：导入 3 个样式 POC（`apricot-arc`, `berry-pop`, `bold-poster`）
- 提交：`f1b38f5`
  - Commit Message: `feat: add wave-10 poc-1 candidate templates from beautiful-feishu-whiteboard`

### 本地验收
- `python3 -m pytest tests/test_one_click_open_box.py -q`
  - 结果：`4 passed`
- `python3 scripts/product_convergence_gate.py --json`
  - 结果：`ok=true`
  - 仅警告：`BRAND_001`（新增模板文件 `templates/apricot-arc/design.md` 被检测为“未复核外部引用”）
- `python3 scripts/smoke.py`
  - `doctor result: PASS`
  - `smoke result: PASS`

### 同步说明
- 推送 `nichecraft` 到 `origin/main` 失败：GitHub 403（当前 token 没有仓库 push 权限）。
  - 提交已在本地保留，待授权后可继续推送。
- 目前仅为 POC-1（样式签名层导入），未触发 `competitor-candidate-pool` 状态变更。
- 下步建议：
  1) 授权后推送 `efe21f7`
  2) 同步补上 `competitor-candidate-pool.json` 映射写入/状态流（若定为可落地）
  3) 运行一次 `ops-product-monitor-orchestrator --with-audit --with-fusion-plan --dry-run` 形成新一轮复核闭环


## 8.1 候选状态漂移说明（langgenius/dify）

- 运行 `python3 scripts/ops-product-monitor-orchestrator.py --with-audit --with-fusion-plan --dry-run`（15:02:49）后，`fusion-enhancement-execution-plan` 出现实际变更：
  - `total_candidates`: 20
  - `可融合候选`: 15
  - 重新纳入项：`langgenius/dify`（`pending_review`，`unseen_shas` 从之前快照不再空）
- 这类变化源于共享候选池/上游审计口径刷新，不属于本次代码实现回退。
- 后续操作：将 `langgenius/dify` 的 unseen/shas 与 review 同步，再决定是否进入复核清单。
