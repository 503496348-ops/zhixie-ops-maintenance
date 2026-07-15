# 新技能融合增强匹配评估（2026-07-15）

> 目标：基于你新增的两个外部技能仓库，给出可落地的融合增强匹配与优先级。

## 1) external: yetone/kill-ai-slop

### 技能特征
- 反 AI 生成痕迹（网站/产品视觉风格）检测与修复建议。
- 着重清理：视觉与文案层面的“机器默认感”，如渐变、过度卡片化、emoji、排版异常。
- 包含可直接应用的 Agent Skill。

### 推荐匹配仓库（优先级）
1. **nichecraft（飞书白板设计）**
   - 原因：产品本身是设计系统/配色/界面呈现相关，最容易映射为风格体检与风格修正链路。
   - 建议融合点：
     - 生成/导出前做 AI-slop 检测扫描（色彩、卡片结构、字体对齐、动效风格）
     - 返回“可执行修复建议”并生成替换样式稿
2. **canvas-design（艺游未境）**
   - 原因：视觉创作链路（海报/PPT/原型/动画/视频）重，跨模态资产生成，风格噪音检测价值高。
   - 建议融合点：
     - 将 anti-slop 规则接入内容模板产物审查（图文并重）
     - 在自动输出后附带“清洁度评分 + 一键修复建议”
3. **artipen（文章编排）**
   - 原因：文章配图与排版能力，kill-ai-slop 在文案与排版风格处可提供直接价值。
   - 建议融合点：
     - 增加排版“反AI味”规则阈值，输出替代版块样式
4. **fractovision / ideasphere（内容生产产物）**（次优）
   - 适合作为“二次清洗”插件：在图文/视频片段导出后做风格偏差扫描与修复提示。

### 不优先匹配
- 数字分析/运维类仓（stratapro、hermes-security-suite、mindriver 等）
  - 与该技能的视觉/文案修复目标匹配度低。

---

## 2) external: jakubkrehel/skills

### 技能特征
- 动画、排版、颜色、布局、字体等“产品外观与排版体验”增强。
- 目标仓：提升界面表达/视觉打磨效率。

### 推荐匹配仓库（优先级）
1. **nichecraft（飞书白板设计）**
   - 一致性最高（设计系统场景），可作为核心接入目标。
   - 融合方式：把本地 skills 按技能组映射为“排版优化、配色优化、动效优化”入口。
2. **canvas-design（艺游未境）**
   - 视觉生成链路强，适合映射色彩/布局/动效模板化能力。
   - 融合方式：在 PPT/原型/海报导出环节加入“布局-颜色-动画一致性”检查。
3. **artipen / fractovision / ideasphere**（备选）
   - 分别覆盖文章编排、媒体内容、视频内容，适合引入“视觉质量闭环”而非核心能力。

### 建议执行顺序
- **第一波（最省成本）**：nichecraft + canvas-design
- **第二波（收益可验证）**：artipen + fractovision

---

## 方案B 与现有 `aestheflow` 映射关系

你要求的 B 方案（映射补位）已执行：
- 已在 `product-list.md` 增加 `Aestheflow 反AI痕迹补位` 行（映射到 `minddistill`）。
- 这既保留产品清单口径不变，也能在后续把 `kill-ai-slop` 这类内容风格能力沉淀为“内容分析补位路线”。

## 3) Wave-3 执行记录（2026-07-15）

- 已落地 `nichecraft`：新增 `scripts/anti_ai_style_guard.py`，并接入 `scripts/doctor.py` 与 `scripts/nichecraft_api.py`，提供
  - AI风格风险扫描（emoji、渐变、全大写）
  - `/diag/style` API 入口
  - `npm run style-guard` 脚本
- 已落地 `canvas-design`：新增 `scripts/anti_ai_sanity.mjs`，并接入 `scripts/doctor.mjs` 与 `npm run style-guard`，提供
  - 反AI视觉静态评分（非阻断）
  - `npm run style-guard` 脚本
  - 状态：**已完成（nichecraft 与 canvas-design 已推送主仓库；canvas-design 变更未触发功能阻塞，PR bypass 提示已确认）**


## 4) Wave-4 执行记录（2026-07-15）

- 已落地 `artipen`：新增 `scripts/anti_ai_style_guard.py`，并接入 `scripts/doctor.py`。
  - `npm run style-guard` 入口已加入
  - `check:syntax` 已覆盖 anti-AI 检查脚本
- 已落地 `fractovision`：新增 `scripts/anti_ai_style_guard.py`，并接入 `scripts/doctor.py`。
  - `npm run style-guard` 入口已加入
  - `check:syntax` 已覆盖 anti-AI 检查脚本
- 验收动作：`py_compile`、`check:syntax`、`pytest test_one_click_open_box` 均通过。
- 状态：**已完成（`artipen`、`fractovision` 已推送主仓）**


## 5) Wave-5 执行记录（2026-07-15）

- 已落地 `ideasphere`：新增 `scripts/anti_ai_style_guard.py`，并接入 `scripts/doctor.py` 与 `scripts/ideasphere_api.py`。
  - 新增 `npm run style-guard` 入口
  - `check:syntax` 已覆盖 anti-AI 检查脚本
  - `doctor` 输出为 PASS（样式告警为非阻断）
- 验收动作：`py_compile`、`check:syntax`、`pytest test_one_click_open_box`、`ops orchestrator --dry-run`、`product-repo-card --dry-run`、`audit-products` 均通过
- 状态：**已完成（`ideasphere` 已推送主仓）**


## 6) Wave-6 下一步计划（2026-07-15）
- 已进入下一步可融合候选评审：从 `references/fusion-enhancement-execution-plan.json` 抽取 8 项 `pending_review` 可融合候选
  - P1：`mem0ai/mem0`、`crewAIInc/crewAI`
  - P2：`excalidraw/excalidraw`、`NVIDIA/SkillSpector`、`huggingface/diffusers`、`botpress/botpress`、`assafelovic/gpt-researcher`、`huggingface/transformers`
- 观察/复核与仅记录条目暂缓执行，保持风控界限
- 输出决策文档：`references/fusion-candidate-wave-6-review.md`
