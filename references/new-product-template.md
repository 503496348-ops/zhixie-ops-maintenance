# 新产品创建模板

## 必需文件清单

```
{repo}/
├── SKILL.md              # 技能定义（必须有 frontmatter + triggers + 工作流 + 技术参考 + Pitfalls）
├── README.md             # 用户文档（安装 + 使用 + FAQ + 架构）
├── .env.example          # 配置模板（如有配置）
├── .gitignore            # 排除 __pycache__、.env、数据目录
├── docker-compose.yml    # Docker 编排（如需部署）
├── install.sh            # 一键安装脚本（支持 --auto 无交互模式）
├── conf/                 # 配置文件
│   └── *.ini / Caddyfile
└── scripts/              # Python 脚本
    ├── main_script.py    # 核心逻辑
    ├── healthcheck.py    # 健康检查
    ├── backup.py         # 备份恢复
    └── setup_wizard.py   # 交互式配置向导
```

## SKILL.md 必需结构

```yaml
---
name: product-name
version: 1.0.0
description: "一句话描述"
author: AtomCollide-智械工坊团队
license: Apache-2.0
triggers:
  - 触发词1
  - 触发词2
  # 至少 8 个触发词
metadata:
  hermes:
    author: AtomCollide-智械工坊团队
    created: YYYY-MM-DD
    updated: YYYY-MM-DD
    maturity: production
    category: 分类名
    tags: [标签1, 标签2]
scripts:
  init: scripts/main_script.py
---

# 产品名

**一句话价值主张**

## When to Use
- 场景1
- 场景2

## Agent Workflow（智能体专用）
// 智能体如何使用此技能，无交互模式

## Quick Start
// 一键命令

## 工作流
// 详细步骤

## 技术参考
// 架构图、组件表、API 文档

## Pitfalls
// 踩坑记录
```

## 一键安装脚本设计规范

### 必须支持双模式

```bash
# 交互式（给人用）
curl -fsSL .../install.sh | bash

# 无交互（给智能体用）
curl -fsSL .../install.sh | bash -s -- --domain xxx --auto
```

### 结构化输出（必须）

无交互模式必须输出机器可解析的结果：
```bash
echo "---OUTPUT_START---"
echo "KEY1=value1"
echo "KEY2=value2"
echo "---OUTPUT_END---"
```

### 参数设计

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--domain` | 域名 | localhost |
| `--password` | 密码 | 自动生成 |
| `--auto` | 全自动模式 | 交互式 |

## 注册清单

新产品必须同步更新 4 个文件：

1. `references/product-list.md` — 添加产品行
2. `references/competitors.md` — 添加竞品分类
3. `product-repo-card.py` — COMPETITORS 字典（如有新分类）
4. GitHub 仓库 — 从零 clone 验证

## 质量门禁（v3 严格模式）

- frontmatter 以 `---` 开头，无行号前缀
- `triggers:` 字段存在
- `## 工作流` 章节标题存在
- `## 技术参考` 或 `## 技术架构` 章节标题存在
- 无 Getting Started / Installation 等 README 风格标题
- 代码文件 ≥ 3 个，总行数 ≥ 100
- 无 TODO/FIXME/placeholder/example.com/your-password
- 所有 .py 文件通过 `py_compile` 语法检查
