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
- 没有用“LLM 总结”替代事实源。
