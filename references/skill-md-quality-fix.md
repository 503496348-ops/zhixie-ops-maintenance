# SKILL.md 质量修复模式

## 什么时候用
审计脚本报 "⚠️ SKILL.md 看起来像 README，不是真正的 skill" 时。

## 诊断信号
审计 JSON 中：
```json
{
  "has_technical": false,
  "looks_like_readme": true,
  "skill_md": 8,  // 不低，但 tech=0 拖总分
}
```

## 根因
SKILL.md 写成了产品介绍（"这是一个XX系统，支持YY功能"），而不是技能定义（"当遇到XX场景时，执行YY步骤"）。

## 修复模板

```markdown
---
name: <产品名>
description: "<一句话描述，含触发词>"
version: x.y.z
triggers:
  - <触发词1>
  - <触发词2>
---

# <产品名>

## When to Use
- <场景1>
- <场景2>

## 快速开始
```bash
<最简可运行命令>
```

## 工作流
### Step 1: <步骤名>
<具体操作，不是泛泛而谈>

### Step 2: <步骤名>
<带参数的命令>

## 技术架构
### <模块/组件表>
| 模块 | 实现 | 职责 |

Pipeline: <步骤1> → <步骤2> → <步骤3>

## Pitfalls
1. <具体踩坑1>
2. <具体踩坑2>
```

## Quick Start → 快速开始（必须用中文标题）

`## Quick Start` 会被审计脚本正则 `(Getting Started|Installation|Quick Start|Overview)` 匹配，判定为 README 伪装。

```bash
# ❌ 触发 looks_like_readme
## Quick Start

# ✅ 通过
## 快速开始
```

同理：`## Getting Started` → `## 入门`，`## Overview` → `## 概述`，`## Installation` → `## 安装`。
