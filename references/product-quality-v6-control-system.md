# Product Quality v6 Control System — 产品质量评分与夜间进化控制系统

## 定位

v6 把旧版“仓库规范化合规分”升级为“产品真实交付控制系统”。它不是给仓库贴一个好看的 A/B/C 标签，而是决定：

1. 产品能不能对外交付；
2. 早餐日报应该汇报哪些真实风险和昨夜动作；
3. 夜间自动化最多能动到哪一层，哪些动作必须请示；
4. 竞品更新是否值得融合，而不是被 README、CI、Star 噪声牵着跑。

## 双层评分模型

### 第一层：基础工程交付分（A/B/C/D/F）

回答一个问题：**这个产品现在能不能作为正式产品交付？**

总分 100 分，所有数字必须来自确定性脚本、GitHub API、测试输出、fresh clone 验证结果，禁止 LLM 改写分数。

| 维度 | 权重 | 核心问题 | 关键证据 |
|---|---:|---|---|
| Skill/文档契约 | 15 | Agent 能否按 SKILL.md 直接执行 | frontmatter、triggers、工作流、技术架构、Pitfalls、Quickstart |
| 一键开箱 | 20 | 小白/Agent 能否从零安装运行 | install.sh --auto、doctor/check、CLI --help、dry-run |
| 代码可用性 | 20 | 不是空壳，核心逻辑可执行 | 代码文件/行数、入口脚本、py_compile/npm build、核心 smoke |
| 测试与验证 | 20 | 缺陷能否被自动化捕捉 | pytest/npm test、端到端样例、fresh clone 复验 |
| 依赖与环境 | 10 | 环境声明是否完整且不阻塞 | requirements/pyproject/package.json、env.example、无交互安装 |
| 安全与卫生 | 10 | 是否存在泄密/外部引用/运行产物污染 | token grep、竞品名/作者/Stars 零残留、__pycache__、危险 commit |
| 产品化与数据同步 | 5 | 是否与产品矩阵/Bitable/版本一致 | product-list、Bitable、版本号、README/SKILL 一致 |

等级：

| 等级 | 分数 | 含义 | 默认动作 |
|---|---:|---|---|
| A | ≥85 | 可对外交付 | 只观察，记录增量风险 |
| B | 70–84 | 基本可用，有文档/开箱短板 | 夜间可自动修 S1/S2 |
| C | 55–69 | 有可用性短板，需要计划修 | 生成修复计划，低风险项可修 |
| D | 35–54 | 不适合对外交付 | 标为重点修复，不允许包装成“已完成” |
| F | <35 | 空壳/不可用/安全风险 | P0，先修到可运行或下架/归档 |

### 第二层：业务进化优先级（P0–P4）

回答另一个问题：**今晚要不要动，能动多深？**

| 优先级 | 触发条件 | 动作 |
|---|---|---|
| P0 | install/test/核心入口失败；疑似泄密；公开链接不可用 | 立即修复或报告，进入早餐日报红区 |
| P1 | B/C/D/F 且存在明确可自动修复项 | 夜间 S1/S2 自动修复，必须验证 |
| P2 | 竞品出现真实核心代码更新，且映射到我方明确短板 | 生成融合候选，默认先本地验证后请示 |
| P3 | 文档/版本/Bitable/README/SKILL 不一致 | 自动同步或生成差异报告 |
| P4 | 健康仓库、无新风险 | 只记录状态，不消耗 Agent token |

## 夜间自动化权限 S0–S4

| 等级 | 允许动作 | 禁止动作 | 验收 |
|---|---|---|---|
| S0 | 只读审计、生成 JSON/Markdown 报告 | 写文件、push、发外部消息 | 输出 evidence paths |
| S1 | 修 README/SKILL/示例/env.example/版本口径 | 改代码逻辑、改 API | grep + markdown lint + diff |
| S2 | 补 install.sh --auto、doctor、smoke test、小 bug | 大重构、删功能、改公开接口 | py_compile/test/fresh clone |
| S3 | 竞品融合新增模块并 push | 未经验证直接 push；残留外部引用 | 本地验证 + 去污染 + fresh clone；默认早报请示 |
| S4 | 大重构、删除功能、改 cron/provider/API key | 夜间自动执行 | 必须用户确认 |

默认策略：夜间只自动执行 S0–S2；S3 先产出候选和本地验证证据；S4 禁止上夜车。

## 字段映射：脚本 JSON → 早餐日报

建议产物路径：

```text
/root/.hermes/skills/product-repo-monitor/references/nightly-product-audit.json
/root/.hermes/skills/product-repo-monitor/references/nightly-evolution-ledger.json
/root/.hermes/skills/product-repo-monitor/references/nightly-verification-ledger.json
```

### nightly-product-audit.json

