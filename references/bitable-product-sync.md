# Bitable 产品同步工作流

> 产品管理三端一致性检查：GitHub 仓库 ↔ product-list.md ↔ Bitable 项目总览表

## 数据源优先级

1. **Bitable** — 权威数据源（人工维护，最准确）
2. **product-list.md** — 日报数据源（自动从 Bitable 同步）
3. **GitHub 仓库** — 实际代码（可能存在未注册的产品）

## 同步检查流程

### Step 1: 拉取 Bitable 产品列表

```bash
lark-cli base +record-list --base-token "[REDACTED_BASE_TOKEN]" --table-id "[REDACTED_TABLE_ID]" --as bot --limit 100
```

统计产品数量和名称。

### Step 2: 对比 product-list.md

```bash
grep "^| [0-9]" /root/.hermes/skills/product-repo-monitor/references/product-list.md | wc -l
```

### Step 3: 对比 GitHub 仓库

```bash
gh repo list 503496348-ops --limit 50 --json name --jq '.[].name'
```

### Step 4: 识别差异

| 差异类型 | 处理方式 |
|---------|---------|
| Bitable 有，product-list.md 无 | 更新 product-list.md |
| product-list.md 有，Bitable 无 | 在 Bitable 新增记录 |
| GitHub 有，两边都无 | 评估是否为产品，决定是否注册 |
| Bitable 有，GitHub 无 | 检查是否已归档或未建仓 |

## 新增 Bitable 记录

### 1. 添加产品分类选项（如需要）

```bash
# 先检查现有选项
lark-cli base +field-list --base-token "[REDACTED_BASE_TOKEN]" --table-id "[REDACTED_TABLE_ID]" --as bot

# 如需新选项，更新字段（PUT 语义，必须包含所有现有选项）
lark-cli base +field-update --base-token "[REDACTED_BASE_TOKEN]" --table-id "[REDACTED_TABLE_ID]" --field-id "[REDACTED_FIELD_ID]" --as bot --yes --json '{"name":"产品分类","type":"select","multiple":false,"options":[...全部现有选项...,{"hue":"Green","lightness":"Lighter","name":"新分类"}]}'
```

### 2. 创建记录

```bash
lark-cli base +record-batch-create --base-token "[REDACTED_BASE_TOKEN]" --table-id "[REDACTED_TABLE_ID]" --as bot --json '{
  "fields": ["产品名称", "英文代号", "产品分类", "GitHub仓库", "整体进度", "维护者", "最新动态", "文档版本", "竞品对标Top3", "备注"],
  "rows": [["产品名-ProductName", "ProductName", "分类", "https://github.com/503496348-ops/repo", "已上线", "AtomCollide-智械工坊", "最新动态描述", "v1.0.0", "①竞品A\n②竞品B\n③竞品C", "备注"]]
}'
```

### 3. 更新 product-list.md

```bash
# 在产品表格中添加新行
# 更新记录数
# 添加更新记录
```

## 关键字段

| 字段名 | 类型 | 说明 |
|--------|------|------|
| 产品名称 | text | 格式：中文名-英文代号 |
| 英文代号 | text | 产品英文名 |
| 产品分类 | select | 必须是已有选项 |
| GitHub仓库 | text | 完整 URL |
| 整体进度 | select | 已上线/测试中/开发中 |
| 维护者 | text | 团队名 |
| 最新动态 | text | 最近更新摘要 |
| 文档版本 | text | 版本号 |
| 竞品对标Top3 | text | ①②③ 格式 |
| 备注 | text | 其他信息 |

## Bitable 信息

- base-token: `[REDACTED_BASE_TOKEN]`
- 项目总览表: `[REDACTED_TABLE_ID]`
- 产品分类字段 ID: `[REDACTED_FIELD_ID]`
- 整体进度字段 ID: `fld6hSiW6v`
