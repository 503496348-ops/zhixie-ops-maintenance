---
name: zhixie-ops-maintenance
description: 智械工坊-OPS维护：产品仓库日报、竞品监控、产品质量门禁、cron/no_agent 运维、夜间只读审计与融合候选分诊的一体化维护技能。遇到智械工坊 OPS、产品日报、竞品日报、产品审计、cron 故障、no_agent token hygiene、仓库发布门禁、远端干净 clone 复验时都应使用。
triggers:
  - 产品仓库日报
  - 仓库监控
  - repo monitor
  - 产品日报
  - 竞品监控
  - 竞品持续监控
  - competitor monitor
  - 产品质量审计
  - 产品审计
  - product audit
  - SKILL.md质量检查
  - 技术特性检查
  - 夜间产品进化
  - 夜间自主修复
  - 早餐日报
  - ABCD评分
  - P0风险
  - 产品真实交付评分
  - 智械工坊OPS维护
  - 智械工坊-OPS维护
  - OPS维护
  - no_agent token hygiene
  - cron三层诊断
  - 远端干净clone验证
  - 产品质量门禁
  - 仓库发布门禁
version: "6.1"
---

# 产品仓库监控


## v6.1 融合增强：智械工坊 OPS 维护面

本技能从 `product-repo-monitor` 升级为 **智械工坊-OPS维护**。旧名保留为历史关键词，职责扩大为“产品矩阵事实源 + 自动化日报 + 竞品监控 + 仓库质量门禁 + Cron 运维”的统一控制台。

### 本轮融合来源

| 来源技能 | 融合进本技能的能力 | 落点 |
|---|---|---|
| `product-quality-gate` | 一键开箱、README/SKILL 契约、测试/doctor/smoke、远端干净 clone 二次验证 | `references/repository-release-checklist.md` |
| `product/product-ops` | 产品全生命周期、矩阵/Bitable/仓库三端同步、竞品融合后去污染与推送纪律 | `references/local-fusion-map.md` |
| `cron-failure-three-layer-diagnosis` | 配置层→执行层→依赖层诊断、no_agent 输出非空、wrapper 化、token 消耗治理 | `references/ops-maintenance-runbook.md` |
| `nightly-evolution-reflection` | 夜间审计前置自检、artifact 验证、系统健康快照、未验证不标记解决 | `references/ops-maintenance-runbook.md` |
| `competitor-fusion` | 监控告警后的文件级 triage、反向融合、运行时语义抽取、外部引用零残留 | `references/local-fusion-map.md` |

### 使用边界

- 默认只读审计和确定性脚本；监控类任务优先 `no_agent=true + script`，避免 LLM 二次改写数字。
- 数字口径只来自 GitHub API、`product-list.md`、`competitors.md`、schema-v2 snapshot、脚本 stdout 和测试输出。
- 修改 cron/provider/API key/gateway 属 S4，高危，必须另行授权；本技能不把“诊断”偷换成“重启”。
- 发布仓库前必须执行敏感信息扫描，Feishu/Lark/Bitable 连接标识统一写成 `[REDACTED_*]`。

## 核心原则

**单一数据源**：所有列表型配置只在一个地方维护，脚本自动读取。
- 产品清单 → `references/product-list.md`（人工维护）
- 竞品清单 → `references/competitors.md`（人工维护）
- 脚本中**禁止硬编码**任何列表

## 架构

```
scripts/product-repo-card.py    ← 产品日报（从 product-list.md 读取，生成飞书卡片）
scripts/competitor-monitor.py   ← 竞品监控（从 competitors.md 读取，对比快照告警）
references/product-list.md      ← 产品清单唯一数据源
references/competitors.md       ← 竞品清单唯一数据源
references/competitor-snapshot.json ← 竞品历史快照（自动生成）
references/product-quality-v6-control-system.md ← v6评分/权限/字段映射/灰度计划
references/nightly-product-evolution-pipeline.md ← 夜间审计→修复→日报闭环
references/community-template.md ← 社群招募标准模板
references/pitfalls.md          ← 踩坑记录（详细排障见此文件）
```

