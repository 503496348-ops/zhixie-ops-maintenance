# 审计评分公式详解

## 当前状态

`audit-products.py` 当前仍保留旧 10 分制五维评分，适合做仓库规范化 baseline；v6 已把目标升级为“产品真实交付控制系统”。

因此本文件分两层使用：

1. **Legacy 10 分制**：解释现有脚本输出，避免早餐日报和历史报告失去可读性。
2. **v6 100 分制**：作为下一版夜间产品进化流水线的目标评分口径。

详细控制系统见 `references/product-quality-v6-control-system.md`。

---

## Legacy 10 分制公式（当前脚本）

```text
total = skill_md × 0.25 + readme × 0.10 + code × 0.25 + tech × 0.20 + template × 0.20
```

等级划分：A≥8.0, B≥6.0, C≥4.0, D≥2.0, F<2.0。

### 各项评分细则

#### SKILL.md 质量（满分 12 分，归一化到 10）

| 检查项 | 分值 | v3 严格模式检测方式 |
|---|---:|---|
| YAML frontmatter | +2 | `content.strip().startswith("---")` 且无行号前缀（`^\d+\|`） |
| triggers 字段 | +3 | `"triggers:" in content` |
| workflow 章节 | +3 | 章节标题 `^## 工作流/Workflow/Steps/步骤/流程` |
| 技术架构章节 | +2 | 章节标题 `^## 技术架构/Technical/Architecture/算法/Pipeline` |
| 非 README 风格 | +2 | 不含 `Getting Started/Installation/Quick Start/Overview` |

#### README（满分 10 分）

基于安装、使用示例、内容长度做粗粒度评估。

#### 代码质量（满分 10 分）

| 检查项 | 分值 | 条件 |
|---|---:|---|
| 文件数≥10 | +3 | 代码扩展名：.py/.ts/.tsx/.js/.go/.rs/.java 等 |
| 文件数≥3 | +1 | 与上一项互斥 |
| 代码行数≥1000 | +3 | 与 100 行项互斥 |
| 代码行数≥100 | +1 | 与 1000 行项互斥 |
| 代码行数≥10000 | +2 | 额外加分 |
| 有 >50 行真实代码文件 | +2 | `any(cf["lines"] > 50 for cf in code_files)` |

#### 技术特性（满分 10 分）

8 项特征检测，每命中一项 +1：API 集成、数据处理、机器学习、Web 框架、数据库、文件处理、CLI 工具、测试。

#### 模板残留（满分 10 分）

只扫描 SKILL.md 和 README.md，不扫代码文件。命中 `example.com / your.api.key / REPLACE_ME / placeholder` ≥3 个才扣分：

```text
score = max(0, 10 - count × 2)
```

### Legacy 10 分制的边界

旧评分只能说明“仓库看起来像不像一个规范产品仓”，不能说明：

1. install.sh 是否真能无交互跑通；
2. README 命令是否会卡死或误发送外部消息；
3. pytest/npm test 是否存在并通过；
4. fresh clone 是否能复现；
5. 产品是否有竞品能力差距；
6. 夜间自动化是否应该动手修。

所以旧 A 级不等于可交付，只能作为 baseline。

---

## v6 100 分制公式（目标口径）

```text
delivery_score =
  skill_contract × 0.15 +
  open_box × 0.20 +
  code_runtime × 0.20 +
  tests_verification × 0.20 +
  dependencies_env × 0.10 +
  security_hygiene × 0.10 +
  product_sync × 0.05
```

所有子分统一为 0–100，再按权重合成。输出分数必须来自脚本 JSON，不允许 LLM 重算或润色数字。

### v6 维度定义

| 维度 | 权重 | 通过标准 | 关键失败信号 |
|---|---:|---|---|
| skill_contract | 15 | SKILL.md 有 frontmatter/triggers/工作流/技术架构/Pitfalls/Quickstart | README 伪装 skill、缺触发词、工作流泛泛 |
| open_box | 20 | install.sh --auto、doctor/check、CLI --help、dry-run 可执行 | 安装交互卡死、help 触发发送、无 env.example |
| code_runtime | 20 | 有真实代码入口，py_compile/npm build 通过 | 空壳、只有文档、入口脚本不存在 |
| tests_verification | 20 | pytest/npm test/smoke/fresh clone 通过 | 无测试、测试失败、本地过远端不过 |
| dependencies_env | 10 | requirements/pyproject/package.json/系统依赖声明完整 | 依赖缺失、版本冲突、隐藏凭据 |
| security_hygiene | 10 | token/外部引用/运行产物/危险 commit 清零 | ghp/sk/open_id、竞品名/作者/Stars 残留、__pycache__ |
| product_sync | 5 | product-list/Bitable/SKILL/README/版本一致 | 仓名大小写错、Bitable 幽灵记录、版本未同步 |

### v6 等级

| 等级 | 分数 | 含义 | 早餐日报口径 |
|---|---:|---|---|
| A | ≥85 | 可对外交付 | 健康，只报增量风险 |
| B | 70–84 | 基本可用，有短板 | 可夜间修 S1/S2 |
| C | 55–69 | 可用性不足 | 列 P1/P2 修复项 |
| D | 35–54 | 不适合交付 | 红区，禁止包装成完成 |
| F | <35 | 空壳/不可用/安全风险 | P0，优先修或下架 |

---

## 业务进化优先级（P0–P4）

基础分回答“能不能交付”，优先级回答“今晚要不要动”。

| 优先级 | 触发条件 | 动作 |
|---|---|---|
| P0 | install/test/入口失败；疑似泄密；公开不可用 | 立即修复或报告 |
| P1 | B/C/D/F 且存在明确可自动修复项 | 夜间 S1/S2 自动修复 |
| P2 | 竞品真实代码更新映射到我方短板 | 生成融合候选，默认请示 |
| P3 | 文档/版本/Bitable/README/SKILL 不一致 | 自动同步或生成差异报告 |
| P4 | 健康且无变化 | 静默，不消耗 token |

## 自动化权限映射（S0–S4）

| 权限 | 允许 | 禁止 |
|---|---|---|
| S0 | 只读审计、生成报告 | 写文件/push/外发 |
| S1 | 文档、示例、env.example、版本口径 | 改代码逻辑/API |
| S2 | install.sh、doctor、smoke test、小 bug | 大重构/删功能 |
| S3 | 独立模块融合、本地验证、受控 push | 未验证直接 push |
| S4 | 大重构、删除功能、改 cron/provider/API key | 夜间自动执行 |

默认夜间只自动执行 S0–S2；S3 先报候选，S4 必须用户确认。

## v6 输出字段要求

`nightly-product-audit.json` 每个产品至少包含：

```json
{
  "repo": "canonical-repo-name",
  "branch": "main",
  "delivery_score": 0,
  "grade": "F",
  "priority": "P0",
  "allowed_action_level": "S0",
  "checks": {},
  "evidence": [],
  "issues": [],
  "recommended_actions": []
}
```

早餐日报只能引用这些字段，不得临时从自然语言里提数。

## 迁移策略

1. Phase 0：文档/schema 对齐，不改 cron。
2. Phase 1：v6 只读审计与旧 10 分制并行 3 天。
3. Phase 2：开放 S1/S2 自动修复，必须写 ledger。
4. Phase 3：S3 竞品融合先本地验证并请示。
5. Phase 4：早餐日报汇总真实动作、失败验证和待批准事项。
