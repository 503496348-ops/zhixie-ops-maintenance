# Wave-1 候选复核（二拍）

执行时间：2026-07-23（本拍）

## 1) 复核范围
本拍处理 `pending_review` 可融合候选中的后2位：
- `langgenius/dify`
- `excalidraw/excalidraw`

## 2) 基础状态校验
- `competitor-candidate-pool.json`
  - `langgenius/dify`: `pending_review / 可融合候选 / score=6 / unseen_shas=1 / head_sha=b95d3131`
  - `excalidraw/excalidraw`: `pending_review / 可融合候选 / score=6 / unseen_shas=1 / head_sha=53732f08`
- `build-fusion-enhancement-plan.py --validate`：`total_candidates=26`，结构仍与上一拍一致（可融合 15 / 观察5 / 仅记录6）
- 运行链路绿灯（同拍）
  - 产品日报：`25产品 / 24有仓 / 总⭐82`
  - 竞品日报：`分类21 / 44 / 成功44 / 错误0`
  - 编排器：`4/4` 成功

## 3) `langgenius/dify` 初筛
### 最近 3~4 次关键提交（`gh api /repos/langgenius/dify/commits/{sha}`）
- `4da4fa72`（12:54）：改动集中在 `api/core/app/apps/agent_app/app_generator.py`（14+）、`api/services/agent/composer_service.py`（新增/调整）、以及 2 个单测文件（agent app 解析相关）
- `8853ed99`（12:44）：前端 header 组件小改动
- `34a5ca19`（12:00）：新增/调整 `knowledge_fs` 相关 API controller 与 openapi 文档（含 `api/controllers/console/knowledge_fs_proxy.py`）
- `b95d3131`（21日）：E2E 步骤变更 + 大量非接口脚本（UI 文案）

### 初筛结论
- `dify` 侧近期提交中，已出现**真正的后端应用/Agent生成与知识FS能力相关改动**（`app_generator`, `composer_service`），且有单测同步，具备“直接复用 API/服务能力”潜力。
- 目标产品 (`hermes-doctor`, `pipixia-doctor`) 均具备 `API集成/机器学习/Web框架/数据库/CLI/测试` 等能力闭环，与 `dify` 的部分 agent 应用生成链路存在接口抽象接入可能。
- 判定：**建议推进到 Wave-1 深度复核（可执行级）**，优先级可与 `crewAIInc/crewAI` 同步进行。

### 建议动作（可执行）
1. 拉取 `dify` 最新 `main` 的 `agent_app` 与 `composer_service` 对比产物，抽取可复用组件（尤其是 `tool` 调度与对话流拼装）
2. 生成最小对齐文档（输入 schema、返回 schema、错误码）
3. 做 `hermes-doctor` 侧 smoke：新建一个最小 agent 调用路径验证

## 4) `excalidraw/excalidraw` 初筛
### 最近 4 次关键提交
- `e6ae6bf0`、`91b78903`、`a3b90897`、`53732f08`
- 变更文件基本集中在前端画布/几何引擎：
  - `packages/element/src/*.ts`
  - `packages/element/src/utils.ts`
  - `packages/excalidraw/components/App.tsx`
  - `packages/math/src/curve.ts`
  - 以及 tests/snapshots 与部分 SCSS

### 初筛结论
- 当前可见为**前端交互与几何计算修复/微调**，没有看到明确的 `api` 或服务层输出可直接复用的落地钩子。
- 目标产品为 `nichecraft`，更偏飞书白板/PPT 生成链路。
- 判定：**暂归为“继续观察/待价值验证”层**，不直接纳入当下 Wave-1 首批落地。

### 建议动作（可执行）
1. 若后续必须复核：继续检查是否近期存在 `app/renderer` 导出 API 或导出 pipeline 的公开接口层提交（当前样本未覆盖）
2. 以 `pending_review` 保持，等待其他高优先候选（如 crewA I）形成可复用接口锚点后再推进

## 5) 本拍结论
- `langgenius/dify`：**进入 Wave-1 深度复核候选**
- `excalidraw/excalidraw`：**保持 pending_review，暂缓一拍**

## 6) 下一拍执行队列
- `huggingface/transformers`
- `scrapy/scrapy`

---
本拍只做外部仓 commit 类型与可复用面向性初筛，未改写 candidate 池状态。