⚠️ **脚本路径**：cron只接受 `~/.hermes/scripts/` 下的真实文件（不接受symlink）。skill脚本需`cp`到该目录。

## 执行步骤

### References

- `references/visual-design-audit-methodology.md` — 视觉设计需求审计方法论：7大类分类体系、优先级定义、去重合并规则、输出模板。当需要为品牌/产品系统性梳理视觉设计需求时使用。
- `references/product-quality-v6-control-system.md` — v6 产品质量控制系统：100分基础交付分、P0-P4业务进化优先级、S0-S4夜间自动化权限、字段映射和灰度落地计划。
- `references/audit-scoring-formula.md` — 旧10分制与v6 100分制并行口径；解释当前脚本输出，同时定义下一版评分目标。
- `references/nightly-product-evolution-pipeline.md` — 夜间只读审计、S1/S2低风险修复、竞品融合候选、早餐日报证据链。
- `references/cron-verification-gate.md` — 产品日报/竞品日报/审计门禁的 cron 配置、手动触发、输出文件和明早可用性验收流程。

## 产品日报
```bash
cp /root/.hermes/skills/product-repo-monitor/scripts/product-repo-card.py /root/.hermes/scripts/
python3 /root/.hermes/scripts/product-repo-card.py
```

### 竞品监控
```bash
cp /root/.hermes/skills/product-repo-monitor/scripts/competitor-monitor.py /root/.hermes/scripts/
python3 /root/.hermes/scripts/competitor-monitor.py
```

告警条件：Stars增长≥50 或 3天内有推送。无告警时静默。

### 告警后融合价值判定（防噪声）

日报告警不是融合指令。看到 `🆕 最近3天有更新` 或 `📈 +N⭐` 后，必须先做文件级审计再决定是否融合：

1. 用 GitHub API 拉最近 3 个 commit，并读取 commit detail 的 `files` 列表。
2. 统计 `code_files / doc_files / additions / deletions / sample paths`。
3. 只把新增/修改核心代码模块、API schema、运行时编排、安全分析器、真实 E2E harness、模型/工具适配器列为“可融合”。
4. 纯文档、AGENTS.md、版本 bump、changelog、CI、Star 引导类更新只记录，不触发融合。
5. 输出必须映射到我们的具体产品仓库和模块，不要只写“该竞品值得关注”。

详细判定方法与 2026-07-02 样例见 `references/monitor-driven-fusion-triage.md`。

## Cron 配置

**2026-07-01 重建后的铁律**：监控类 cron 优先使用 `no_agent + script`，避免 LLM 二次总结漂移；数字只能来自脚本 stdout 或 schema-v2 snapshot。

```yaml
# 竞品日报：直接递送脚本 stdout 到飞书
script: competitor-monitor.py
no_agent: true
deliver: feishu

# 产品日报卡片：脚本自行发送飞书交互卡片；cron stdout 只落本地，避免重复消息
script: product-repo-card.py
no_agent: true
deliver: local

# 产品只读审计门禁：早餐日报前生成 audit-report.json，不自动修复
script: audit-products.py
no_agent: true
deliver: local
```

改 cron 后必须按 `references/cron-verification-gate.md` 做真实验收：先备份 `cron/jobs.json`，再手动跑脚本 dry-run/审计，必要时用 `hermes cron tick --accept-hooks` 触发 due job，最后检查 `last_status`、cron output 和 snapshot/report JSON。

### 产品日报每日一次门禁

用户明确要求：`智械工坊产品仓库日报` 每天只发一次。排查“像一天好几次”时，先确认不是 dry-run/引用噪声，再修 cron 与脚本幂等：

