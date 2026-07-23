# SkillSpector ↔ hermes-security-suite 接口对照 PoC

- 生成时间：`2026-07-23T02:22:20.492035+00:00`
- SkillSpector：`a54947c307fe` (`/tmp/SkillSpector-head`)
- hermes-security-suite：`a09a428b6ae0` (`/tmp/zhixie-org-audit/hermes-security-suite`)

## 结论

- **候选状态建议：`implemented`**（不回退为 full pending_review）
- 既有融合：wave-6/9 已合入 `scripts/skillspector_bridge.py` + `modules/security_extensions/*`
- 验收：bridge_sample=`True` · pytest=`True` · doctor=`True` · gate=`True`
- Analyzer 覆盖：{'full': 10, 'partial': 13, 'bridge-only': 0, 'missing': 3}
- Feature 覆盖：{'full': 4, 'partial': 1, 'bridge-only': 0, 'missing': 4}

## 既有桥接面

| 入口 | 状态 |
|---|---|
| `scripts/skillspector_bridge.py` | ✅ sample/json/compact + OSV project |
| `tests/test_skillspector_bridge.py` | ✅ 2 passed |
| `scripts/doctor.py` skillspector check | ✅ |
| `scripts/hermes_security_suite_api.py` `/diag/skillspector` | ✅ |
| `package.json` `skillspector:bridge` | ✅ |
| `product_convergence.json` 映射 | ✅ |

## Analyzer 对照矩阵

| SkillSpector analyzer | HSS 覆盖 | 证据 |
|---|---|---|
| `static_patterns_prompt_injection` | 🟡 partial | redteam/prompt-security + genesisix rules; not first-class skill-scan family CLI |
| `static_patterns_anti_refusal` | 🟡 partial | redteam deepteam plugins; no dedicated static_patterns module |
| `static_patterns_data_exfiltration` | 🟡 partial | agent_action_security_policy / detector rules |
| `static_patterns_privilege_escalation` | 🟡 partial | mcp_runtime_security + policy |
| `static_patterns_supply_chain` | ✅ full | detector/modules/supply_chain.py + osv_client |
| `static_patterns_excessive_agency` | 🟡 partial | mcp least-privilege / runtime audit |
| `static_patterns_output_handling` | 🟡 partial | content_hardening |
| `static_patterns_system_prompt_leakage` | 🟡 partial | redteam prompt-security |
| `static_patterns_memory_poisoning` | ✅ full | modules/security_extensions/memory_poisoning_detector.py |
| `static_patterns_tool_misuse` | 🟡 partial | mcp_analyzer + runtime guard |
| `static_patterns_rogue_agent` | 🟡 partial | agent_handoff_security_invariants |
| `static_patterns_ssrf` | 🟡 partial | may exist in rules/yara; no dedicated module name |
| `static_patterns_harmful_content` | 🟡 partial | content_hardening |
| `static_patterns_agent_snooping` | ✅ full | detector/modules/agent_snooping.py |
| `behavioral_ast` | ✅ full | detector/modules/ast_analyzer.py |
| `behavioral_taint_tracking` | ✅ full | detector/modules/taint_tracker.py |
| `static_yara` | ✅ full | yara_scanner + 4 rule files |
| `mcp_least_privilege` | ✅ full | core/mcp_runtime_security.py + bridge |
| `mcp_tool_poisoning` | ✅ full | detector/modules/mcp_analyzer.py + bridge |
| `mcp_rug_pull` | ✅ full | detector/test_mcp_rug_pull.py / mcp modules |
| `osv_client` | ✅ full | detector/modules/osv_client.py + bridge --project |
| `semantic_developer_intent` | ❌ missing | no LLM multi-provider semantic stage like SS |
| `semantic_quality_policy` | ❌ missing | no equivalent LLM semantic node |
| `semantic_security_discovery` | ❌ missing | no equivalent LLM semantic node |
| `static_runner` | 🟡 partial | unified_scan + agent_scan_pipeline; different shape |
| `pattern_defaults` | 🟡 partial | rules/config distributed |

## 产品特性对照

| Feature | HSS 覆盖 | 证据 |
|---|---|---|
| skillspector scan CLI (`cli_scan`) | 🟡 partial | HSS has doctor/smoke/bridge/API diag, not full skill-dir scan CLI parity |
| baseline / FP suppression (`baseline_suppression`) | ❌ missing | SS suppression.py + baseline command |
| SARIF reporter (`sarif_output`) | ✅ full | modules/security_extensions/sarif_reporter.py |
| batch / multi-skill scan (`batch_multi_skill`) | ❌ missing | SS multi_skill.py |
| MCP server transport (`mcp_server_mode`) | ❌ missing | SS mcp_server.py FastMCP |
| multi LLM providers (`llm_providers`) | ❌ missing | SS providers: anthropic, anthropic_proxy, antigravity_cli, bedrock, claude_cli, codex_cli, gemini_cli, nv_build, openai |
| risk scoring engine (`risk_scoring`) | ✅ full | modules/security_extensions/risk_scoring_engine.py |
| trigger abuse detector (`trigger_abuse`) | ✅ full | modules/security_extensions/trigger_abuse_detector.py |
| fusion bridge (`skillspector_bridge`) | ✅ full | scripts/skillspector_bridge.py v1 + tests + doctor + API |

## 残差 backlog（增量，不重开整包融合）

| ID | 优先级 | 说明 |
|---|---|---|
| `baseline_suppression` | P1 | SS suppression.py + baseline command |
| `batch_multi_skill` | P2 | SS multi_skill.py |
| `llm_providers` | P2 | SS providers: anthropic, anthropic_proxy, antigravity_cli, bedrock, claude_cli, codex_cli, gemini_cli, nv_build, openai |
| `mcp_server_mode` | P2 | SS mcp_server.py FastMCP |
| `semantic_developer_intent` | P2 | no LLM multi-provider semantic stage like SS |
| `semantic_quality_policy` | P2 | no equivalent LLM semantic node |
| `semantic_security_discovery` | P2 | no equivalent LLM semantic node |

## 建议动作

1. 候选池 `NVIDIA/SkillSpector`：`pending_review` → **`implemented`**，保留 residual 备注
2. 不重做 bridge-1；若推进增量，单开：
   - P1：`baseline/suppression` 兼容层 + skill 目录扫描 CLI 对齐
   - P2：LLM semantic stage / multi-provider / MCP-server / multi-skill batch
3. 下次 SHA 漂移只做 residual diff，不再整项打回可融合候选

## 证据文件

- JSON：`/root/projects/zhixie-ops-maintenance/references/skillspector-hss-interface-poc-2026-07-23.json`
- 本报告：`/root/projects/zhixie-ops-maintenance/references/skillspector-hss-interface-poc-2026-07-23.md`
