# 仓内 Memory + OCR 对照与融合优先级（2026-07-23）

## 结论

| 外部仓 | 裁定 | score | 下一拍 |
|--------|------|-------|--------|
| **AIPMAndy/dna-memory** | **可融合候选** `pending_review` | 8 | P0：协议字段 + doctor 诊断/处方 + mindriver 完整性；不新建产品 |
| **NeuraSea/agentic-ocr** | **仅记录** `recorded` | 2 | 许可阻断代码融合；skill 方法论观察可选 |

---

## Memory 栈映射矩阵

| 仓内资产 | 类型 | 与 dna-memory | 动作 |
|----------|------|---------------|------|
| fact_store + fact_feedback | 运行时 | 功能重叠 recall/feedback；缺 Markdown SoT 跨端 | 保持真源；加 supersede/clients 对齐表 |
| memory-write-gate-system | skill | 写入门禁可互补 | 吸收 bounded extraction 与认知类型枚举 |
| memory-management / consolidation | skill | 五层 + 落卡 | 文档对齐 supersedes/status |
| hermes-doctor | 产品 | 诊断弱于跨端记忆链 | **P0 承载** integrity 模块 |
| pipixia-doctor | 产品 | 已有 RX-MEM-* | **P0 承载** 新处方 |
| mindriver | 产品 | context integrity 已有 duplicate/empty | **P1 扩展** |
| neverend | 产品 | vault_index Markdown | **P1 契约扫描** |

**优先级序**：shared 协议文档 → hermes-doctor 诊断 → pipixia-doctor 处方 → mindriver → neverend → 可选 MCP 适配（自研接口，不 vendor dna）。

---

## OCR 栈映射矩阵

| 仓内资产 | 类型 | 与 agentic-ocr | 动作 |
|----------|------|----------------|------|
| ocr-image | skill | 路由/预处理/质量思想可参考 | P2 clean-room 文档增强（零代码摘录） |
| yescan-ocr-universal | skill | 云 API vs 本地引擎 | 保持 |
| tencentcloud-ocr-questionmarkagent | skill | 试题场景 | 保持 |
| mineru-windows-deployment | skill | MinerU 部署 | 保持；不引入其 worker 源码 |
| product-list | — | 无 OCR 主产品 | **无代码回填目标** |

---

## 候选池登记

- `AIPMAndy/dna-memory` → pending_review / 可融合候选 / 智能体上下文 / 4 products
- `NeuraSea/agentic-ocr` → recorded / 仅记录 / 内容分析 / products=[]

报告：

- `/tmp/zhixie-org-audit/dna-memory-fusion-audit-2026-07-23.md`
- `/tmp/zhixie-org-audit/agentic-ocr-fusion-audit-2026-07-23.md`
- 本文件：`/tmp/zhixie-org-audit/memory-ocr-local-map-2026-07-23.md`
