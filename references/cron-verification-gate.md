# Cron 验证门禁：产品日报 / 竞品日报 / 审计日报

适用场景：用户要求“改 cron”“明早别故障”“手动触发测试/审计”时。目标不是只看配置存在，而是证明脚本、cron、输出文件和投递策略都真实可用。

## 标准链路

推荐顺序：

1. `08:45` 产品只读审计门禁：`audit-products.py`，`no_agent=true`，`deliver=local`。
2. `09:00` 产品仓库日报卡片：`product-repo-card.py`，`no_agent=true`，`deliver=local`，由脚本自行发送飞书卡片，cron stdout 只本地保存。
3. `09:00` 竞品仓库监控日报：`competitor-monitor.py`，`no_agent=true`，`deliver=feishu`，直接递送脚本 stdout。

## 修改前备份

改 cron 前先备份当前 profile 的 cron 配置：

```bash
backup_dir=/root/projects/hermes-backups/cron-product-monitor-$(date +%Y%m%d-%H%M%S)
mkdir -p "$backup_dir"
cp /root/.hermes/cron/jobs.json "$backup_dir/jobs.json"
```

## 手动脚本验证

```bash
python3 -m py_compile \
  /root/.hermes/scripts/product-repo-card.py \
  /root/.hermes/scripts/competitor-monitor.py \
  /root/.hermes/scripts/audit-products.py

python3 /root/.hermes/scripts/product-repo-card.py --help
PRODUCT_MONITOR_DRY_RUN=1 python3 /root/.hermes/scripts/product-repo-card.py --dry-run
python3 /root/.hermes/scripts/competitor-monitor.py
python3 /root/.hermes/scripts/audit-products.py
```

必须看到：

- 产品日报 dry-run 输出 `发送未发送（dry-run）`，不能显示“发送成功”。
- 竞品日报输出分类数、唯一仓库数、成功检查、错误数，并写入 `competitor-snapshot.json`。
- 产品审计输出产品总数、等级分布，并写入 `audit-report.json`。

## Cron 配置验收

检查三类 job 时不要只看名字，要核对：

- `enabled=true`
- `no_agent=true`
- `script` 指向真实 `~/.hermes/scripts/` 下可执行脚本
- `deliver` 符合策略：产品卡片 local、竞品 feishu、审计 local
- `last_delivery_error=None`
- `last_status=ok` 或新 job 经过手动 tick 后为 ok

用 `hermes cron tick --accept-hooks` 执行 due job 后，再检查 `~/.hermes/cron/jobs.json` 和 `~/.hermes/cron/output/<job_id>/`。

## 输出文件验收

```python
import json, pathlib, datetime
files = {
  'product_snapshot': '/root/.hermes/scripts/repo-snapshot.json',
  'competitor_snapshot': '/root/.hermes/skills/product-repo-monitor/references/competitor-snapshot.json',
  'audit_report': '/root/.hermes/skills/product-repo-monitor/references/audit-report.json',
}
for name, path in files.items():
    p = pathlib.Path(path)
    print(name, p.exists(), p.stat().st_size if p.exists() else 0)
    data = json.loads(p.read_text())
    if name == 'competitor_snapshot': print(data.get('schema_version'), len(data.get('repos', {})))
    if name == 'audit_report': print(data.get('total_products'), data.get('grade_distribution'))
    if name == 'product_snapshot': print(data.get('date'), len(data.get('products', [])))
```

## Pitfalls

- `cronjob(action="run")` 可能只是把 job 标成下一次 scheduler tick 执行；需要再执行 `hermes cron tick --accept-hooks` 或等待调度器 tick，然后复查 `last_run_at/last_status`。
- `last_status=ok` 不够，必须确认 cron output 文件非空且没有 `Traceback`、`401`、`403`、`429`、schema error。
- 产品日报不要为了测试直接实发；用 dry-run 验证脚本，用幂等 marker 防重复发送。
- 不要重启/停止 gateway，不要切 provider/model，除非用户明确授权。
