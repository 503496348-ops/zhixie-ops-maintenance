#!/usr/bin/env python3
"""
基于审计报告与竞品融合候选池，生成产品融合增强执行清单。

设计目标：把“可融合候选”从静态快照变成可执行、可验证的任务包。
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Any

SKILL_DIR = Path(__file__).resolve().parents[1]
REFERENCE_DIR = SKILL_DIR / "references"

AUDIT_REPORT_FILE = REFERENCE_DIR / "audit-report.json"
PLAN_JSON = REFERENCE_DIR / "fusion-enhancement-execution-plan.json"
PLAN_MD = REFERENCE_DIR / "fusion-enhancement-execution-plan.md"

# 竞品候选池默认优先读项目路径，兼容外部共享路径
DEFAULT_CANDIDATE_POOL = (
    REFERENCE_DIR / "competitor-candidate-pool.json"
)
SHARED_CANDIDATE_POOL = Path("/root/.hermes/shared/skills/product-repo-monitor/references/competitor-candidate-pool.json")

# 固定特征词，用于确定补齐方向
ALL_FEATURES = [
    "API集成",
    "数据处理",
    "机器学习",
    "Web框架",
    "数据库",
    "文件处理",
    "CLI工具",
    "测试",
]


@dataclass
class CandidateWorkItem:
    repo: str
    category: str
    products: list[str]
    triage: str
    score: int
    status: str
    audit_total: float
    audit_tech: int
    missing_features: list[str]
    recommended_actions: list[str]
    evidence: list[str]


def _load_json(path: Path, fallback: Path | None = None) -> dict[str, Any]:
    if not path.exists():
        if fallback is not None and fallback.exists():
            path = fallback
        else:
            return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _parse_args() -> set[str]:
    flags = set()
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            continue
        flags.add(arg[2:].lower())
    return flags


def _load_audit_data() -> dict[str, dict[str, Any]]:
    raw = _load_json(AUDIT_REPORT_FILE)
    results = raw.get("results", []) if isinstance(raw, dict) else []
    by_repo: dict[str, dict[str, Any]] = {}
    for item in results:
        if not isinstance(item, dict):
            continue
        repo = str(item.get("repo", "")).strip()
        if repo:
            by_repo[repo] = item
    return by_repo


def _load_candidates() -> dict[str, dict[str, Any]]:
    raw = _load_json(DEFAULT_CANDIDATE_POOL, SHARED_CANDIDATE_POOL)
    candidates = raw.get("candidates", {}) if isinstance(raw, dict) else {}
    if not isinstance(candidates, dict):
        return {}
    return candidates


def _missing_features(item: dict[str, Any]) -> list[str]:
    features = item.get("details", {}).get("features", [])
    current = set(features if isinstance(features, list) else [])
    return [f for f in ALL_FEATURES if f not in current]


def _recommendations(missing: list[str], triage: str) -> list[str]:
    recs: list[str] = []
    if "Web框架" in missing:
        recs.append("补齐可复用 API/服务能力边界，先补充 HTTP 输入输出契约与异常码策略")
    if "数据库" in missing:
        recs.append("补齐持久化落库与迁移脚本（至少持久化关键指标与证据凭证）")
    if "机器学习" in missing:
        recs.append("补齐模型推理链路/评分链路的最小闭环，并补充 smoke 测试")
    if "CLI工具" in missing:
        recs.append("补齐 CLI / 入口参数文档，增加 install/test/help 的一致性")
    if not recs:
        if triage == "可融合候选":
            recs.append("先完成 commit 语义回放，确认可复用模块后逐条提交")
        else:
            recs.append("先补齐审计缺口，再评估融合可执行性")

    # 防重
    seen: set[str] = set()
    uniq: list[str] = []
    for r in recs:
        if r in seen:
            continue
        seen.add(r)
        uniq.append(r)
    return uniq


def build_plan() -> tuple[dict[str, Any], list[CandidateWorkItem]]:
    audit = _load_audit_data()
    candidates = _load_candidates()

    works: list[CandidateWorkItem] = []
    for repo, c in candidates.items():
        if not isinstance(c, dict):
            continue
        triage = str(c.get("triage", "仅记录")).strip()
        score = int(c.get("score", 0) or 0)
        status = str(c.get("status", "recorded"))
        category = str(c.get("category", "").strip())
        products = c.get("products") if isinstance(c.get("products"), list) else []

        # 证据源
        evidence = [
            f"{repo} status={triage} score={score}",
            f"products={products}",
        ]

        # 找该仓库对应的审计口碑/短板（优先按产品映射）
        audit_item: dict[str, Any] = {}
        anchor_repo = ""
        if products:
            anchor_repo = str(products[0])
        elif "/" in str(repo):
            anchor_repo = str(repo).split("/")[1]
        else:
            anchor_repo = str(repo)

        if anchor_repo in audit:
            audit_item = audit[anchor_repo]
        elif products:
            for item in audit.values():
                if item.get("repo") == anchor_repo:
                    audit_item = item
                    break

        scores = (audit_item.get("scores") or {}) if isinstance(audit_item, dict) else {}
        total = float(scores.get("total", 0) if isinstance(scores, dict) else 0)
        tech = int(scores.get("tech", 0) if isinstance(scores, dict) else 0)
        missing = _missing_features(audit_item)

        # 只输出可执行方向：可融合候选 + 低分产品补齐类
        actionable = triage == "可融合候选" or total < 8.5 or (total >= 8.5 and tech <= 6)
        if not actionable:
            continue

        recs = _recommendations(missing, triage)

        if triage == "仅记录" and score == 0:
            # 避免把纯噪声记录拉进执行清单
            continue

        works.append(CandidateWorkItem(
            repo=repo,
            category=category,
            products=[str(x) for x in products],
            triage=triage,
            score=score,
            status=status,
            audit_total=round(total, 1),
            audit_tech=tech,
            missing_features=missing,
            recommended_actions=recs,
            evidence=evidence,
        ))

    # 排序：优先 triage，再分数，再技术分
    works.sort(key=lambda i: (
        0 if i.triage == "可融合候选" else 1,
        -i.score,
        -i.audit_total,
        -i.audit_tech,
    ))

    payload = {
        "schema_version": 2,
        "generated_at": datetime.now().isoformat(),
        "source": {
            "audit_report": str(AUDIT_REPORT_FILE),
            "candidate_pool": str(
                DEFAULT_CANDIDATE_POOL
                if DEFAULT_CANDIDATE_POOL.exists()
                else SHARED_CANDIDATE_POOL
            ),
        },
        "summary": {
            "total_candidates": len(works),
            "by_triage": {"可融合候选": 0, "观察/人工复核": 0, "仅记录": 0},
        },
        "items": [asdict(w) for w in works],
    }

    for w in works:
        payload["summary"]["by_triage"][w.triage] = payload["summary"]["by_triage"].get(w.triage, 0) + 1

    return payload, works


def write_plan(payload: dict[str, Any], items: list[CandidateWorkItem]) -> tuple[Path, Path]:
    PLAN_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    lines: list[str] = [
        "# 产品融合增强执行清单",
        f"生成时间：{payload.get('generated_at', '')}",
        "",
        "## 来源",
        f"- 产品审计：`references/audit-report.json`",
        "- 竞品候选池：`references/competitor-candidate-pool.json`（若本地无效则回退共享路径）",
        "",
        "## 执行约束",
        "- 不直接改供应商核心仓库口径，优先产出可验证增量",
        "- 每项融合需给出 `代码入口 / 验收命令 / 回退点`",
        "- 首轮只做能力增强准备，不做跨仓库自动重构",
        "",
    ]

    lines.append(f"## 候选池（共 {len(items)} 项）")
    lines.append("")
    for idx, item in enumerate(items, start=1):
        lines.append(f"### {idx}. {item.repo}")
        lines.append(f"- 分类：{item.category}")
        lines.append(f"- 映射产品：{', '.join(item.products) if item.products else '未命中'}")
        lines.append(f"- 融合判定：{item.triage}")
        lines.append(f"- 评分：{item.score}（状态：{item.status}）")
        lines.append(f"- 审计信号：total={item.audit_total}, tech={item.audit_tech}")
        lines.append(f"- 缺口特征：{', '.join(item.missing_features) if item.missing_features else '无明显缺口'}")
        if item.missing_features:
            lines.append("- 建议动作：")
            for act in item.recommended_actions:
                lines.append(f"  - {act}")
        lines.append("- 执行证据：")
        for line in item.evidence:
            lines.append(f"  - {line}")
        lines.append("")

    lines.extend([
        "## 交付验收",
        "1. 产出/更新本文件后，运行 `python3 scripts/audit-products.py`",
        "2. 产出后对比 `total_products` 与 25 产品一致，`products_with_issues` 无历史污染项",
        "3. 在 PR/候选动作中附上 `orchestrator` 汇总输出",
        "",
    ])

    PLAN_MD.write_text("\n".join(lines), encoding="utf-8")
    return PLAN_JSON, PLAN_MD


def main() -> int:
    flags = _parse_args()
    payload, items = build_plan()

    plan_json, plan_md = write_plan(payload, items)
    print(f"✅ 融合增强执行清单已生成: {plan_json}")
    print(f"✅ 人类可读版已生成: {plan_md}")

    if "validate" in flags:
        if payload["summary"]["total_candidates"] == 0:
            print("⚠️ 当前无可执行融合候选")
            return 1
        if not AUDIT_REPORT_FILE.exists():
            print("❌ 审计文件不存在")
            return 2
        print(f"📌 候选项统计: {payload['summary']}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
