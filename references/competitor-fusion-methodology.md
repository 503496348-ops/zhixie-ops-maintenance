# 竞品融合增强方法论

## 适用场景
用户要求"研究竞品并融合增强"、"对标XX产品"、"看看竞品有什么值得学的"。

## 工作流

### Phase 1: 竞品研究（并行）
```python
# 用 web_extract 并行抓取竞品 README
urls = ["https://github.com/{org}/{repo}" for repo in target_repos]
results = web_extract(urls)
```
提取每个竞品的：
- 核心架构（设计模式、模块划分）
- 关键 API（用户直接调用的函数/命令）
- 差异化能力（我们没有的）

### Phase 2: 融合匹配
为每个竞品找到融合目标产品，确定可提取的能力：
| 竞品 | 我们的产品 | 可融合能力 | 预期代码量 |
|------|----------|-----------|-----------|

### Phase 3: 代码实现
- 每个融合独立一个目录 `/tmp/fusion-{product}/`
- 文件数 3-5 个，每个 150+ 行实际 Python
- 包含 docstring、类型提示、错误处理、回退机制
- 每个目录附 README.md 集成指南

### Phase 4: 推送
```bash
# 对每个产品仓库：
git clone https://github.com/503496348-ops/{repo}.git /tmp/{repo}-repo
mkdir -p /tmp/{repo}-repo/modules/{module_name}
cp /tmp/fusion-{product}/*.py /tmp/{repo}-repo/modules/{module_name}/
git add -A && git commit -m "feat: {竞品}融合 - {能力列表}" && git push
```

### Phase 5: 报告
输出表格：| # | 产品 | 竞品来源 | 新增模块 | 新增代码 | 增强能力 |

## Pitfalls

1. **不要只写代码不推送** — 本地文件不算完成，必须 git push 到仓库
2. **分支名检查** — `git push origin main` 失败时试 `master`，用 `git ls-remote --symref` 确认默认分支
3. **不要覆盖现有模块** — 新模块放在 `modules/` 子目录下，不碰已有代码
4. **并发限制（硬性）** — `delegate_task` 的 `max_concurrent_children=1`，**禁止并行 spawn 多个子任务**。多产品融合必须：(a) 用 `execute_code` 自己写全部模块（推荐），或 (b) 串行 delegate 每个产品。今天实测：7个模块全部用 execute_code 单线程写完，比 delegate 快且可控。
5. **竞品引用清理** — 代码和文档中不得出现竞品仓库名/Stars/作者名，只在 SKILL.md 技术参考中简要说明来源
6. **代码质量** — 每个 .py 文件必须可独立 `py_compile`，不依赖项目特定的导入路径。**写完立即验证**，不要等 push 后才发现语法错误。Python ≤3.11 的 f-string 不支持反斜杠（`f\"{d[\\\"k\\\"]}\"`` 报错），改用字符串拼接或变量提取。
7. **f-string 复杂表达式** — Python ≤3.11 的 f-string 内不能有多行 `if/else` 表达式（如 `f\"{x if y else z:.4f}\"` 会报 `unterminated string`）。**解决方案**：提取为独立方法 `def _format_x(self): return \"%.4f\" % self.x`，在 f-string 中只调用方法。

## Deep Research 模式（竞品代码级分析）

当竞品有复杂架构（不是简单 README 就能理解的）时，用 `delegate_task` 做深度研究：

```python
delegate_task(
    goal="Deep-read {竞品} GitHub repo: extract architecture, core capabilities, API design...",
    context="Repo: https://github.com/{org}/{repo} ({stars}K stars). Extract from README, docs, recent releases...",
    toolsets=["web", "search"],
)
```

**适用场景**：竞品是框架/引擎级产品（如 ComfyUI、diffusers），需要理解内部架构才能找到可融合点。
**不适用**：竞品是简单工具/脚本，README 就够了。

### 多优先级分批执行

当融合涉及多个产品时，按优先级分批：

| 优先级 | 判定标准 | 执行策略 |
|--------|---------|---------|
| P0 | 竞品信号最强（Stars+100以上）或架构级创新 | 最先执行，代码量最大 |
| P1 | 中等信号或辅助增强 | P0完成后执行 |
| P2 | 评估性质，可行性待验证 | 最后执行，代码量最小 |

**铁律**：用户说"依次执行P0-P2"= 按顺序一个一个做，不是并行。

## 实战案例（2026-06-25 第二次 — 媒体生成融合）

4个融合对（P0-P2），11个新模块，~3952行代码：

| 优先级 | 竞品 | 产品 | 模块 | 行数 |
|--------|------|------|------|------|
| P0 | ComfyUI (118K⭐) | 破窗造视 | dag_executor + vram_manager + node_registry + conditioning_composer | 1161 |
| P0 | diffusers (34K⭐) | 灵感象限 | modular_pipeline + taylor_cache + layerwise_casting + regional_compiler | 917 |
| P1 | KrillinAI (10K⭐) | 灵感象限 | pipeline_orchestrator + multi_asr_backend | 527 |
| P2 | excalidraw (126K⭐) | 有点东西 | excalidraw_adapter | 371 |

**关键发现**：
- ComfyUI 最值得融合的是执行引擎架构（DAG + VRAM管理），不是模型列表
- diffusers v0.37 Modular Diffusers 是架构级创新，与我们模块化编排思路高度契合
- KrillinAI 的 CLI+skills+pipeline 模式让视频处理变成 Agent 可编排的模块化命令
- excalidraw .excalidraw JSON 格式是开放标准，tldraw 生产需付费许可→选择 excalidraw

## 实战案例（2026-06-25 第一次）

2个融合对，7个新模块，~2257行代码：

| 竞品 | 产品 | 模块 | 行数 |
|------|------|------|------|
| SkillSpector (10K⭐) | 奇点造物 | memory_poisoning_detector + trigger_abuse_detector + risk_scoring_engine + sarif_reporter | 972 |
| QuantDinger (8.7K⭐) | 深度方略 | agent_gateway + strategy_runtime + opportunity_radar | 1285 |

## 实战案例（2026-06-24）

5个融合对，17个新模块，~5029行代码：

| 竞品 | 产品 | 模块 | 行数 |
|------|------|------|------|
| CrewAI (25K⭐) | 荒原序列 | role_orchestrator + flow_engine | 690 |
| GPT-Researcher (27K⭐) | 裂变创作 | research_planner + parallel_researcher + deep_explorer + report_publisher | 1149 |
| ControlNet (30K⭐) | 艺游未境 | control_processors + control_fusion + conditioning_pipeline | 968 |
| spaCy (30K⭐) | 艺术生花 | ner_analyzer + text_classifier + keyword_extractor + readability_scorer | 919 |
| Outlines (10K⭐) | 妙笔生花 | structured_generator + schema_prompts + output_validator + format_templates | 1303 |
