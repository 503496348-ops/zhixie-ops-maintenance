# 智械工坊 OPS 维护 Runbook

## 1. 每日链路

```text
08:45 产品只读审计门禁 → audit-products.py → audit-report.json
09:00 产品仓库日报卡片 → product-repo-card.py → repo-snapshot.json → 飞书卡片
09:00 竞品仓库监控日报 → competitor-monitor.py → competitor-snapshot.json → stdout
```

## 2. Cron 三层诊断

1. 配置层：job 是否 enabled、schedule 是否正确、script 是否存在、no_agent 是否符合任务性质、deliver 是否会重复发送。
2. 执行层：手动 `cronjob(action=run)` 或 `hermes cron tick --accept-hooks` 后检查 output 文件、exit code、`Mode: no_agent (script)`、stdout 是否非空。
3. 依赖层：GitHub API/gh auth、lark-cli、Python 依赖、网络、磁盘空间、快照文件可写性。

## 3. no_agent token hygiene

- 确定性监控/同步/健康检查使用 `no_agent=true + script`。
- stdout 必须是最终可读结果；脚本要捕获异常并 exit non-zero。
- 保留 provider/model 字段不等于会调用 LLM；判断以 `no_agent` 和 cron output header 为准。

## 4. 夜间审计自检

夜间任务只做 S0–S2：只读审计、文档/示例/doctor/smoke 小修。S3 竞品融合默认生成候选和验证证据后请示；S4（改 cron/provider/API key/gateway/大重构）禁止自动执行。

## 5. 完成定义

- 有真实脚本输出。
- 有 JSON/schema 或 Markdown artifact。
- 有敏感信息扫描结果。
- 有远端干净 clone 或部署态脚本哈希一致性验证。
- 没有用"LLM 总结"替代事实源。

---

## 6. 融合增强链路（v1.1）

### 6.1 产品质量门禁（融合 v6 评分体系）

**目的**：把 `audit-products.py` 的 10 分制简单评分升级为 v6 交付控制系统。

**融合来源**：
- `references/product-quality-v6-control-system.md` — 完整的 v6 评分体系（100 分制）
- `references/repository-release-checklist.md` — 发布门禁
- `references/new-product-checklist.md` — 新产品检查清单

**执行链路**：
```text
audit-products.py (现有 10 分制)
    ↓ 输出 audit-report.json
v6 评分引擎 (新增)
    ↓ 计算：基础交付分(0-100) + 优先级(P0-P4) + 自动化权限(S0-S4)
nightly-product-audit.json (目标产物)
    ↓
早餐日报汇总
```

**验收标准**：
- 产品总数 = product-list.md
- repo 名 = GitHub canonical（禁止猜大小写）
- 无旧快照诈尸
- 输出 JSON 符合 `product-quality-v6-control-system.md` 定义的 schema

### 6.2 Cron 健康度监控（融合三层诊断法）

**目的**：把 cron 任务的健康度纳入日报，自动诊断失败原因。

**融合来源**：
- `cron-failure-three-layer-diagnosis` 技能（三层诊断法：配置层→执行层→依赖层）

**执行链路**：
```text
cron job 执行
    ↓ 成功/失败
诊断引擎
    ↓ 三层诊断
    ├─ 配置层：job 是否 enabled、schedule、script 路径
    ├─ 执行层：exit code、stdout/stderr、超时
    └─ 依赖层：GitHub API、lark-cli、Python 依赖、磁盘
诊断报告
    ↓
早餐日报"任务健康度"板块
```

**验收标准**：
- 每个 cron 任务有健康度标记（✅/⚠️/❌）
- 失败任务自动生成诊断报告
- 不盲目重试，先定位根因

### 6.3 竞品融合分诊（融合 monitor-driven-fusion-triage）

**目的**：把竞品监控的告警转化为可执行的融合候选清单。

**融合来源**：
- `references/competitor-fusion-methodology.md` — 融合方法论
- `references/competitor-fusion-workflow.md` — 融合工作流
- `references/monitor-driven-fusion-triage.md` — 监控驱动的融合分诊

**执行链路**：
```text
competitor-monitor.py
    ↓ 输出 competitor-snapshot.json
分诊引擎
    ↓ 过滤：只保留核心代码/API schema/运行时/测试 harness 变更
    ↓ 映射：关联到具体产品和模块目录
    ↓ 评分：代码变化评分 + 产品匹配度
融合候选池
    ↓ 输出 competitor-candidate-pool.json
早餐日报"竞品融合候选"板块
```

**验收标准**：
- 候选必须满足 5 个条件（见 `product-quality-v6-control-system.md` 竞品驱动融合判定）
- 不触发融合：纯 README、AGENTS、CI、changelog、版本 bump、Star 增长但无代码变更
- 默认先本地验证后请示

### 6.4 统一编排器

### 6.5 融合增强执行清单（候选与验收闭环）

**目的**：把竞品分诊候选变为可执行清单（含建议动作与验收链路）。

**执行链路**：
```text
competitor-monitor.py（含分诊）
    ↓ competitor-candidate-pool.json
build-fusion-enhancement-plan.py
    ↓ fusion-enhancement-execution-plan.md/json
ops-product-monitor-orchestrator.py --with-fusion-plan
    ↓ 引导任务分配与验收闭环
```

**产物**：
- `references/fusion-enhancement-execution-plan.md`
- `references/fusion-enhancement-execution-plan.json`

**验收标准**：
- 优先级 top 候选至少包含 `可融合候选` 中的可执行项（当前 9 项）
- 产出后触发 `python3 scripts/audit-products.py` 验证 `products_with_issues {}`
- 审计/日报与候选清单保持同口径（25 产品与 44 竞品）


**脚本位置**：`scripts/ops-product-monitor-orchestrator.py`

**用法**：
```bash
# 完整运行（含发送）
python3 scripts/ops-product-monitor-orchestrator.py

# Dry-run 模式（只读，不发送）
python3 scripts/ops-product-monitor-orchestrator.py --dry-run

# 含产品质量审计（耗时较长）
python3 scripts/ops-product-monitor-orchestrator.py --with-audit --with-fusion-plan --dry-run
```

**输出产物**：
- `references/orchestrator-run-result.json` — 结构化执行结果
- `references/orchestrator-summary.md` — 人类可读摘要

**验收标准**：
- 所有步骤成功时 exit code = 0
- 存在失败步骤时 exit code = 1
- 输出包含关键指标摘要（产品数、分类数、成功检查数、总⭐）
