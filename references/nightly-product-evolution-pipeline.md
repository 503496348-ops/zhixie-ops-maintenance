# Nightly Product Evolution Pipeline — 夜间产品进化流水线

## 触发场景

当用户希望产品仓库日报不只报 GitHub 数字，而是在夜间空闲时主动审计、修复、研究竞品差距并把结果纳入早餐日报时，使用本流程。

## 目标

把产品日报从“被动统计”升级为“夜间作战记录”：

- 夜间审计每个产品仓库的完整度、可用性、依赖、小白开箱体验。
- 发现产品与竞品的能力差距。
- 在安全门禁内自动修复低风险问题。
- 对竞品融合只做有证据、有代码、有测试、有从零 clone 验证的增强。
- 早餐日报汇报昨夜真实动作和证据，而不是 LLM 改写后的泛泛总结。

完整评分与权限模型见 `references/product-quality-v6-control-system.md`。

## 总体架构

```text
product-list.md / competitors.md
        ↓
L1 确定性审计脚本（no_agent）
        ↓
nightly-product-audit.json  ← v6 delivery_score + P级优先级 + S级权限
        ↓
L2 低风险自动修复器（S1/S2）
        ↓
nightly-evolution-ledger.json + nightly-verification-ledger.json
        ↓
早餐产品日报卡片
```

## L1：确定性审计层（no_agent 纯脚本）

优先用脚本输出 JSON，禁止 LLM 改写数字。审计项：

1. SKILL.md 完整度：frontmatter、triggers、工作流、技术架构、Pitfalls、Quickstart。
2. README 开箱体验：安装、运行、环境变量、示例、故障排查。
3. 依赖完整度：requirements/pyproject/package.json、系统依赖、无交互安装。
4. 可执行性：py_compile、pytest、npm/bun test、install.sh --auto、CLI --help、dry-run。
5. 仓库卫生：__pycache__、外部竞品残留、疑似 token/open_id/link_token、危险 commit message。
6. 数据同步：product-list、Bitable、README、SKILL、版本号是否一致。

产物：

```text
/root/.hermes/skills/product-repo-monitor/references/nightly-product-audit.json
```

## L2：v6 评分与分级层

基础工程交付分使用 100 分制：

| 维度 | 权重 |
|---|---:|
| Skill/文档契约 | 15 |
| 一键开箱 | 20 |
| 代码可用性 | 20 |
| 测试与验证 | 20 |
| 依赖与环境 | 10 |
| 安全与卫生 | 10 |
| 产品化与数据同步 | 5 |

等级：

| 等级 | 分数 | 含义 |
|---|---:|---|
| A | ≥85 | 可对外交付 |
| B | 70–84 | 基本可用，有短板 |
| C | 55–69 | 可用性不足 |
| D | 35–54 | 不适合交付 |
| F | <35 | 空壳/不可用/安全风险 |

业务进化优先级：

| 优先级 | 含义 |
|---|---|
| P0 | 公开不可用、安装失败、测试失败、疑似泄密 |
| P1 | 明确可自动修复的交付短板 |
| P2 | 竞品真实代码更新映射到我方短板 |
| P3 | 文档/版本/Bitable/README/SKILL 不一致 |
| P4 | 健康且无变化，静默 |

## L3：竞品差距研究层（受限 Agent/LLM）

只从两个入口触发：

1. 竞品日报发现最近 3 天真实核心代码变更。
2. 产品审计发现明确短板。

输出必须是“证据 → 对应产品 → 模块 → 验收标准”，不能只写“值得学习”。

示例格式：

```text
竞品: owner/repo
证据: 最近 commit 新增/修改核心代码模块 X
对应产品: <product>
可融合模块: modules/<domain>/...
验收标准: pytest 通过 + 外部引用零残留 + SKILL/README/版本/Bitable 同步 + fresh clone 验证
```

噪声过滤：纯 README、AGENTS、CI、changelog、版本 bump、Star 引导类更新只记录，不触发融合。

