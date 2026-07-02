# 新产品创建 Checklist

## 触发条件
用户说"新增产品""做成第N款产品""新建仓库做产品"时，按此流程执行。

## 前置信息（必须确认）
- [ ] 产品中文名 + 英文代号
- [ ] GitHub 仓库名（小写-kebab-case）
- [ ] 产品分类（新建 or 现有）
- [ ] 一句话描述

## Step 1: 创建 GitHub 仓库
```bash
gh repo create 503496348-ops/<repo-name> --public --description '<中文描述>'
```
注意：`gh repo create` 不会自动设置 remote，push 前需要手动 `git remote add origin`。

## Step 2: 初始化仓库内容
最低标准文件：
- `SKILL.md` — 必须有 YAML frontmatter + triggers + 工作流 + 技术参考
- `README.md` — 用户文档，含 Quick Start
- `.gitignore`

## Step 3: 注册到 product-list.md
1. 添加产品行（#、产品名、英文代号、仓库名、分类、默认分支、状态）
2. 更新头部产品总数
3. 添加更新记录条目

## Step 4: 竞品分类同步
如果是新分类：
1. 在 `references/competitors.md` 添加分类行
2. 更新 `competitor-monitor.py` 的分类覆盖（如需要）

## Step 5: 推送 + 从零 clone 验证
```bash
git remote add origin https://github.com/503496348-ops/<repo>.git
git push -u origin main
# 验证
cd /tmp && rm -rf verify && git clone --depth 1 <url> verify
ls verify/SKILL.md  # 确认文件存在
head -5 verify/SKILL.md  # 确认 frontmatter 正确
```

## Step 6: 交叉验证
- product-list.md 产品数 = Bitable 记录数
- competitors.md 分类覆盖率不下降
- SKILL.md 通过审计（frontmatter + triggers + 工作流 + 技术参考）

## 常见坑
1. **gh repo create 后忘了 remote** — push 报 "origin does not appear to be a git repository"
2. **默认分支名不一致** — 本地 git init 默认 master，GitHub 默认 main。用 `git branch -m main` 统一
3. **SKILL.md 像 README** — 必须有 `## 工作流` 章节（不是"使用方法"），必须有 `## 技术参考` 或 `## Pitfalls`
4. **竞品引用残留** — SKILL.md/README 不得出现"融合自""Stars引用""竞品对标表"
