# brightdata/competitive-intelligence

- 目标状态：`pending_review -> implementation-ready`
- 口径：`commit 语义复核 + 接口映射 + 前端模板提取`
- 入口 Commit：`1ac94e30b2276da5883eae9bf8c967bd22e15e67`
- 映射产品：`energsolve`

## 1) API/调度层
- 源文件：`api/app.py`, `api/ci_agent.py`, `api/README_API.md`
- 抽取能力：任务提交、轮询、超时重试、失败回溯
- 对接目标：`energsolve/services/competitive_insight_orchestrator.py`
- 验收命令：
  - `pytest -q tests/test_competitive_orchestrator.py`
  - `python -m pytest tests/test_competitive_orchestrator.py::test_retry_policy`
  - `python -m pytest tests/test_competitive_orchestrator.py::test_timeout_fallback`

## 2) API 契约层
- 源文件：`api/__init__.py`, `api/README_API.md`, `api/app.py`
- 抽取能力：create_job / poll_job / result / health 四端点契约
- 输出：`energsolve/docs/competitor_api_contract.md`
- 验收命令：
  - `python /root/projects/zhixie-ops-maintenance/scripts/audit-products.py --check-product energsolve | tail -n 20`

## 3) 前端模板层
- 源文件：`ci-agent-ui/src/App.tsx`, `ci-agent-ui/src/components/CompetitiveIntelligenceForm.tsx`, `ci-agent-ui/src/components/DemoScenarios.tsx`
- 抽取能力：输入参数面板、场景选择、结果展示、错误态
- 输出：`energsolve/components/competitive-intel-query-template.tsx`
- 验收命令：
  - `npm -C energsolve/web test -- --runInBand`

## 回退点
- 删除 `energsolve` 增量层与映射配置，恢复旧交互调用。

## 下一拍动作
- 先提交 mapping 文档与两条 smoke（成功、超时），再做 implementation PR。