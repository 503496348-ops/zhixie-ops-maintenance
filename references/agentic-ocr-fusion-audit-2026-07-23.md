# 深度审计：NeuraSea/agentic-ocr → 仓内 OCR 融合评估

**审计日**：2026-07-23  
**本地 clone**：`/tmp/audit-agentic-ocr`  
**HEAD**：`8d01a7710119cb581f3d800e771f619d3f05ad94`（`8d01a77` Initial commercial release，2026-07-21）  
**许可**：**NeuraSea Commercial Source License 1.0**（禁止生产使用、修改、衍生、再分发、SaaS 托管，除非另签商用协议）  
**Stars / 语言**：1⭐ / Python 3.12–3.13  
**形态**：Standalone MinerU + PP-OCR FastAPI worker（`agentic-ocr` 0.1.0）

---

## 1. 许可红线（一票否决代码融合）

LICENSE 明确：

- 仅允许 **查看 / 安全评估 / 内部评估商用许可**
- **禁止** production、copy、modify、derivative、distribute、hosted/SaaS
- 第三方组件（Paddle/MinerU 等）各自许可证仍适用，**不授予**对本仓库代码的衍生权

**裁定**：不得将本仓库任何源码合入产品仓或 shared skills 脚本；不得 PoC 拷贝实现。  
允许：架构阅读后的 **clean-room 方法论** 写入 skill 文档（自写描述，零代码摘录）。

---

## 2. 能力结构（只读摘要）

| 模块 | 路径 | 能力要点 |
|------|------|----------|
| Worker API | `ocr_worker_api.py` `/api/v1/ocr` | PDF/URL/Image 解析端点、队列、超时、健康检查 |
| Pipeline | `services/ocr_pipeline.py` | PDF/native/image/pages；structure + repair 阶段 |
| 路由 | `ocr_model_routing.py` | 语言/脚本 → Paddle v5/v6 route；dual-paddle |
| 融合 | `ocr_dual_paddle_line_fusion.py` | 空间匹配 + 置信度 + 片段抑制 |
| 质量 | `ocr_quality.py` | quality metrics / reading metadata |
| 预处理/策略 | preprocess/structure/language/repair policy | 可配置启发式 |
| 安全出站 | worker outbound request policy | URL/对象存储源限制 |
| 依赖 | pyproject optional `ocr` | paddleocr 3.7 / paddlepaddle 3.3 |

测试面宽（20+），但本拍 `uv run pytest` 策略子集因依赖/环境 **超时未出结果**；**不以测试绿作为融合许可依据**——许可已阻断代码路径。

---

## 3. 仓内 OCR 栈对照

| 能力 | 仓内 | agentic-ocr | 增量（方法论 only） |
|------|------|-------------|---------------------|
| 中文图文/证件/表格 | **yescan-ocr-universal**（夸克 API） | 本地 Paddle/MinerU | 本地离线路径我们已有 MinerU 笔记；不抄其 worker |
| 路由决策树 | **ocr-image** skill | 语言检测 + model policy | 可增强：双引擎投票/质量门的**文字描述** |
| PDF→MD | MinerU（Windows LL + Linux，ocr-image 文档化 6 坑） | MinerU provider 封装 | 部署经验我们更强；其 dual-paddle 融合思路可文档化 |
| 试题批改 OCR | tencentcloud-ocr-questionmarkagent | 通用 worker | 场景不同 |
| 产品仓 | **无独立 OCR 产品**（product-list 无 OCR 主产品） | 商业 worker | 无处「代码级融合回填」 |

---

## 4. 承载映射

| 外部模块 | 承载 | 裁定 |
|----------|------|------|
| 双引擎融合 / 质量门 / 语言路由 | skill **`ocr-image`**（文档方法论） | P2 观察：clean-room 写进决策树，**不贴代码** |
| MinerU worker 运维 | 已有 `mineru-windows-deployment` / ocr-image 坑位 | 不融源码 |
| 商用 API worker 整体 | — | **不融**；若业务需要生产级本地 OCR 中台 → 自研或签 NeuraSea 商用许可后再议 |

---

## 5. 状态裁定

| 字段 | 值 |
|------|-----|
| status | `recorded` |
| triage | `仅记录` |
| score | **2**（工程完整但许可阻断 + 1⭐ + 单 commit + 无产品承载） |
| category | `内容分析` |
| products | `[]`（无产品仓可回填代码；skill 层仅方法论） |
| decision | `commercial_license_block_code_fusion_2026-07-23` |

**快速淘汰维度**：License 不兼容代码融合（强于 stars 规则）。保留记录供监控许可变更 / 商用谈判，不进 fusion 执行 Wave。

---

## 6. 证据

```text
clone: /tmp/audit-agentic-ocr @ 8d01a77
LICENSE: NeuraSea Commercial Source License 1.0 (view-only without commercial agreement)
API: FastAPI /api/v1/ocr + dual-paddle experiment router
No product-list OCR primary product; local skills: ocr-image, yescan-ocr-universal, tencentcloud-ocr-questionmarkagent
```
