# Bitable 数据解析踩坑（2026-06-25）

## 问题1：`--format json` 字段顺序与 `+field-list` 不一致

`lark-cli base +record-list --format json` 返回 `data.data` 二维数组，值的顺序由 `data.field_id_list` 决定，**不是** `+field-list` 返回的字段名列表顺序。

```python
# ❌ 错误：假设 values[i] 对应 field_names[i]
fields = ["产品名称", "产品分类", ...]  # 来自 +field-list
values = records[0]  # 来自 --format json
rec = dict(zip(fields, values))  # 字段错位！

# ✅ 正确：用 field_id_list 做中间映射
field_ids = data["data"]["field_id_list"]   # 值的实际顺序
fields_meta = data["data"]["fields"]         # 与 field_id_list 等长，按 field_id_list 排序
id_to_name = dict(zip(field_ids, fields_meta))
rec = {id_to_name[fid]: vals[j] for j, fid in enumerate(field_ids)}
```

**根因**：`field_id_list` 按 Bitable 内部 ID 排序，`+field-list` 按创建时间或字母排序，两者顺序不同。

## 问题2：默认 markdown 格式管道符断裂

`+record-list`（不加 `--format json`）输出 markdown 表格。当字段值包含 `|`（markdown 链接 `[text](url)`、HTML `<br>`），表格列解析错位。

**症状**：某些记录有 17 列（正常 13 列），GitHub 仓库列显示竞品信息，文档版本列显示维护者名称。

**判断方法**：`len(line.split("|")) - 2` 不等于字段数 → 该行有管道符断裂。

**修复**：程序化解析 Bitable 数据时**必须用 `--format json`**，不用 markdown 表格。

## 正确的全量读取流程

```python
import json

# 1. 获取字段元数据（用于构建 id→name 映射）
field_data = json.loads(terminal("lark-cli base +field-list --base-token X --table-id Y --as bot --format json")["output"])
fields = field_data["data"]["fields"]

# 2. 获取记录（JSON格式）
rec_data = json.loads(terminal("lark-cli base +record-list --base-token X --table-id Y --as bot --limit 50 --format json")["output"])
field_ids = rec_data["data"]["field_id_list"]
id_to_name = dict(zip(field_ids, fields))
records = rec_data["data"]["data"]

# 3. 正确映射
for vals in records:
    rec = {}
    for j, fid in enumerate(field_ids):
        v = vals[j] if j < len(vals) else None
        if isinstance(v, list) and v and isinstance(v[0], dict):
            # 富文本：提取 text
            v = "".join(item.get("text", "") for item in v if isinstance(item, dict))
        rec[id_to_name[fid]] = v
```

## 交叉验证 checklist

审计 Bitable 数据时：
1. 记录数 = `len(records)` vs `len(record_ids)`
2. 每条记录的字段数 = `len(field_ids)`
3. 分类与 product-list.md 一致（用 repo name 做 join key，不用产品名称）
4. 版本号以 `v` 开头
5. GitHub 仓库字段以 `http` 开头
6. 竞品对标字段非空
