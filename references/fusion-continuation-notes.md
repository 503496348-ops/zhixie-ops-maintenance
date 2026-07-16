# 前两项候选复核·第二轮继续执行（frontend-slides / beautiful-feishu-whiteboard）

更新时间：2026-07-16T13:11:00+08:00

状态：`pending_review` 继续复核，未标记 `implemented`

## 1) frontend-slides -> nichecraft
- 源 repo: `zarazhangrui/frontend-slides`
- 映射产品: `nichecraft`
- 评分: 6
- 适配度结论: **可复用但与 nichecraft 有明显重叠**，适合作为增强而非替代。

### 复核证据（直接可见）
- Frontend-slides 已包含固定 16:9 舞台约束、动画策略与视觉预览规则（`STYLE_PRESETS.md`、`viewport-base.css`、`animation-patterns.md`）
- 近 10 次提交内持续强调 `STYLE_PRESETS` 与 `bold-template-pack`，并无大面积核心算法重写
- 最近提交 `9906a34` 为 `README` 文案更新；最近有一次提交 `871ce4d` 调整 24 个 `design.md`
- Nichecraft 本身已有 `scripts/html_deck` + `motion_patterns` + `ppts` 相关流程，说明目标方向已存在

### 结论
- 这条链路的价值不在“重建 HTML 引擎”，而在于：
  1. 把 `STYLE_PRESETS` 体系和 `bold-template-pack` 的选模策略（元数据优先、最小化读取）嫁接到 Nichecraft 的样式/模板入口。
  2. 统一动画预算上限与可访问性规则，减少当前 deck 生成中的风格漂移。

### 执行动作（建议最小闭环）
1. 映射对齐：列出 `nichecraft/templates` 与 `frontend-slides` 的 `bold-template-pack/templates` 重名集合。
2. 先迁移一个样式（如 `block-frame`）为 POC，确认输出 HTML 结构与现有 `scripts/html_deck` 无冲突。
3. 将 `viewport-base.css` 的舞台规则与 Nichecraft 的 deck 渲染模板中的舞台参数对齐。
4. 运行 `python3 scripts/smoke.py` / `python3 scripts/product_convergence_gate.py --json`。

---

## 2) beautiful-feishu-whiteboard -> nichecraft
- 源 repo: `zarazhangrui/beautiful-feishu-whiteboard`
- 映射产品: `nichecraft`
- 评分: 5
- 适配度结论: **高重叠，需以增量补齐优先**（不是全量替换）。

### 复核证据（直接可见）
- 当前 Nichecraft 模板目录 20 个；外部仓库模板 35 个。
- 可直接重叠（模板名重名）16 个：
  `avocado-press, block-frame, cobalt-bloom, court-press, crayon-stack, grove, grove-block, long-table, mint-brut, monochrome, papier-bleu, pin-and-paper, raw-grid, reading-room, riso-brut, soft-editorial`
- 外部仓库仅有 19 个可补齐模板（`apricot-arc` 等），可能带来增量价值。
- 外部仓库近 2 年版本行为：`RULES.md` 强化了可编辑中端形状与箭头规范、`CATALOG.md` 的风格签名映射。

### 结论
- 当前最小可执行动作是：补齐 `19` 个独占风格模板 + 同步风格签名策略 + 统一白板中端渲染规则。

### 执行动作（建议最小闭环）
1. 只选 1 个独占新风格（如 `apricot-arc`）+ 1 个重叠风格做对照，提取 `template/design.md` 与 `assets/styles/*.png`。
2. 将其迁移到 Nichecraft 对应目录并保持 style 命名策略一致。
3. 在 `RULES` 中增加“禁止手绘 arrow/有机图形”的判定示例，接上现有 `svg` 审计。
4. 运行 `python3 scripts/smoke.py` / `python3 scripts/product_convergence_gate.py --json`。

---

## 下一步（用户“继续”自动继续触发）
- 以上两条均为可复用增量，建议按该顺序执行：
  1) `beautiful-feishu-whiteboard` 先补齐独占 19 模板 POC（2~3 模板）
  2) `frontend-slides` 提取 `STYLE_PRESETS` 与 `bold-template-pack` 的元数据选模策略
- 所有动作完成后再回到 `ops`，重跑全链路 DRY-RUN 输出快照与差异。
