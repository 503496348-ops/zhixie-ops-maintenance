# brightdata/competitive-intelligence 实施任务清单

## 任务1：scheduler service 适配
- 目标：实现 `energsolve/services/competitive_insight_orchestrator.py`
- 输入：`api/app.py`, `api/ci_agent.py`
- 子任务
  1. 任务提交/轮询/超时重试逻辑映射
  2. 失败回溯与结果持久化策略
  3. 日志与告警字段对齐
- 成功标准：新增/更新对应 smoke

## 任务2：api contract
- 目标：`energsolve/docs/competitor_api_contract.md`
- 交付：
  - create_job
  - poll_job
  - result
  - health
  - 错误码映射（参数、429、超时）
  - 幂等键约定

## 任务3：前端模板
- 目标：`energsolve/components/competitive-intel-query-template.tsx`
- 要点：
  - 参数面板
  - 场景选择
  - 结果卡片
  - 错误态展示

## 本拍后置条件
- 所有任务均形成可回滚点：删除新增文件与适配层恢复旧调用链。
- 下拍执行前补齐 evidence（命令输出片段）后标注 `pending_review` -> `implemented`。
