# Wave-7 POC 设计提取（接续）

基于你要求“继续融合增强”，按 `pending_review` 高价值项，先给出可执行的 POC 设计。

> 数据口径与当前执行状态约束保持不变：
> - 只做最小增量增强，不改主架构口径
> - 每项先给出 `入口 / 验收命令 / 回退点`
> - 先走 `build-fusion-enhancement-plan.py --validate` + `ops-product-monitor-orchestrator.py --with-audit --with-fusion-plan --dry-run`

---

## 1) EverMind-AI/Raven → `hermes-doctor` / `pipixia-doctor` / `mindriver`

### 结论
**Raven 的关键增益点不在“单工具替换”，而在“记忆+技能编排能力的标准化抽象”，可用于三个仓库的能力护城河增强。**

### 可复用锚点（来自 Raven）
- `MemoryBackend` 抽象，支持 `recall/store/feedback/start/stop`（`raven/memory_engine/backend.py:102-119`）
- `Curator` 具备上下文编排、manifest 与工作态重构能力（`raven/context_engine/curator.py`）
- `Memory` 合同测试可落地（`raven/memory_engine/contract_test.py`）
- `SkillHubClient` 具备 4 步分离式技能读取流程（搜索/取 body/下载 zip；统一 envelope）
- `providers` 已有多模态 provider 插件模型（`raven/providers/*`）支持 MiniMax 等 provider 扩展

### POC 目标（最小闭环）
在不改现有主链路的前提下，实现 `hermes-doctor` 的三件事：
1. **可选外部记忆后端接口层**（不替换原有存储）
2. **技能源“按需发现-按需下载”协议样例**（只读/离线安全）
3. **医生脚本可观测增强**（在 `scripts/doctor.py` 中新增一条可执行检查）

### POC 具体设计

#### A. `hermes-doctor` / `pipixia-doctor`
- 新增 `scripts/raven_bridge.py`
  - 定义轻量 `RavenLikeMemoryBackend` 协议类（内部可复用 `memory_engine/backend.py` 的 `Memory` 字段语义）
  - 目标方法：`recall(query, user_id, top_k)`、`store(session_id, messages)`、`feedback(payload)`。
  - 初始实现先使用 `FileBackend`（本地 JSON/JSONL）作为回归安全默认；`provider` 字段保留为后续切换到真实 Raven 的扩展点。
- 新增 `scripts/memory_bridge.py`
  - 封装 `raven` 风格记忆适配器的 I/O 格式（`Memory` + metadata）
  - 兼容未来 `raven.provider` 字段映射，避免后续打桩成本
- 修改 `scripts/hermes_doctor.py`（或 `scripts/doctor.py`）
  - 新增 `--check=raven-bridge`，输出结构化报告（命中条数、回放顺序、top_k 限制）
  - 把报告接入现有 `doctor` 的 JSON 汇总 schema（兼容现有采集脚本）

#### B. `mindriver`
- 新增 `scripts/memory_bridge.py`（同一接口）和 `scripts/memory_smoke.py`
- 在 `scripts/doctor.py` 增加“记忆桥接自检”项：`PY` bridge 协议可 parse/read/write，不泄露 token

### 验收（Wave-7 建议验收）
1. 先在 `hermes-doctor` 执行：
   - `python scripts/doctor.py --check`（回归现有项）
   - `python scripts/raven_bridge.py --smoke --repo hermes-doctor`
2. 在 `pipixia-doctor` 执行同上
3. 在 `mindriver` 执行：
   - `python scripts/doctor.py --check`（现状）
   - `python scripts/memory_smoke.py --input tests/fixtures/sample_turn.json`

### 回退
- 新增文件独立存在；不改现有主流程导入，回退只需移除新增文件并清理命令开关。

---

## 2) OpenCut-app/OpenCut → `ideasphere` / `fractovision`

### 结论
OpenCut 当前仓内已有“Editor API/Plugin-first/Desktop/Headless/Cloudflare API”方向信号（`README` + `apps/api` + `apps/web` + `apps/desktop`）。更适合先做“只读/触发器”级 PoC：
- 不接入完整编辑器编辑状态
- 只接入“任务提交->状态轮询->结果取回”最小服务能力

