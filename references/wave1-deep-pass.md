# Wave-1 候选复核（深度复核启动稿）

执行时间：2026-07-23（三拍后续）

> 此稿为“继续”后的下一步，目标：把前两项高优先候选从“语义回放”提升到“接口级可落地判断”。

## 最新语义扫描（补充）
### crewAIInc/crewAI
- 当前池内 head（`competitor-candidate-pool.json`）：`3bb87532...`
- 最近提交序列（含最新 3）：
  - `3bb87532` — dispatch execution_end hook on failed flow executions
  - `6d496f79` — handle async get_agent in load_agent_from_repository
  - `40279e31` — fix dep resolution
- 关键文件（head）
  - `lib/crewai/src/crewai/crew.py`
  - `lib/crewai/src/crewai/hooks/contexts.py`
  - `lib/crewai/src/crewai/flow/runtime/__init__.py`
  - `lib/crewai/tests/hooks/test_interception_conformance.py`

### langgenius/dify
- `competitor-candidate-pool.json` 仍记作 head：`b95d3131...`（历史扫描版本）
- GitHub 最近序列显示池尾之后有 `d5788cc0...` 更新（未进入池头口径的提交）
  - `d5788cc0`（更偏向工具多选输入与 Tool 实体/OpenAPI）
  - `4da4fa72`（agent 端 inline preview draft 刷新）
- 关键文件（`d5788cc0`，新提交）
  - `api/core/tools/__base/tool.py`
  - `api/core/tools/entities/tool_entities.py`
  - `api/openapi/markdown/console-openapi.md`
  - `web/app/components/workflow/nodes/tool/*.ts/.tsx`

## 深度复核判定（初步）
- **crewAIInc/crewAI**：
  - 与当前本地映射入口存在“有重合但不即插即用”状态。先前判定中「可直接评估」的方向保留，但本拍的口径对齐后，优先级下调为**先做最小对接 PoC，再评估是否进入 implementation**。
- **langgenius/dify**：
  - 已出现大量新提交（包括 `d5788cc019`），当前池头滞后。先做候选池口径同步后再进入 implementation 复核。

## 深度复核核验结果（当前拍）

### 关键口径对齐

- `crewAIInc/crewAI`：
  - `competitor-candidate-pool.json` 记录的 `head_sha`：`3bb87532...`
  - GitHub 当前 HEAD：`b14d36bfe4...`
  - `unseen` 差量（按当前 1 页）= **1**（`b14d36bfe4...`）
  - 该提交为依赖/安全类变更（扫描与 parser/tool_usage 小修），未见新增可直接映射到本地 `barren-order` 执行闭环的“业务大改动”。

- `langgenius/dify`：
  - `competitor-candidate-pool.json` 记录的 `head_sha`：`b95d3131...`
  - GitHub 当前 HEAD：`d5788cc019...`
  - `unseen` 差量（当前窗口）= **52**（`d5788cc019...` 起）
  - `d5788cc019` 为新功能增强：`tool multi-select input`，并且触及 `api/core/tools/**`、`web/app/components/workflow/nodes/tool/**`。

### 本地接口层匹配度（已做最小定位）

- `barren-order` 当前存在自研 `Crew/Flow` 执行引擎与角色编排（`modules/crew/flow_engine.py`, `modules/crew/role_orchestrator.py`），
  但与候选 `crewai` 仓库的 `execution_start/END hook` 与 `load_agent_from_repository` 语义未形成一一对应现成入口。
- `hermes-doctor` 与 `pipixia-doctor` 当前为诊断/测试+轻量 API 服务结构，未发现 Dify 风格的 `ToolEntity`/`tool schema`/`workflow` 统一入参模块。
  因而 `dify` 的 commit 价值目前更偏“有意向”而非“可立即落地”。

### 本拍结论

1. `crewAIInc/crewAI`：保留 `pending_review`，并把**差量评审结论**记为“**等待候选池与本地可映射入口对齐后再推进 implementation**”。
2. `langgenius/dify`：先做候选池对齐（将 `head_sha` 更新到最新可复核窗口）再继续深度复核；当前以 `pending_review` 继续。

### 下一步动作（本拍后）

1. 对 `dify` 先做候选池头同步与版本对齐（避免 `head_sha` 与提交实际不一致导致决策漂移）。
2. 对 `crewAIInc/crewAI` 做最小对接 PoC（`load_agent` 异步边界 + 流程失败回流）
   - 目标：确认是否能直接绑定 `barren-order` 的 `Flow/Crew` 观测点。
3. 在 `dify` 完成候选口径同步后，对 `tool multi-select` 的参数转换做本地接口级对接试探。

文件记录：
- `/root/projects/zhixie-ops-maintenance/references/wave1-deep-pass.md`

## PoC 级接口映射验收（本拍完成）

### 结果摘要

- `crewAIInc/crewAI`：本地可观察点与候选钩子仍是**同语义不同形状**，尚未实现可即插即用映射。
- `langgenius/dify`：本地已有 `tool` 回调/跟踪能力，但**不具备 `ToolEntity` 级参数 Schema 入口**，`tool multi-select` 仍需额外封装层。

### 证据（静态 PoC）

#### crewAI
- 远端关键符号（含当前池更新后头）：
  - `ExecutionEndContext / ExecutionStartContext`
  - `Execution/Flow` 运行时（如 `_dispatch_execution_end_failure`、`_set_tasks_callbacks`）
  - `load_agent_from_repository`
- 本地关键符号：
  - `Flow`, `FlowEvent`, `FlowEngine`, `WorkflowExecutor`, `Task`, `AgentRole`
- 关键词重叠（本地/远端）示意：
  - `execution`：2 / 7
  - `on_`：1 / 22
  - `hook`：0 / 2
  - `load_agent`：0 / 1
  - `agent`：1 / 7
  - `failure`：0 / 1
  - `runtime`：0 / 2

#### langgenius/dify
- 远端关键提交（`d5788cc0`）围绕 `tool.py`/`tool_entities.py` 的工具模型/schema 展开。
- 本地检索到的工具观测点在 `hermes-doctor`：`callback_handler.py`, `trace_observability.py`，为执行时回调；`health_scorer.py`。
- 关键词重叠主要停在通用名词（如 `to_dict`），未发现可直接对接 `tool schema` 的实体层命名重叠。

### 最终决策（本拍）

1. `crewAIInc/crewAI`：继续保持 `pending_review`，转入**实现前设计稿阶段**，先定义 `load_agent` 与本地 `Flow/Fallback` 的映射表。
2. `langgenius/dify`：继续保持 `pending_review`，先补齐 `tool` 参数 schema 转换层设计，再决定是否进入 implementation。

### 复测回执（已完成）

- `build-fusion-enhancement-plan.py --validate`：成功。
- `ops-product-monitor-orchestrator.py --with-audit --with-fusion-plan --dry-run`：成功。
- 候选统计保持：26 项（可融合 15 / 观察 5 / 仅记录 6）。