1. cron 层只保留一个产品日报任务：`script=product-repo-card.py`、`no_agent=true`、`deliver=local`、`0 9 * * *`。
2. 脚本层必须有每日幂等 marker：成功发送后写 `/root/.hermes/scripts/product-repo-card-sent.json`；同一天同目标再次运行默认 `[SKIP]`，仅 `PRODUCT_MONITOR_FORCE_SEND=1` 可强制重发。
3. dry-run 绝不能输出“发送成功”，必须输出 `发送未发送（dry-run）`，避免用户误以为又推了一次日报。
4. 运行脚本与 skill 源脚本要同步更新：`/root/.hermes/scripts/product-repo-card.py` 与 `scripts/product-repo-card.py`。

详细排查与验证见 `references/product-daily-idempotency.md`。

快照要求：
- 产品快照：`/root/.hermes/scripts/repo-snapshot.json`，`schema_version=2`。
- 竞品快照：`references/competitor-snapshot.json`，`schema_version=2`。
- 旧 nested/flat 混合快照只能作为兼容读取输入，每次保存必须重写成单一 schema。

## 产品变动操作

| 操作 | 步骤 |
|------|------|
| 新增产品 | 编辑 `references/product-list.md` 添加一行，运行验证 |
| 下线产品 | 修改状态列为 `❌` 或 `🔒 已归档` |
| 改名/换仓库 | 同步修改 `product-list.md` + Bitable + SKILL.md frontmatter + 仓库README |

### 产品改名铁律（2026-06-30）

**改名请求必须立即执行，不能搁置。** 用户说"改成XX名字"时，当场完成全部同步，不要说"稍后处理"。

**改名五步同步**（缺一不可）：
1. `references/product-list.md` — 产品名 + 英文代号列
2. Bitable 项目总览表 — 用 `lark-cli base +record-batch-update` 更新"产品名称"字段
3. 产品仓库 `SKILL.md` — frontmatter 的 `name:` 和 `description:` 字段
4. 产品仓库 `README.md` — 标题和品牌名
5. `product-repo-card.py` — 如果脚本内有硬编码的产品名映射

**Pitfall: 上下文压缩后丢失改名请求**
用户在对话中给出改名指令但 session 被 compaction 后，原始指令可能丢失。预防措施：
- 收到改名请求时**立即执行**，不要等到"批量处理"
- 如果用户问"为什么没改名"，直接承认丢失并当场执行，不要花时间搜索历史
- `session_search` 搜产品名可能找不到改名指令（因为 compaction 后原文被摘要替代）

**验证**：改名后用 `grep -rn '旧名字' /root/.hermes/skills/产品仓库/` 确认零残留。

新增分类时，同步更新 `references/competitors.md`。

### 版本号管理

每次产品改动后必须更新版本号，三方同步（SKILL.md ↔ Bitable ↔ product-list.md）：

| 改动类型 | 版本变更 | 示例 |
|---------|---------|------|
| 新增代码模块 | Minor (x.y.0) | 1.0.0 → 1.1.0 |
| 文档/格式优化 | Patch (x.y.z) | 1.0.0 → 1.0.1 |
| 破坏性变更/重写 | Major (x.0.0) | 1.0.0 → 2.0.0 |

**同步流程**：
1. 确定新版本号（按改动力度）
2. 更新SKILL.md的`version:`字段（去掉引号，统一semver格式）
3. 更新Bitable的`文档版本`字段（用lark-cli api PUT）
4. 交叉验证：从零clone读SKILL.md ↔ lark-cli读Bitable

```bash
# Bitable版本更新
lark-cli api PUT "/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/{record_id}" \
  --data '{"fields": {"文档版本": "v1.1.0"}}'

# 交叉验证
lark-cli api GET "/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records" --params '{"page_size":50}'
```

**铁律**：版本号不更新 = 改动未记录。SKILL.md和Bitable版本号必须一致。

## 17. Commit Message 卫生检查（2026-06-22）

产品仓库commit历史是公开的。发现以下关键词时报警并用 `git reset --soft` + `amend` 清理：
```
清除 | 清理 | 原作者 | clean author | remove author | brand residual
```

## 竞品融合增强工作流

当日报竞品监控发现显著增长（Stars+100或关键功能更新）时，可触发融合增强。

### 融合流程