## L4：自主修复/融合权限层

| 等级 | 动作 | 默认策略 |
|---|---|---|
| S0 | 只读审计、生成报告 | 自动 |
| S1 | 修 README/SKILL/示例/env.example/版本口径 | 自动 |
| S2 | 补 install.sh、doctor、smoke test、小 bug | 自动，但必须验证 |
| S3 | 竞品融合新增代码并 push | 默认本地验证后早报请示 |
| S4 | 大重构、删除功能、改公开 API、改 cron/provider/API key | 禁止夜间自动执行 |

默认夜间只自动执行 S0–S2。S3 必须先有本地验证证据，S4 必须用户确认。

## L5：早餐日报增强层

产品日报应合并以下产物：

```text
/root/.hermes/scripts/repo-snapshot.json
/root/.hermes/skills/product-repo-monitor/references/competitor-snapshot.json
/root/.hermes/skills/product-repo-monitor/references/nightly-product-audit.json
/root/.hermes/skills/product-repo-monitor/references/nightly-evolution-ledger.json
/root/.hermes/skills/product-repo-monitor/references/nightly-verification-ledger.json
```

日报结构：

1. 产品矩阵概览：产品数、仓库数、Stars、Issue、健康分布。
2. 昨夜实际动作：审计数、修复数、融合候选数、push 数、fresh clone 验证数。
3. 风险：不可开箱、安装失败、依赖缺失、文档/代码不一致。
4. 竞品差距：真实代码更新 vs README/CI 噪声。
5. 下一步：P0 必修、P1 可增强、需要用户确认的高风险动作。

## 安全门禁

- 所有结论必须带证据路径：repo、commit SHA、测试输出、clone 验证路径、audit JSON 字段。
- 禁止只改文档冒充“能力增强”；竞品融合必须有代码/测试/验证。
- 禁止凭仓库名猜分类；必须读 product-list.md / Bitable / SKILL.md。
- 禁止 LLM 改写数字；数字来自脚本 JSON。
- 竞品融合后外部引用零残留：竞品名、作者、Stars、GitHub URL 不进入产品代码/README/SKILL。
- push 后必须 fresh clone 验证；本地通过不等于远端通过。
- 高风险动作不上夜车：删除功能、改 API、架构重构、改 cron、改 provider、写 API key 必须用户确认。

## 最小落地闭环

### Phase 0：文档/schema 对齐

- 更新本文件、`audit-scoring-formula.md`、SKILL.md 索引。
- 不改 cron，不 push 产品仓，不引入自动写操作。

### Phase 1：只读 v6 审计

- 新增/改造脚本输出 `nightly-product-audit.json`。
- 与旧 10 分制并行 3 天。
- 验证：产品总数 = product-list.md；仓名 = GitHub canonical；无旧快照诈尸。

### Phase 2：S1/S2 自动修复

- 只修文档、env.example、install.sh --auto、doctor、smoke test、小 bug。
- 每次动作写 `nightly-evolution-ledger.json`。
- 必须跑 py_compile/test/fresh clone/grep。

### Phase 3：S3 受控融合

- 竞品融合先只生成候选和本地验证证据。
- 经用户授权后才 push。
- 稳定后可把“新增独立模块+完整验证”的低风险融合纳入自动 push 白名单。

### Phase 4：早餐日报闭环

- 展示健康分布、昨夜真实动作、失败验证、P0/P1、需要批准事项。
- 低价值重复项静默；无变化不制造噪声。

## 完成定义

一次夜间进化闭环完成，必须满足：

1. `nightly-product-audit.json` 存在且 schema_version 固定；
2. 产品数量、仓库数量、分类数量与唯一数据源一致；
3. 所有分数来自脚本字段，不来自 LLM 改写；
4. 每个 P0/P1 有 evidence 和 recommended_actions；
5. 所有自动修复动作有 ledger 和验证结果；
6. 早餐日报能说明“昨夜实际做了什么”，而不是只报 GitHub 数字。