| 字段 | 类型 | 来源 | 说明 |
|---|---|---|---|
| schema_version | int | 脚本常量 | 固定为 1，禁止混 schema |
| generated_at | iso datetime | 脚本 | 生成时间 |
| products_total | int | product-list.md | 产品总数 |
| products[] | array | 审计循环 | 每个产品一条 |
| products[].repo | string | product-list.md | 真实 GitHub 仓名，禁止猜大小写 |
| products[].branch | string | product-list.md + git ls-remote | 审计使用分支 |
| products[].delivery_score | int | v6 scoring | 0–100 基础交付分 |
| products[].grade | A/B/C/D/F | scoring | 基础等级 |
| products[].priority | P0–P4 | rules | 夜间处理优先级 |
| products[].allowed_action_level | S0–S4 | policy | 自动化权限上限 |
| products[].checks | object | commands | 各项检查布尔/分数 |
| products[].evidence | array | commands | clone 路径、测试输出摘要、API 响应 key |
| products[].issues | array | rules | 风险清单，带 severity |
| products[].recommended_actions | array | rules | 明确到文件/命令的动作 |

### nightly-evolution-ledger.json

记录昨夜真实动作，不能写“计划”。

| 字段 | 类型 | 说明 |
|---|---|---|
| action_id | string | 时间戳+repo+动作类型 |
| repo | string | 产品仓库 |
| action_level | S0–S4 | 实际动作等级 |
| action_type | string | audit/fix/doc_sync/test_added/fusion_candidate/fusion_push |
| files_changed | array | 实际改动文件 |
| commands_run | array | 实际执行命令摘要 |
| verification | object | 测试/fresh clone/grep 结果 |
| pushed | bool | 是否 push |
| needs_user_approval | bool | 是否需要用户批准下一步 |

### nightly-verification-ledger.json

早餐日报只汇总验证过的事实。

| 字段 | 类型 | 说明 |
|---|---|---|
| repo | string | 产品仓库 |
| py_compile | pass/fail/na | Python 语法 |
| unit_tests | pass/fail/na | 测试 |
| install_auto | pass/fail/na | install.sh --auto |
| cli_help | pass/fail/na | CLI --help |
| dry_run | pass/fail/na | dry-run 是否不发送外部消息 |
| fresh_clone | pass/fail/na | 从远端干净 clone 验证 |
| external_residue_grep | pass/fail/na | 外部竞品名/作者/Stars/GitHub URL 零残留 |

## 竞品驱动融合判定

竞品日报只提供信号，不等于融合指令。

进入融合候选必须同时满足：

1. 最近 commit 的 files 列表显示核心代码/API schema/运行时/测试 harness 变更；
2. 该能力能映射到我方一个具体产品和模块目录；
3. 我方存在明确短板或增强收益；
4. 预计可做成独立模块，不需要大改公开 API；
5. 有明确验收：测试、去污染、fresh clone、版本/Bitable/SKILL/README 同步。

不触发融合：纯 README、AGENTS、CI、changelog、版本 bump、Star 增长但无代码变更。

## 灰度落地计划

### Phase 0：文档与 schema 对齐

- 更新 `audit-scoring-formula.md`、`nightly-product-evolution-pipeline.md`、SKILL.md 索引。
- 不改 cron，不 push 产品仓，不引入自动写操作。

### Phase 1：只读 v6 审计

- 新增/改造脚本输出 `nightly-product-audit.json`。
- 与旧 10 分制并行 3 天，早餐日报只展示 v6 分布和 P0/P1，不自动修。
- 验证：产品总数 = product-list.md；repo 名 = GitHub canonical；无旧快照诈尸。

### Phase 2：S1/S2 自动修复

- 只修文档、env.example、install.sh --auto、smoke test、小 bug。
- 每次动作写 ledger。
- 必须跑 py_compile/test/fresh clone/grep。

### Phase 3：S3 受控融合

- 竞品融合先只生成候选和本地验证证据。
- 经用户授权后才 push。
- 稳定后可把“新增独立模块+完整验证”的低风险融合纳入自动 push 白名单。

### Phase 4：治理闭环

- 早餐日报展示：健康分布、昨夜真实动作、失败验证、P0/P1、需要批准事项。
- 低价值重复项静默；无变化不制造噪声。

## 完成定义

一次 v6 夜间增强闭环完成，必须同时满足：

1. 审计 JSON 存在且 schema_version 固定；
2. 产品数量、仓库数量、分类数量与 product-list/competitors 源一致；
3. 所有分数来自脚本字段，不来自 LLM 改写；
4. 每个 P0/P1 有 evidence 和 recommended_actions；
5. 所有自动修复动作有 ledger 和验证结果；
6. 早餐日报能说明“昨夜实际做了什么”，而不是只报 GitHub 数字。