### 关键锚点
- OpenCut 重写声明：Editor API / plugin-first / MCP / headless（README: status lines）
- API 入口骨架：`apps/api/src/index.ts`（仅 health/echo）可作为最小网关扩展点
- Desktop 当前为 GPUI 外壳，Web/Api 有清晰路由边界

### POC 目标
在 `ideasphere` 增加外部视频任务接入的可观测桥：
- 通过 OpenCut REST 创建裁剪任务（或返回 mock）
- 通过状态轮询拿到任务结果摘要
- 提供统一诊断端点

### POC 具体设计（最小闭环）
- `ideasphere/scripts/opencut_bridge.py`（新增）
  - `submit_job(payload)`：将 `source`,`start`,`duration`,`style` 写成统一请求结构
  - `poll_status(job_id)`：统一重试 + 超时策略
  - `download_or_summary(job_id)`：返回“可见产物元信息”而非直接下载大文件
- `ideasphere/scripts/doctor.py`
  - 新增条目：`diag_opencut_bridge`，做
    - env 变量存在性
    - API 基础连通（可配 mock）
    - 本地任务生命周期（submit -> poll -> resolve/error）
- 可选 `fractovision` 侧增加 `scripts/comfyui_workflow_bridge.py` 的简化适配：
  - 将 OpenCut 输出元信息转为本地“任务摘要”格式，供后续视频流程链路消费

### 验收
1. `python scripts/doctor.py --check`（ideasphere）通过原有项
2. 新增 `python scripts/opencut_bridge.py --smoke --mode mock` 通过
3. `python scripts/doctor.py --check=opencut_bridge` 可见三段式状态

### 回退
- 全部为新增文件与可选 `doctor` 条目；回退只删新增文件并恢复 `doctor.py` 分支。

---

## 3) Nutlope/hallmark（建议同步进入 Wave-7.2）

### 结论
Hallmark 并非“渲染增强”而是“反 AI 模板化规则治理”。它对我们的仓库价值高在：
- 与现有 `anti_ai_style_guard` 的规则重叠，但覆盖范围更系统（结构/移动端/微交互/节奏/拒绝规则）
- 可作为“审美与可读性基线增强”（轻量化，不改功能模型）

### POC 目标（下一小步）
给 1 个仓库（`nichecraft`）加可开关的**Hallmark 规则集合引用**，与现有 `style guard` 做分层联合：
- Level0：现有 `anti_ai_style_guard`（当前）
- Level1：hallmark 规则（引用 `skills/hallmark` 的 anti-pattern、microinteractions 片段）

### POC 设计
- `nichecraft/scripts/hallmark_bridge.py`（新增）
  - 读取本地 `~/.cache` 或仓内 vendor 的 hallmark 规则快照（不在运行时访问网络）
  - 输出结构化命中码：`hallmark_anti_patterns`, `motion_corpus`, `responsive_blocks`
- `nichecraft/scripts/doctor.py`
  - 新增 `diag_hallmark_bridge` 检查项（默认 OFF，可配置）
  - 与现有 `anti_ai_style_guard` 并行，避免破坏既有规则阈值

### 验收
1. 默认开关 OFF 时，原有 doctor 不变
2. 开启标志时新增项可独立执行，且不得阻断主路径
3. 未命中任何现有关键阈值（`doctor` 总分不下降）

### 回退
- 删除 `scripts/hallmark_bridge.py` 并从 `doctor` 移除该入口

---

## Wave-7 当前建议（按你的“继续”立即执行）

### 已完成：
- 生成上述 POC 设计清单（Raven + OpenCut + Hallmark 预备）
- 将实现从“重改代码”降级为“分层可执行 PoC 入口”

### 下一步按钮（选一个）：
1. **先落地 Raven POC（优先级最高）**
2. 或先落地 OpenCut POC（与视频链路可直连）

若你确认，我下一条直接开始**执行 Raven 的最小代码版 POC**（新增 bridge + doctor 检查 + smoke），然后马上跑：
- `python3 scripts/build-fusion-enhancement-plan.py --validate`
- `python3 scripts/ops-product-monitor-orchestrator.py --with-audit --with-fusion-plan --dry-run`