1. **研究阶段**：用 `web_extract` 抓取竞品 README，提取核心架构/能力/API设计
2. **匹配阶段**：将竞品能力映射到我们产品，选 Top 5 最高价值融合对
3. **编码阶段**：每个融合创建 2-4 个 Python 模块，放在产品仓库的 `modules/<主题>/` 目录
4. **推送阶段**：clone → 复制文件 → git add → commit → push
5. **验证阶段**：从零clone验证文件在正确位置

### 模块目录规范

| 融合主题 | 模块目录 | 示例 |
|----------|---------|------|
| 多Agent编排 | `modules/crew/` | role_orchestrator.py, flow_engine.py |
| 研究流水线 | `modules/research/` | research_planner.py, parallel_researcher.py |
| 图像控制 | `modules/controlnet/` | control_processors.py, control_fusion.py |
| NLP管道 | `modules/nlp/` | ner_analyzer.py, text_classifier.py |
| 结构化输出 | `modules/structured_output/` | structured_generator.py, output_validator.py |

### Commit规范

```
feat: <竞品名>融合 - <能力1>+<能力2>+<能力3>
```

### Pitfall: 多仓库推送分支差异

不同产品仓库的默认分支不统一（main vs master）。推送时必须：
```bash
# 先尝试main，失败则尝试master
git push origin main 2>&1 || git push origin master 2>&1
```

**铁律**：不能只试一个分支名。`product-list.md` 中的"默认分支"列记录了正确值，优先使用。

详细流程和代码模板见 `references/competitor-fusion-workflow.md`。

## Pitfall: 多仓库推送分支差异

不同产品仓库默认分支不统一（main vs master）。`canvas-design` 用 master，`barren-order` 用 main。

**错误模式**：只试 `git push origin main`，master 分支仓库静默失败。

**正确做法**：
```bash
# 方案1：从 product-list.md 查默认分支
grep "canvas-design" references/product-list.md  # → master

# 方案2：自动回退
git push origin main 2>&1 || git push origin master 2>&1
```

**铁律**：推送后必须验证（从零clone确认文件存在），不能只信 push 输出。

## SKILL.md 审计修复模式

当审计脚本报 `looks_like_readme: true` 或 `has_technical: false` 时。

### 审计脚本精确正则（`scripts/audit-products.py`）

| 检测项 | 正则 | 触发扣分的关键词 |
|--------|------|-----------------|
| `looks_like_readme` | `(Getting Started\|Installation\|Quick Start\|Overview)` (IGNORECASE) | 英文章节标题 |
| `has_technical` | `^##\s+(技术架构\|Technical\|Architecture\|算法\|Pipeline)` | 需要精确章节标题 |
| `has_workflow` | `^##\s+(工作流\|Workflow\|Steps\|步骤\|流程)` | 需要精确章节标题 |

### 诊断信号
- `skill_md.looks_like_readme: true` → SKILL.md 含 `Quick Start`/`Getting Started`/`Overview`/`Installation`
- `skill_md.has_technical: false` → 缺少 `## 技术架构`/`## Technical` 等精确章节标题

### 修复操作清单（按优先级）

1. **消除 `looks_like_readme`**：`## Quick Start` → `## 快速开始`（最常见触发原因）
2. **补 `## 技术架构`**：模块表 + Pipeline 流水线描述（正则要求精确标题）
3. **保留**：frontmatter（name/description/triggers/version/metadata）
4. **替换**：模板套话工作流 → 真实的分步工作流（带命令和参数）
5. **新增**：`## Pitfalls` 章节（3-6条实战踩坑）
6. **删除**：营销引用（"融合自 X"/"对标 Y"/Stars 数字）

### 反面教材

```markdown
# ❌ 模板套话（审计会判为 README）
## 工作流
- [ ] 1. 确认用户需求和使用场景
- [ ] 2. 加载相关代码和配置
- [ ] 3. 执行核心功能
- [ ] 4. 验证输出结果
- [ ] 5. 反馈给用户

# ✅ 真实工作流（审计通过）
## 工作流
### Step 1: 需求确认
| 分支 | 触发词 | 入口脚本 |
|------|--------|----------|
| 完整流水线 | "处理视频" | scripts/pipeline.py --all |
| 仅下载 | "下载视频" | scripts/video_download.py |
```

