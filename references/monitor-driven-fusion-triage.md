# 竞品日报驱动融合审计：代码变化优先级判定

## 背景

竞品监控日报里的 `最近3天有更新` 和 `Stars增长` 只是告警信号，不等于融合价值。高 star 或高 delta 项目可能只是文档、版本号、CI 或导航更新；低 star 项目也可能新增了关键代码能力。

## 快速判定流程

1. 从日报筛出告警仓库：
   - `🆕 最近3天有更新`：必须查最近 commit。
   - `📈 +N⭐`：除非同时有代码更新，否则先记录。
   - `🆕 + 📈`：最高优先级，但仍需文件级验证。
2. 用 GitHub API 拉每个仓库最近 3 个 commit，并进一步拉 commit detail 的 `files`。
3. 统计：
   - `files_total`
   - `code_files`：py/ts/tsx/js/go/rs/java/cpp/vue 等
   - `doc_files`：md/mdx/rst/txt
   - `additions/deletions`
   - 变更文件 sample
4. 分类输出：
   - **可融合**：新增/修改核心代码模块、API schema、运行时编排、安全分析器、验证 harness、模型/工具适配器。
   - **仅记录**：纯文档、版本 bump、CI、依赖轻微更新、测试覆盖补充但无新产品能力。
   - **噪声更新**：README/AGENTS/导航/Star 引导等。

## code_change_score 建议

给日报脚本增加一个派生分数，避免把纯文档更新推成“融合机会”。

| 信号 | 加分 |
|---|---:|
| 最近 3 个 commit 中 `code_files >= 5` | +3 |
| `additions >= 300` 且含代码文件 | +2 |
| 文件路径含 `src/`、`packages/`、`api/`、`core/`、`tests/` | +1 |
| commit message 含 `feat`、`security`、`contract`、`runtime`、`toolkit`、`e2e` | +1 |
| 纯 docs/mdx/README/AGENTS | -3 |
| 仅 version bump/changelog/CI | -2 |

建议阈值：
- `score >= 4`：进入“可融合候选”。
- `score 1-3`：列入“观察/人工复核”。
- `score <= 0`：日报只记录，不触发融合。

## 映射输出格式

审计日报不要只说“仓库更新了”，必须映射到我们的产品：

| 竞品 | 证据 | 代码变化 | 对应产品 | 融合建议 | 优先级 |
|---|---|---:|---|---|---|
| owner/repo | commit sha + 文件路径 | N files / M code files / +X | 产品名/仓库 | 具体模块/能力 | P0/P1/P2 |

## 2026-07-02 实战样例

- `NVIDIA/SkillSpector`：新增/更新 MCP least privilege、tool poisoning、OSV live vulnerability lookup；应映射到 `hermes-security-suite` / `AtomGuard`，P0。
- `langgenius/dify`：最近 commit 大量 console contract / API schema / Zod 类型契约迁移；应映射到白龙马/皮皮虾/智脑星河/荒原序列的工具契约校验，P0。
- `botpress/botpress`：`llmz` runtime orchestration 拆分、静态输入 schema、tuple/object 参数处理；应映射到 EasyRhythm/Blastogene 的客服流转与社群工作流 schema，P1。
- `vrtmrz/obsidian-livesync`：真实 Obsidian E2E runner ADR 和测试 harness；应映射到 Neverend 的真实同步验收，P1。
- `mem0ai/mem0`：本轮主要是 docs/mdx 导航和 star nudges；记录即可，不触发融合。
- `Comfy-Org/ComfyUI`：本轮高星增长但最新代码变化很小，主要 AGENTS 文档；记录即可，不插队。
