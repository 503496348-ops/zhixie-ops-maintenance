# Wave-2 pending_review 初筛（2026-07-23 continue）

## 前置闭环（本拍实测 10:01）
- 命令：`python3 scripts/ops-product-monitor-orchestrator.py --with-audit --with-fusion-plan --dry-run`
- 结果：`success_count=4 / total_steps=4`，`failure_count=0`，`dry_run=true`
- 产品日报实测：`25个产品, 24有仓, 总⭐82`；`products_with_issues={}`；既有缺仓 `aestheflow`
- 竞品快照：`schema_version=2`，`counts.categories=21`，`counts.repos=44`，失败=0
- 融合清单：`total_candidates=26`，`by_triage={可融合候选:15, 观察/人工复核:5, 仅记录:6}`

## 候选计数变化说明
- 历史拍：`25 (14/5/6)`（dify 降级为观察且出执行清单）
- 本拍：`26 (15/5/6)`
- **+1 主因**：`NVIDIA/SkillSpector` 进入执行清单（`pending_review / 可融合候选 / score=4` → `hermes-security-suite`）
- `langgenius/dify` 仍为 `watching / 观察 / score=1`，**不在**本拍执行清单
- 用户贴的旧截图 `25有仓/总⭐73` 为历史快照，**不以之为当前结论**

## Wave-2 初筛（pending_review ∩ 可融合候选）

| repo | score | unseen | 近提交语义 | go_for_wave | next_action |
|---|---:|---:|---|---|---|
| crewAIInc/crewAI | 6 | 1 | runtime hooks / agent load / dep | **hold-design** | Wave-1 已深核；等目标产品映射后做最小 PoC，不自动 implemented |
| excalidraw/excalidraw | 6 | 1 | editor hit-test / canvas 交互修复 | **no-code** | 保持 pending_review；无通用后端融合点 |
| huggingface/diffusers | 6 | 2 | modular pipelines + agentic CLI/skills | **watch-extract** | 仅抽取 agentic CLI 模式参考，不整仓融合 |
| **NVIDIA/SkillSpector** | **4** | **1** | **skill 安全扫描 runtime / provider / suppression / agent-cli** | **hold-design** | **映射 hermes-security-suite；建议下一拍做接口对照 PoC（规则层/CLI/baseline）** |
| huggingface/transformers | 4 | 3 | whisper/quantization/trainer 运行时 | **no-code** | 保持 pending_review；缺产品级直接入口 |
| scrapy/scrapy | 4 | 1 | spider middleware / optional deps | **no-code** | 保持 pending_review；无强绑定前不落地 |

### SkillSpector 初筛证据（本拍）
- 描述：Security scanner for AI agent skills（漏洞/恶意模式/安全风险）
- 星标实测：13555；语言 Python；HEAD `a54947c3`（Sync OSS release snapshot 2.4.3）
- 近期提交文件：`src/skillspector/providers/*`、`suppression.py`、`_agent_cli*.py`、tests — **后端/运行时信号强**
- 根目录：`src/`、`tests/`、`pyproject.toml`、`model_registry.yaml`、`Dockerfile` — 可工程化对接
- 产品映射：`hermes-security-suite`（与现有安全扫描/规则层同域）

## Wave-2 结论
1. **仍无“立即 merge 落地”项**（无无需设计即可并入的候选）。
2. **值得设计推进的 2 项**：
   - `crewAI` → barren-order（Wave-1 已定边界）
   - **`SkillSpector` → hermes-security-suite（本拍新晋 hold-design）**
3. `diffusers` 仅作 agentic CLI 模式参考摘录。
4. `excalidraw` / `transformers` / `scrapy`：no-code 观察。
5. `dify` 本拍保持观察，不回写成 implemented。

## 噪音闸门
- 本拍有实质变化：候选 25→26，可融合 14→15（SkillSpector 入榜）；产品星标稳定 82，Issue 仍 0。
- 编排器 4/4 绿灯；不跟旧截图 73⭐/25有仓 口径。
- 下一拍建议：对 `SkillSpector` 做与 `hermes-security-suite` 的最小接口对照 PoC（规则覆盖差集 + CLI 入口 + baseline 兼容性），再决定是否升 `poc_verified`。

## SkillSpector PoC 收口（2026-07-23）
- 对照报告：`references/skillspector-hss-interface-poc-2026-07-23.md`
- 结论：核心桥接已在 HSS main → 候选状态 **implemented**
- 残差：P1 baseline + skill-scan CLI；P2 LLM semantic / providers / MCP-server / batch