### 营销引用清理铁律

SKILL.md/README.md 中禁止出现：
- `融合自 <竞品名>` → 改为功能描述
- `Stars` 数字引用 → 只写在 Bitable
- 竞品对标表 → 只写在 competitors.md

## Dead Repo 清理

日报报404时，必须同步更新**4个文件**：

| 文件 | 作用 |
|------|------|
| `references/competitors.md` | 竞品清单（competitor-monitor.py 自动读取） |
| `scripts/product-repo-card.py` | 产品日报的 COMPETITORS 字典 |
| `product-portfolio-competitive-fusion/references/product-repo-mapping.md` | 产品-竞品映射 |
| `references/competitor-snapshot.json` | 删除对应条目 |

**铁律**：替换仓库前必须 `gh search repos` 验证存在，不用猜测的owner/repo。

## GitHub Pages 产品矩阵

**仓库**：`503496348-ops/atomcollide-product-matrix`
**详细流程**：见 `product-ops` skill 第二部分"产品矩阵网站维护"

产品变动时同步更新 `index.html`：产品卡片、统计数字、分类计数、商业引擎层级。

**设计标准**：对标 Linear/Vercel 级世界级设计。详细设计模式和差距诊断见 `frontend-optimization` skill 的 `references/world-class-web-design-patterns.md`。

HTML 编辑铁律：
- 新增卡片在 `.cards-row` 容器内（按分类分区，不在统一网格）
- 禁止 sed 删 HTML 区块，用 Python 结构性修改
- 验证标签平衡
- CTA 按钮必须链到永不失效的资源（知识库首页，不是群链接）

默认发送到飞书群 `[REDACTED_CHAT_ID]`（智械工坊群）。

## 产品质量审计（v6 控制系统）

自动化审计脚本：`scripts/audit-products.py`（当前仍输出 Legacy 10 分制 baseline）
审计方法论：`references/audit-methodology.md`（含语言感知技术特性检查）
竞品覆盖分析：`references/competitor-gap-analysis.md`
评分控制系统：`references/product-quality-v6-control-system.md`（100分基础交付分、P0-P4优先级、S0-S4夜间权限、字段映射、灰度计划）
夜间产品进化流水线：`references/nightly-product-evolution-pipeline.md`（夜间审计完整度/小白开箱/依赖/竞品差距，低风险自主修复，并把昨夜真实动作纳入早餐日报）

```bash
cp /root/.hermes/skills/product-repo-monitor/scripts/audit-products.py /root/.hermes/scripts/
python3 /root/.hermes/scripts/audit-products.py
```

当前脚本审计维度（Legacy 10分）：SKILL.md质量(25%) + README(10%) + 代码质量(25%) + 技术特性(20%) + 模板残留(20%)。
下一版 v6 审计维度（100分）：Skill/文档契约(15) + 一键开箱(20) + 代码可用性(20) + 测试与验证(20) + 依赖与环境(10) + 安全与卫生(10) + 产品化与数据同步(5)。
**评分公式详解**：见 `references/audit-scoring-formula.md`。

### v3 严格模式变更（2026-06-23）

| 检查项 | 旧版（宽松） | v3（严格） |
|--------|-------------|-----------|
| has_workflow | 匹配散落关键词`步骤`/`流程`/`执行` | 只匹配`## 工作流`/`## Workflow`等章节标题 |
| has_technical | 匹配任意位置的`技术`/`架构`/`API` | 只匹配`## 技术架构`/`## Technical`等章节标题 |
| frontmatter | `content.startswith("---")` | 有行号前缀(`1\|---`)时判为失败，并报告🔴 |
| grade判定 | 用原始浮点值比较（7.95 < 8 → B） | 先`round(total, 1)`再比较（8.0 >= 8 → A） |

### Post-Push 验证协议（强制）

**铁律：push完不算完，从零clone验证才算完。**

