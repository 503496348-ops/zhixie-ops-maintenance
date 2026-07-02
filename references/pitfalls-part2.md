## 44. read_file行号前缀导致审计脚本误判（2026-06-24）

**问题**：审计Neverend产品时，`read_file`返回内容带行号前缀（`1|---`、`74|## 工作流`），导致：
- frontmatter检查 `content.strip().startswith("---")` → 返回False（实际是`1|---`）
- workflow正则 `^## 工作流` 匹配失败（实际是`74|## 工作流`）
- 所有 `^` 锚定的章节标题正则全部失效
- 审计报告显示SKILL.md质量5.8/10（实际应为10/10）

**修复**：审计脚本读取文件后必须strip行号前缀：
```python
import re
content = read_file(path)['content']
lines = content.split("\n")
cleaned = [re.sub(r'^\d+\|', '', line) for line in lines]
content = "\n".join(cleaned)
```

或者直接用 `terminal('cat file')` 读取原始内容。

**铁律**：审计脚本不能直接用`read_file`的返回值做正则匹配。必须先strip行号，或改用`terminal('cat')`。

## 45. 新产品创建的标准流程（2026-06-24）

**问题**：创建Neverend产品时，漏了多个步骤（注册product-list.md、更新competitors.md、审计、品牌清理），需要反复提醒。

**标准流程**（按顺序）：
1. 创建GitHub仓库（`gh repo create`）
2. 编写核心代码（scripts/）
3. 编写SKILL.md（frontmatter+triggers+工作流+技术参考+Pitfalls）
4. 编写README.md（安装+使用+FAQ+架构）
5. 编写docker-compose.yml + 配置文件
6. 编写install.sh一键安装脚本
7. 注册到`references/product-list.md`（更新计数+添加行+更新日志）
8. 注册到`references/competitors.md`（添加竞品分类）
9. 品牌清理（扫描第三方引用、致谢改为技术栈）
10. 质量审计（5维度评分）
11. 补强到A级
12. 推送+从零clone验证

**铁律**：新产品创建不是"写完代码就结束"，必须完成全部12步才算交付。

## 46. 品牌清理扫描模式（2026-06-24）

**问题**：Neverend仓库中残留了"致谢"章节引用竞品仓库（vrtmrz/obsidian-livesync）、代码注释中的原作者库名（octagonal-wheels）。

**扫描模式**：
```bash
grep -rniE 'vrtmrz|vorotamoroz|octagonal-wheels|saltyoldgeek|融合自|Stars|⭐|致谢|原作|原作者' \
  --include='*.py' --include='*.md' --include='*.yml' --include='*.ini' .
```

**处理规则**：
- "致谢" → 改为"技术栈"，删除竞品仓库链接
- 代码注释中的库名 → 改为通用描述（"Compatible with X" → "Uses AES-256-GCM"）
- 技术兼容性字段（如数据库名`obsidian-livesync`）→ **保留**，改了会破坏兼容性

**铁律**：每个新产品的SKILL.md和README.md必须经过品牌清理扫描。"致谢"章节禁止出现竞品仓库链接。

## 47. 傻瓜式部署脚本模式（2026-06-24）

**问题**：用户明确说"我们的用户没有任何基础"，docker-compose + .env.example的手动配置流程不够傻瓜。

**标准模式**：每个Docker类产品必须有`install.sh`，实现：
1. 自动检查/安装Docker
2. 克隆仓库
3. 交互式配置（回车用默认值，自动生成密码）
4. 启动服务
5. 自动提取并打印关键信息（Setup URI / 密码 / 地址）

**install.sh关键技巧**：
- `curl -fsSL ... | bash` 一键运行
- 自动生成密码：`openssl rand -base64 16 | tr -d '/+=' | head -c 16`
- 自动生成口令：adjective-noun组合（如`patient-haze`）
- 等待服务就绪：轮询`docker logs`检查关键字
- 输出格式：带颜色的banner + 账号信息 + 下一步操作

**铁律**：Docker类产品的"完成定义"必须包含install.sh。没有一键脚本 = 用户无法使用。
