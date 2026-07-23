# 深度审计：AIPMAndy/dna-memory → 仓内 Memory 融合评估

**审计日**：2026-07-23  
**本地 clone**：`/tmp/audit-dna-memory`  
**HEAD**：`ba38e7ed2e916c2d131457becae8a50ba8bd4901`（`ba38e7e` docs: clarify cognitive memory strategy，2026-07-22）  
**许可**：Apache-2.0  
**Stars / 语言**：86⭐ / Python  
**本地验收**：`pytest tests/test_policy.py tests/test_memory_value.py tests/test_unified_memory.py tests/test_hermes_adapter.py` → **16 passed**

---

## 1. 仓库定位

跨客户端（Codex / Claude Desktop / Hermes）统一的**认知型记忆内核**：

- **Markdown 为 Source of Truth**，SQLite 为索引
- MCP 工具面：`memory_remember` / `memory_recall` / `memory_feedback` / `memory_get`
- 写入门禁：敏感内容策略、容量、类型校验
- 认知类型 + `supersedes` 冲突链 + useful/misleading 反馈
- Hermes 会话 SQLite 只读导入（`import_hermes_sessions.py`）
- 蒸馏 / 压缩 / memory_value 指标 / 多 Agent 适配器

不是「又一个向量 RAG」，而是**可审计、可替代、可跨端同步的结论记忆**。

---

## 2. TOP 能力清单（对照仓内）

| # | 外部能力 | 证据路径 | 仓内现状 | 增量 | 优先级 |
|---|----------|----------|----------|------|--------|
| 1 | Markdown SoT + SQLite 索引 + reindex | `scripts/markdown_memory.py`, `memory_service.py` | fact_store + MEMORY.md + cards；无统一 Markdown SoT 跨端 | 高：跨 Codex/Claude/Hermes 共享结论 | **P0** |
| 2 | `supersedes` 原子替换链 | `MemoryService.remember` 写旧 meta→superseded | fact_store 有 supersede；Markdown/MEMORY 层弱 | 高：多端结论冲突可追踪 | **P0** |
| 3 | MCP 工具面 + Hermes `mcp add` 文档 | `scripts/memory_mcp.py`, `docs/mcp-and-client-adapters.md` | Hermes 原生 fact_store/memory 工具；缺跨客户端统一 MCP 记忆服务 | 高：与「多 Agent 记忆不通」直接对齐 | **P0** |
| 4 | Hermes session 只读导入 | `scripts/import_hermes_sessions.py`（schema 校验+proposal） | session_search / 手工 consolidation | 中：可作导入适配参考 | **P1** |
| 5 | useful/misleading 反馈进 recall 排序 | `memory_service.recall` CTE feedback_scores | fact_feedback + memory-write-gate | 中：排序公式可对齐 | **P1** |
| 6 | 蒸馏 / 压缩 / cold archive | `memory_distillation.py`, `memory_compression.py` | memory-consolidation + L5 archive | 中：脚本化批处理可借鉴 | **P1** |
| 7 | memory_value 多窗口指标 | `memory_value.py` | memory-write-gate 质量报告 | 中：诊断面板 | **P1** |
| 8 | bounded extraction（≤3/session, 800 chars） | README / dna-memory-loop skill | 写入门槛 6 信号 | 低-中：策略可对齐 | **P2** |
| 9 | 多客户端 adapter 探测 | `agent_adapter.py` | 无统一跨端 adapter 层 | 中 | **P1** |

---

## 3. 承载产品映射（读 product-list + SKILL，不猜名）

| 外部模块 | 承载产品 | 依据 | 融合形态 |
|----------|----------|------|----------|
| 记忆健康/冲突/膨胀诊断 | **hermes-doctor** | product-list「智能体上下文映射补位A」；已有 sandbox/runtime diagnostics | 新增 memory integrity / supersede-chain / capacity 诊断模块（领域化命名，去 dna 品牌） |
| 记忆修复处方 | **pipixia-doctor** | 已有 RX-MEM-001/002；snapshot MEMORY | 处方：supersede 冲突、Markdown/index 漂移、反馈闭环缺口 |
| 上下文完整性 / fleet 审计 | **mindriver** | 已有 `MemoryStore`、context integrity（duplicate/empty） | 扩展：跨客户端 client 维度、feedback_score、supersede 状态 |
| Vault/Markdown 索引健康 | **neverend** | vault_index SQLite + link health | Markdown SoT 索引/孤儿/路径策略可对齐（非整仓搬迁） |
| Skill 层 SOP | **memory-management / memory-consolidation / memory-write-gate-system** | 五层模型、落卡、6 信号 | 协议级对齐：认知类型、supersedes 字段、跨端 clients 标签 |

**禁止新建产品**；增量回填现有仓 + shared skills。

---

## 4. 与仓内 Memory 栈差距（结论优先）

| 维度 | 仓内（Hermes Kingdom） | dna-memory | 裁定 |
|------|------------------------|------------|------|
| 长期事实 | fact_store + MEMORY 索引 + cards | Markdown 文件 SoT | 互补：仓内更贴 Hermes 运行时；dna 更强跨端 SoT |
| 写入门禁 | 6 信号 write gate | policy + capacity + type | 可融合策略清单 |
| 冲突 | fact supersede | Markdown supersedes 链 + 默认不召回旧条 | **应吸收** |
| 反馈 | fact_feedback useful/unhelpful | useful/misleading → recall rank | **应吸收排序** |
| 跨端 | 弱（各 profile 隔离） | 一等公民 clients[] + MCP | **核心缺口** |
| 蒸馏 | consolidation cron | batch distill/compress CLI | 可借鉴批处理 |
| 许可 | — | Apache-2.0 | **可代码级融合**（需去品牌、通用化） |

---

## 5. 推荐融合步骤（不执行代码改造于本拍；只定案）

1. **P0 协议对齐（shared skill）**  
   - 在 `memory-management` / write-gate 增加可选字段：`clients[]`, `supersedes[]`, `cognitive_type`, `status∈{active,superseded,archived}`  
   - 与 fact_store supersede API 映射表写进 references  
2. **P0 诊断面（hermes-doctor）**  
   - `diagnostics/memory_cross_client_integrity.py`：检测 MEMORY/cards/fact_store 三端 ID 漂移、superseded 仍被热载、容量告警  
3. **P0 修复面（pipixia-doctor）**  
   - RX-MEM-00x：supersede 未闭环、index 丢文件、反馈全空  
4. **P1 mindriver**  
   - context integrity 增加 client/feedback/supersede 维度  
5. **P1 neverend**  
   - vault_index 可选「memory-frontmatter 契约」扫描  
6. **P2**  
   - 可选 MCP sidecar 包装 fact_store（**不要**整仓 vendoring dna-memory；接口兼容即可）

**不做**：把 dna-memory 整仓 fork 成新产品；不引入其品牌叙事。

---

## 6. 状态裁定

| 字段 | 值 |
|------|-----|
| status | `pending_review` |
| triage | `可融合候选` |
| score | **8** |
| category | `智能体上下文` |
| products | `hermes-doctor`, `pipixia-doctor`, `mindriver`, `neverend` |
| decision | `deep_audit_2026-07-23_p0_cross_client_memory` |

---

## 7. 证据命令摘要

```text
clone: /tmp/audit-dna-memory @ ba38e7e
LICENSE: Apache-2.0
pytest: 16 passed (policy/value/unified/hermes_adapter)
core: memory_service.remember/recall/supersedes; import_hermes_sessions; memory_mcp; markdown_memory
```
