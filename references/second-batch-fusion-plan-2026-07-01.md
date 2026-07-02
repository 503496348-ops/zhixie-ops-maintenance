# 第二批竞品融合排期（2026-07-01）

## 已做前置核验

- 已从零 clone 第二批目标仓库并读取目录结构：`nichecraft`、`easyrhythm`、`blastogene`、`barren-order`、`herpeakgem`。
- 第二批进入按能力线排期状态，避免把白板、客服、多 Agent、教育、知识同步几个方向混成一锅粥。

## P1-A 白板与画布能力

目标产品：`nichecraft`

已确认可落点：
- `scripts/canvas_state.py`
- `scripts/excalidraw_svg.py`
- `scripts/diagram_builder.py`
- `references/canvas-formats.md`
- `references/svg-image-embedding.md`

融合方向：元素状态归一、SVG 导出兼容、擦除/工具切换状态机、画布对象 schema、页面/shape 版本迁移、交互状态快照。下一轮提交建议：`feat: strengthen canvas state pipeline`。

## P1-B 智能客服与群运营

目标产品：`easyrhythm` + `blastogene`

已确认可落点：
- `easyrhythm/python-backend/memory_store.py`
- `easyrhythm/python-backend/server.py`
- `blastogene/classifier.py`
- `blastogene/workflow_engine.py`
- `blastogene/alerter.py`

融合方向：静态输入 schema、array/object 参数克隆、客服流转节点校验、CRM 字段映射、工单交接摘要、群消息分类、风险告警、工作流触发条件。下一轮提交建议：`feat: harden support workflow schemas`。

## P1-C 多 Agent 协作编排

目标产品：`barren-order` + `mindriver`

已确认可落点：
- `barren-order/scripts/workflow_engine.py`
- `barren-order/scripts/message_router.py`
- `barren-order/scripts/shared_memory.py`
- `mindriver/mindriver/temporal_graph.py`

融合方向：flow step helper、任务输入输出契约、agent card、消息路由、发言权限边界、任务分解、角色协同、共享环境状态。下一轮提交建议：`feat: add agent workflow contract checks`。

## P1-D 教育与知识管理

目标产品：`herpeakgem` + `neverend`

已确认可落点：
- `herpeakgem_cli/book.py`
- `herpeakgem_cli/notebook.py`
- `herpeakgem_cli/kb.py`
- `herpeakgem_cli/memory.py`
- `neverend/scripts/sync_auditor.py`

融合方向：学习路径、题目/反馈结构、学生状态跟踪、同步端到端验收、冲突检测、知识库变更审计。下一轮提交建议：`feat: add learning and sync verification contracts`。

## 第二批执行顺序

1. `nichecraft`：画布状态与 SVG round-trip。
2. `easyrhythm` + `blastogene`：客服流转 schema 与社群告警规则。
3. `barren-order`：多 Agent workflow contract。
4. `herpeakgem` + `neverend`：教育反馈结构与知识同步验收。

## 门禁

- 先看目标仓库现有模块，再写入。
- 每个目标至少 1 个核心模块 + 1 个测试。
- 禁止 README/SKILL.md 写竞品来源表。
- 禁止竞品品牌、作者、URL 残留。
- `py_compile` + pytest。
- 从零 clone 验证。
- Bitable 最新动态逐条 `+record-batch-update` 同步。
