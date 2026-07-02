# 智械工坊 OPS 维护：本地技能融合图谱

## 已融合

1. `product-quality-gate`：把“一键开箱可用”变成产品仓库发布门禁，要求 setup/doctor/smoke/test 与远端干净 clone 复验。
2. `product/product-ops`：吸收产品全生命周期运营、矩阵/Bitable/仓库对齐、竞品融合后去污染纪律。发布版只保留方法，所有租户连接标识均使用 `[REDACTED_*]`。
3. `cron-failure-three-layer-diagnosis`：把 cron 故障排查固定为配置层、执行层、依赖层三层诊断，并加入 no_agent token hygiene。
4. `nightly-evolution-reflection`：加入夜间审计前置自检、artifact 验证、系统健康快照。
5. `competitor-fusion`：加入监控告警后的文件级 triage、反向融合与外部引用零残留验证。

## 不直接合并

- `lark/bitable-management-system`：只保留 Bitable 同步原则，不打包真实租户命令。
- `daily-report`：日报排版方法可参考，但产品日报数字由脚本生成，禁止 LLM 改写。
- `memory-write-gate-system`：记忆治理与 OPS 日报相邻但职责不同，不并入主流程。

## 触发分流

- 产品/竞品/cron/仓库门禁 → 本技能。
- 具体 Bitable 表设计 → `lark-base` / `bitable-management-system`。
- 外部竞品仓深度融合 → 先用本技能 triage，再进入 `competitor-fusion`。
