
# Pitfall #52: 逐个抓 README 而不是从 Bitable 拉（2026-06-25）

**场景**：用户要产品仓库链接和能力描述，Agent 逐个用 `web_extract` 抓 GitHub README。

**问题**：
- 慢（23个产品 = 23次 HTTP 请求）
- 不全（README 可能没有结构化的能力描述）
- 可能 404（部分仓库 README 路径不同）

**正确做法**：直接从 Bitable 拉，一次 API 调用拿到全部字段（产品名称、GitHub仓库、能力描述、最新动态、竞品对标等）。

```bash
lark-cli base +record-list --base-token [REDACTED_BASE_TOKEN] --table-id [REDACTED_TABLE_ID] --as bot --limit 50
```

**教训**：用户说"多维表格里面不就有么，你只要整理一下就好了"——数据源优先级：Bitable > product-list.md > GitHub。

---

# Pitfall #54: Python ≤3.11 f-string 不支持反斜杠（2026-06-25）

**场景**：竞品融合写模块时，f-string 表达式内使用带反斜杠的 dict 访问。

**问题**：Python 3.11 及以下，f-string 的 `{}` 表达式部分不能包含反斜杠字符。

```python
# ❌ SyntaxError: f-string expression part cannot include a backslash
text = f"[{t.get(\"rule_id\", \"\")}] {t.get(\"description\", \"\")}"

# ✅ 方案1：变量提取（推荐）
rid = t.get("rule_id", "")
desc = t.get("description", "")
text = f"[{rid}] {desc}"

# ✅ 方案2：字符串拼接
text = "[" + str(t.get("rule_id", "")) + "] " + str(t.get("description", ""))
```

**触发条件**：`py_compile` 报错 `SyntaxError: f-string expression part cannot include a backslash`，指向 f-string 中的 `\"` 转义。

**注意**：Python 3.12+ 解除了此限制（PEP 701），但服务器和 CI 环境可能仍是 3.11。为兼容性，统一用变量提取。

**铁律**：写完 .py 文件必须立即 `py_compile` 验证。f-string 中需要访问 dict 时，先提取到变量再插值。

---

# Pitfall #53: lark-cli base 命令参数踩坑（2026-06-25）

**连续 6 次命令错误**才找到正确语法：

| 错误写法 | 正确写法 |
|---------|---------|
| `lark-cli bitable` | `lark-cli base` |
| `records list` | `+record-list` |
| `--app-token` | `--base-token` |
| `--page-size` | `--limit` |

**完整正确命令**：
```bash
lark-cli --profile "$HERMES_LARK_CLI_PROFILE" base +record-list \
  --base-token [REDACTED_BASE_TOKEN] \
  --table-id [REDACTED_TABLE_ID] \
  --as bot \
  --limit 50
```

**注意**：`+record-list` 默认输出 markdown 表格。如需 JSON 解析，加 `--format json`。
