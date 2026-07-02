# 竞品融合增强工作流

## 什么时候用
- 用户说"研究竞品""融合增强""对标XX做升级"
- 竞品监控日报显示某竞品有重大更新（Stars +50+，3天内有推送）
- 季度产品回顾

## 工作流

### Phase 1: 竞品研究（并行）
1. 从 `references/competitors.md` 读取竞品列表
2. `web_extract` 批量抓取竞品 GitHub README（每批 5 个）
3. 提取：核心能力、架构设计、API 模式、技术栈

### Phase 2: 融合匹配
按以下维度评估融合价值：
| 维度 | 权重 | 说明 |
|------|------|------|
| Stars + 增长 | 30% | 社区热度 = 能力成熟度 |
| 能力互补性 | 40% | 竞品有我们没有的能力 |
| 代码可移植性 | 30% | 能否提取独立模块 |

输出：融合对列表（竞品 → 我们的产品 → 具体能力 → 预估代码量）

### Phase 3: 代码生成
每个融合对创建独立目录 `/tmp/fusion-<product>/`：
- 每个模块 150+ 行，有 docstring、类型提示、错误处理
- 包含 README.md（集成指南 + 用法示例）
- 代码风格：适配我们架构，不是直接复制竞品

### Phase 4: 推送到产品仓库
```bash
# 每个产品仓库单独 clone → 复制文件 → commit → push
git clone <repo-url> /tmp/<repo>-repo
mkdir -p /tmp/<repo>-repo/modules/<module>/
cp /tmp/fusion-<repo>/*.py /tmp/<repo>-repo/modules/<module>/
git add -A && git commit -m "feat: <竞品>融合 - <能力列表>" && git push
```

### Phase 5: 交叉验证
- 从零 clone 验证文件存在
- **`py_compile` 逐文件验证**（不能只看语法高亮）
- 检查 commit 历史（不含"清除/清理原作者"等字样）
- 更新 competitors.md 和 product-list.md

## 输出格式
```
| # | 竞品来源 | 我们的产品 | 新增模块 | 新增代码 | 增强能力 |
```

## 注意事项
1. **代码必须是真正可运行的**，不是 stub/wrapper
2. **竞品引用清理**：不得在 SKILL.md/README 出现"融合自 XX"
3. **并发限制**：delegate_task 最多 1 个并发，优先用 execute_code 自己写
4. **push 分支名**：先检查远程默认分支（main vs master），用对应的 push
5. **Python f-string 禁止反斜杠**：`f"{dict[\"key\"]}"` 在 ≤3.11 报 SyntaxError。改用 `"[" + str(t.get("key", "")) + "]"` 或先提取变量
6. **push 前 `git diff --cached --stat`**：确认行数合理，空 diff = 文件复制失败