```python
# 1. push后立即从零clone验证
subprocess.run(['git','clone','--depth','1',f'https://github.com/{org}/{repo}.git', tmpdir])

# 2. 检查6项（缺一不可）
checks = {
    'frontmatter': content.strip().startswith('---'),
    'triggers': 'triggers:' in content,
    '工作流': bool(re.search(r'^## 工作流|## Workflow', content, re.M)),
    '技术架构': bool(re.search(r'^## 技术架构|## Technical', content, re.M)),
    '无行号': not bool(re.search(r'^\d+\|', content, re.M)),
    'references': bool(re.search(r'references/|📖', content)),
}

# 3. 验证git log确认commit在正确分支上
curl -s "https://api.github.com/repos/{org}/{repo}/commits?per_page=1"
```

### product-list.md 分支名审计（关键）

**product-list.md中的分支名直接驱动审计脚本的clone行为。** 列表写`master`但实际用`main` → 审计脚本clone到旧内容 → 读到过时的SKILL.md/README → 评分不准。

发现分支名错误时必须**立即修正product-list.md**，不能只修仓库。

```bash
# 批量检查所有产品的实际默认分支
for repo in $(grep -oP 'github.com/[^/]+/\K[^.]+' references/product-list.md); do
    branch=$(git ls-remote --symref "https://github.com/503496348-ops/$repo.git" HEAD | grep -oP 'refs/heads/\K\S+')
    echo "$repo: $branch"
done
```

