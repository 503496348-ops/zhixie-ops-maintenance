# 产品日报每日一次与防重复发送

## 背景

产品日报卡片由 `product-repo-card.py` 自行调用飞书发送；cron 只负责每天触发脚本并把 stdout 保存在本地。如果 cron stdout 又被递送到飞书，或 dry-run 输出写成“发送成功”，用户会看到类似“一天好几次”的日报噪声。

## 标准配置

产品日报 cron 只能保留一个任务：

```yaml
script: product-repo-card.py
no_agent: true
deliver: local
schedule: "0 9 * * *"
```

排查时检查：
- 名称/脚本包含 `智械工坊产品仓库日报`、`产品仓库日报`、`product-repo-card.py` 的 cron 是否只有一个。
- `deliver` 必须是 `local`，因为脚本已经自行发送飞书交互卡片。
- `no_agent` 必须是 `true`，避免 LLM 对 stdout 二次总结并再次推送。

## 脚本级幂等

`product-repo-card.py` 必须具备每日幂等保护：
- 成功发送后写入 `/root/.hermes/scripts/product-repo-card-sent.json`。
- 标记 key 使用 `日期 + chat_id hash`，不要把 chat_id 明文写入 marker。
- 同一天同目标再次运行时，默认输出 `[SKIP] 今天已发送过` 并不再发送。
- 只有显式设置 `PRODUCT_MONITOR_FORCE_SEND=1` 才允许强制重发。

## dry-run 输出要求

`--dry-run` / `PRODUCT_MONITOR_DRY_RUN=1` 绝不能输出“发送成功”。标准输出应明确为：

```text
[DRY_RUN] 跳过飞书发送，仅生成卡片和快照
产品仓库日报: ... 发送未发送（dry-run）
```

## 验证命令

```bash
python3 -m py_compile /root/.hermes/scripts/product-repo-card.py /root/.hermes/skills/product-repo-monitor/scripts/product-repo-card.py
python3 /root/.hermes/scripts/product-repo-card.py --dry-run | tail -n 8
python3 /root/.hermes/scripts/product-repo-card.py | tail -n 8
```

预期：
- dry-run 不发送飞书，摘要为 `发送未发送（dry-run）`。
- 当天已发送后，正常运行命中 `[SKIP]`，摘要为 `发送已跳过（今日已发送）`。