**铁律**（详见 `references/pitfalls.md`）：
- 必须检查所有代码文件类型（.py/.ts/.tsx/.js/.go/.rs/.java等），不能只检查.py（#18）
- 技术特性检测必须语言感知（TS/JS项目用前端检查项，Python项目用后端检查项）（#23）
- SKILL.md必须有YAML frontmatter + triggers字段，否则审计扣分
- "拼凑感"通常来自SKILL.md格式不规范，不是代码质量问题——修复格式即可
- 没有代码的"产品"不是产品——SKILL.md描述的能力必须有对应代码实现
- 修复后必须从零clone验证，不能用缓存目录（#24）
- **read_file返回带行号前缀，批量修改文件后必须strip行号再write_file**（#26）
- **workflow正则必须覆盖"工作流"+"Checklist"+"- [ ]"格式**（#27）
- **template拼凑感检查只扫描SKILL.md和README，不扫代码文件**（#28）
- **批量git push后必须验证每个repo的push结果**（#29）
- **产品仓库名以product-list.md为准，不凭记忆猜测**（#30）
- **git push前必须确认远程默认分支名（main vs master）**（#31）
- **产品补强必须按评分公式精准施策，不能盲目堆代码**（#32）
- **竞品驱动增强必须有实际代码产出，不是文档优化**（#33）
- **gh repo create 不会自动设置 git remote** — push 前必须 `git remote add origin <url>`（#43）
- **delegate_task 并发限制为1** — 竞品融合等并行任务优先用 execute_code 自己写，不要 delegate（#44）
- **SKILL.md 质量修复不能只改格式** — 必须重写工作流为具体步骤，加技术参考和 Pitfalls 章节（#45）
- **诊断≠修复，推送≠生效，脚本通过≠内容完整**（#34）
- **审计脚本关键词匹配太宽松 → 改为章节标题检查**（#35）
- **product-list.md分支名错误 → 审计clone到旧内容 → 评分虚高**（#36）
- **浮点精度：7.95 round=8.0但grade用7.95判定 → 先round再判定**（#37）
- **read_file行号污染：read_file返回N|content，直接write_file会写入行号**（#38）
- **批量push后必须逐个从零clone验证，不能只信push输出**（#39）
- **批量融合推送时只试一个分支名**（必须从product-list.md读分支）（#43）
- **commit前检查diff非空**（文件复制失败会导致空commit）（#43）（#40）
- **审计脚本不检查version字段**（#41）
- **改动后忘记升版本号：版本更新是"完成定义"的一部分**（#42）
- **install.sh 必须支持 --auto 无交互模式，否则智能体调用会卡死**（#46）
- **新产品 install.sh 输出结构化数据（---OUTPUT_START---标记），方便智能体解析**（#47）
- **__pycache__ 必须加入 .gitignore，否则会提交编译缓存**（#48）
- **竞品融合后代码中不得出现竞品仓库名/Stars/作者名**（#49）
- **产品日报脚本禁止硬编码竞品清单和 GitHub Token**（#55）：`product-repo-card.py` 必须从 `references/competitors.md` 读取竞品；GitHub 认证只能使用 `GITHUB_TOKEN` 环境变量或 `gh auth token`，不得在脚本中写入 `ghp_...`。修改后用 `py_compile` + 模块导入验证分类数/仓库数与 `competitors.md` 一致。
- **产品日报脚本必须有真 `--help` / `--dry-run`（#56）**：任何 `--help` 查询不得触发飞书发送；`--dry-run` 必须等同 `PRODUCT_MONITOR_DRY_RUN=1`，只生成卡片/快照并打印 `[DRY_RUN]`。修改或部署 `product-repo-card.py` 后必须执行：`python3 -m py_compile ...`、`python3 product-repo-card.py --help`、`PRODUCT_MONITOR_DRY_RUN=1 python3 product-repo-card.py`，确认 help 不发送、dry-run 不发送。
- **Bitable product sync 解析必须按真实 shape（#57）**：`lark-cli base +record-list --format json` 可能返回 `{data:{fields, field_id_list, data, record_id_list}}`，其中 `data.data` 是行数组而非 records dict。必须用 `dict(zip(fields, row))` 映射字段；按 GitHub 仓库 URL 精确包含 `/503496348-ops/<repo>` 定位记录，禁止用宽泛 `英文代号 in set` 造成三条记录交叉匹配。三条不同动态/版本必须逐条 `+record-batch-update` 单 record patch，不要用同值批量更新。
- **Python f-string 禁止反斜杠（#54）**：`f"[{t.get(\"key\", \"\")}]"` 在 Python ≤3.11 报 `SyntaxError: f-string expression part cannot include a backslash`。修复：改用字符串拼接 `"[" + str(t.get("key", "")) + "]"` 或先提取变量再插值。**竞品融合模块写完必须 `py_compile` 逐文件验证**，不能只看语法高亮。
- **write_file 截断陷阱（#50）**：`read_file` 有行数上限（~500行），读到的只是文件片段。对片段做 patch 替换后用 `write_file` 回写 = 把截断内容写回，丢失大半文件。正确做法：用 `execute_code` 里的 Python 字符串拼接生成完整 HTML/大文件再写入，永远不要基于 `read_file` 片段做修改
- **Python ≤3.11 f-string 反斜杠（#54）**：f-string `{}` 内不能有反斜杠（`f"{d[\"k\"]}"` → SyntaxError）。写完必须 `py_compile`。修复：变量提取（`v=d["k"]; f"{v}"`）或字符串拼接
- **飞书知识库标题获取（#51）**：`feishu_doc_read` 在非飞书上下文不可用；`curl` 抓不到 SPA 渲染的标题。唯一可靠方法：`browser_navigate` 到飞书 wiki URL → 从返回的 `page.title` 提取真实标题（格式：`标题 - Feishu Docs`）

## 产品质量门禁

**详细流程见 `product-quality-gate` skill**

每次产品变动（新增/下线/改名）必须过5项检查：
1. SKILL.md有YAML frontmatter + triggers字段
2. 仓库有实际代码（≥100行，全语言检测）
3. 模板残留≤5处
4. 仓库可访问性（用git clone验证，不只看API）
5. Bitable记录数 = product-list.md产品数（过滤空记录）

**铁律**：发现异常必须修复或报告，不能静默跳过。完成前必须从零clone验证。

## 新产品创建

详细流程见 `references/new-product-checklist.md`。
竞品融合增强流程见 `references/competitor-fusion-workflow.md`。
SKILL.md 质量修复见 `references/skill-md-quality-fix.md`。

## 详细排障

详细排障见 `references/pitfalls.md`（43条）+ `references/pitfalls-part2.md`（4条）+ `references/pitfalls-part3.md`（3条：#52 Bitable优先、#53 lark-cli参数、#54 f-string反斜杠）

### Bitable 数据解析踩坑

程序化读取 Bitable 记录时的两个关键陷阱，详见 `references/bitable-parsing-pitfalls.md`：
- **JSON字段顺序错位**：`--format json` 的值顺序由 `field_id_list` 决定，不是 `+field-list` 名称顺序。必须用 `id_to_name = dict(zip(field_ids, fields_meta))` 映射。
- **Markdown管道符断裂**：默认 markdown 格式中，字段值含 `|` 时列解析错位。程序化解析必须用 `--format json`。
- Bitable表ID变化、lark-cli格式问题
- GitHub API限流处理策略
- 分支名不统一（main vs master）
- raw.githubusercontent.com CDN缓存
- 已归档仓库无法推送
- 社群信息grep模式不统一
- Commit Message卫生检查
- **审计脚本只检查.py文件**（必须覆盖.ts/.tsx/.js等）
- **SKILL.md是README伪装**（必须有triggers/workflow）
- **空壳仓库需要实现代码**（不能只有文档）

## 竞品融合增强

详细方法论见 `references/competitor-fusion-methodology.md`。

流程：竞品研究（并行 web_extract）→ 融合匹配 → 代码实现（modules/ 目录）→ 推送 → 报告。

## 新产品创建

详细模板见 `references/new-product-template.md`。

关键：SKILL.md 必须有 frontmatter + triggers + 工作流 + 技术参考 + Pitfalls。install.sh 必须支持 `--auto` 无交互模式。

## 竞品覆盖度

竞品覆盖：**21/21 分类全覆盖**（2026-06-24 新增知识管理）。竞品仓库详见 `references/competitors.md`。

## Bitable 产品同步

当需要新增产品到 Bitable 或检查三端一致性时，使用 `references/bitable-product-sync.md` 工作流。

关键信息：
- base-token: `[REDACTED_BASE_TOKEN]`
- 项目总览表: `[REDACTED_TABLE_ID]`
- 产品分类字段 ID: `[REDACTED_FIELD_ID]`

### 数据查询：优先 Bitable

**用户要产品信息（仓库链接、能力描述、分类等）时，直接从 Bitable 拉，不要逐个抓 GitHub README。** Bitable 是权威数据源，字段齐全（产品名称、GitHub仓库、能力描述、最新动态、竞品对标等），一次 API 调用全部拿到。

```bash
# ✅ 正确：一次拉全部产品数据
lark-cli base +record-list --base-token [REDACTED_BASE_TOKEN] --table-id [REDACTED_TABLE_ID] --as bot --limit 50

# ❌ 错误：逐个抓 README（慢、不全、可能 404）
# for repo in repos: web_extract(f"https://raw.githubusercontent.com/.../{repo}/main/README.md")
```

### lark-cli Bitable 命令速查

| 命令 | 用途 |
|------|------|
| `lark-cli base +record-list --base-token X --table-id Y --as bot --limit N` | 列出记录 |
| `lark-cli base +field-list --base-token X --table-id Y --as bot` | 列出字段 |
| `lark-cli base +record-batch-create --base-token X --table-id Y --as bot --json '{...}'` | 批量创建 |
| `lark-cli base +record-batch-update --base-token X --table-id Y --as bot --json '{...}'` | 批量更新 |

⚠️ **注意**：`+record-list` 默认输出 markdown 表格（不是 JSON）。如需 JSON 解析，加 `--format json`。用管道接 `python3 -c "json.load(sys.stdin)"` 前必须确认输出是 JSON。

**踩坑**：
- `--app-token` ❌ → `--base-token` ✅
- `--page-size` ❌ → `--limit` ✅
- `bitable` ❌ → `base` ✅
- `records list` ❌ → `+record-list` ✅

新增产品前必须检查产品分类选项是否存在，不存在时先 `+field-update` 添加选项。
