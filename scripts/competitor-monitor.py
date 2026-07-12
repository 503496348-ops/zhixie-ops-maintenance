#!/usr/bin/env python3
"""
竞品持续监控脚本 v3（融合增强版）

事实源：../references/competitors.md（或 ZHIXIE_OPS_SKILL_DIR 指定目录）
快照：../references/competitor-snapshot.json

设计原则：
- GitHub 认证只读 GITHUB_TOKEN 或 gh auth token，禁止硬编码凭据。
- 每次保存 schema_version=2 的单一结构，旧 nested/flat 混合快照只用于兼容读取，不再续写。
- 输出只包含脚本实查原始数值和 delta，不让 LLM 二次改写数字。
- 告警仓库走 commit 级融合分诊，映射到具体产品。
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import time
from difflib import SequenceMatcher
from datetime import datetime, timezone
from functools import lru_cache
from pathlib import Path
from typing import Any

DEFAULT_SKILL_DIR = Path("/root/.hermes/shared/skills/product-repo-monitor")
SKILL_DIR = Path(os.environ.get("ZHIXIE_OPS_SKILL_DIR", DEFAULT_SKILL_DIR if DEFAULT_SKILL_DIR.exists() else Path(__file__).resolve().parents[1]))
COMPETITORS_MD = SKILL_DIR / "references" / "competitors.md"
PRODUCT_LIST_MD = SKILL_DIR / "references" / "product-list.md"
SNAPSHOT_FILE = SKILL_DIR / "references" / "competitor-snapshot.json"
CANDIDATE_POOL_FILE = SKILL_DIR / "references" / "competitor-candidate-pool.json"
HISTORY_FILE = SKILL_DIR / "references" / "competitor-history.json"
SCHEMA_VERSION = 2
GITHUB_API = "https://api.github.com"

ALERT_STARS = 50
ALERT_PUSH_DAYS = 3
DELAY_SECONDS = 0.2

CODE_EXTENSIONS = {
    ".py", ".ts", ".tsx", ".js", ".jsx", ".go", ".rs", ".java", ".cpp", ".hpp",
    ".c", ".h", ".cs", ".kt", ".swift", ".php", ".rb", ".vue", ".svelte", ".html",
    ".css", ".scss", ".less",
}
DOC_EXTENSIONS = {".md", ".mdx", ".rst", ".txt"}
CORE_PATH_KEYWORDS = (
    "src/",
    "packages/",
    "package/",
    "api/",
    "core/",
    "runtime/",
    "tests/",
    "test/",
    "schemas/",
    "model/",
    "tools/",
)
COMMIT_SCORE_KEYWORDS = ("feat", "security", "contract", "runtime", "toolkit", "tools", "e2e", "pipeline", "schema")

CATEGORY_ALIAS = {
    "飞书白板": ["飞书白板设计+PPT", "飞书白板设计", "飞书白板"],
    "多agent协作": ["多agent", "多Agent"],
}


def parse_table_rows(md_path: Path) -> list[list[str]]:
    if not md_path.exists():
        return []
    rows: list[list[str]] = []
    for line in md_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line.startswith("|") or line.startswith("|--") or line.startswith("| ------"):
            continue
        if "| # |" in line or "仓库 | 说明" in line:
            continue
        cols = [c.strip() for c in line.split("|") if c.strip()]
        if len(cols) >= 2:
            rows.append(cols)
    return rows


def parse_competitors_md() -> dict[str, list[str]]:
    competitors: dict[str, list[str]] = {}
    for cols in parse_table_rows(COMPETITORS_MD):
        if len(cols) < 2:
            continue
        category = cols[0]
        repos: list[str] = []
        for cell in cols[1:]:
            if cell == "—":
                continue
            m = re.match(r"([\w\-.]+/[\w\-.]+)", cell)
            if m:
                repos.append(m.group(1))
        if repos:
            competitors[category] = repos
    if not competitors:
        raise RuntimeError(f"竞品清单无有效条目: {COMPETITORS_MD}")
    return competitors


def parse_product_categories() -> dict[str, list[str]]:
    # product-list columns: #, 产品名, 英文代号, GitHub仓库, 分类, 默认分支, 状态
    category_products: dict[str, list[str]] = {}
    for cols in parse_table_rows(PRODUCT_LIST_MD):
        if len(cols) < 7:
            continue
        repo = cols[3]
        category = cols[4]
        status = cols[6]
        if "归档" in status:
            continue
        if repo and category:
            category_products.setdefault(category, []).append(repo)
    return category_products


def normalize_category_key(text: str) -> str:
    txt = text.lower().strip()
    txt = txt.replace("+", "")
    txt = re.sub(r"\s+", "", txt)
    return txt


def map_category_to_products(category: str, product_map: dict[str, list[str]]) -> list[str]:
    if category in product_map:
        return product_map[category]

    for k, v in CATEGORY_ALIAS.items():
        if k == category:
            continue
    for aliases in CATEGORY_ALIAS.values():
        if category in aliases:
            for a in aliases:
                if a in product_map:
                    return product_map[a]

    key_norm = normalize_category_key(category)
    # 直接子串命中
    for pcat, repos in product_map.items():
        pnorm = normalize_category_key(pcat)
        if key_norm in pnorm or pnorm in key_norm:
            return repos

    # 模糊匹配 fallback
    best: list[str] = []
    best_ratio = 0.0
    for pcat, repos in product_map.items():
        ratio = SequenceMatcher(None, key_norm, normalize_category_key(pcat)).ratio()
        if ratio > best_ratio and ratio >= 0.68:
            best_ratio = ratio
            best = repos
    return best


@lru_cache(maxsize=1)
def get_github_token() -> str:
    token = os.environ.get("GITHUB_TOKEN", "").strip()
    if token:
        return token
    try:
        r = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True, timeout=6)
        if r.returncode == 0 and r.stdout.strip():
            return r.stdout.strip()
    except Exception:
        pass
    return ""


def github_api(path_or_url: str) -> Any:
    url = path_or_url if path_or_url.startswith("http") else f"{GITHUB_API}{path_or_url}"
    headers = ["-H", "Accept: application/vnd.github+json"]
    token = get_github_token()
    if token:
        headers.extend(["-H", f"Authorization: token {token}"])
    result = subprocess.run(["curl", "-sS"] + headers + [url], capture_output=True, text=True, timeout=45)
    if result.returncode != 0:
        return {"_error": f"curl exit {result.returncode}"}
    try:
        data = json.loads(result.stdout)
    except Exception as e:
        return {"_error": f"json decode error: {e}"}
    if isinstance(data, dict) and data.get("message"):
        msg = str(data.get("message", ""))
        if "rate limit" in msg.lower() or "API rate limit" in msg.lower():
            return {"_rate_limited": True, "message": msg}
        if msg in {"Not Found", "Bad credentials"}:
            return {"_error": msg}
    return data


def fetch_release_summary(repo: str) -> dict[str, str]:
    release = github_api(f"/repos/{repo}/releases/latest")
    if not isinstance(release, dict) or release.get("message") or release.get("_error"):
        return {"tag": "", "published_at": ""}
    return {"tag": str(release.get("tag_name") or ""), "published_at": str(release.get("published_at") or "")}


def fetch_security_policy(repo: str) -> bool:
    """Check whether the repository publishes a SECURITY.md policy."""
    policy = github_api(f"/repos/{repo}/contents/SECURITY.md")
    return isinstance(policy, dict) and bool(policy.get("name"))


def _parse_time(value: str) -> datetime | None:
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (TypeError, ValueError):
        return None


def trend_windows(repo: str, current_stars: int, history: list[dict[str, Any]], now_iso: str) -> dict[str, int]:
    now = _parse_time(now_iso)
    if now is None:
        return {"stars_7d": 0, "stars_30d": 0}
    result: dict[str, int] = {}
    for days, key in ((7, "stars_7d"), (30, "stars_30d")):
        cutoff = now.timestamp() - days * 86400
        eligible = [entry for entry in history if (_parse_time(str(entry.get("generated_at") or "")) or now).timestamp() <= cutoff and repo in (entry.get("repos") or {})]
        if not eligible:
            result[key] = 0
            continue
        baseline = int((eligible[-1].get("repos") or {}).get(repo, {}).get("stars", current_stars) or current_stars)
        result[key] = current_stars - baseline
    return result


def load_history() -> list[dict[str, Any]]:
    try:
        data = json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except (OSError, json.JSONDecodeError):
        return []


def append_history(repos: dict[str, dict[str, Any]]) -> None:
    history = load_history()
    history.append({"generated_at": datetime.now(timezone.utc).isoformat(), "repos": repos})
    HISTORY_FILE.write_text(json.dumps(history[-60:], ensure_ascii=False, indent=2), encoding="utf-8")


def fetch_repo_info(repo: str) -> dict[str, Any]:
    data = github_api(f"/repos/{repo}")
    if not isinstance(data, dict) or data.get("_error") or data.get("_rate_limited"):
        return {
            "error": data.get("message") or data.get("_error") or "无法获取信息",
            "source_repo": repo,
        }
    release = fetch_release_summary(repo)
    security_policy = fetch_security_policy(repo)
    return {
        "source_repo": repo,
        "resolved_full_name": data.get("full_name", repo),
        "stars": data.get("stargazers_count", 0),
        "forks": data.get("forks_count", 0),
        "open_issues_count": data.get("open_issues_count", 0),
        "last_push": data.get("pushed_at", ""),
        "updated_at": data.get("updated_at", ""),
        "default_branch": data.get("default_branch", ""),
        "archived": data.get("archived", False),
        "license": (data.get("license") or {}).get("spdx_id", ""),
        "url": data.get("html_url", ""),
        "latest_release": release,
        "has_security_policy": security_policy,
    }


def normalize_previous_snapshot(raw: dict[str, Any]) -> dict[str, dict[str, Any]]:
    if not isinstance(raw, dict):
        return {}
    if isinstance(raw.get("repos"), dict):
        return raw["repos"]
    if isinstance(raw.get("competitors"), dict):
        prev = dict(raw["competitors"])
    else:
        prev = {}
    for k, v in raw.items():
        if isinstance(v, dict) and "/" in k:
            prev[k] = v
    return prev


def load_snapshot() -> dict[str, dict[str, Any]]:
    if not SNAPSHOT_FILE.exists():
        return {}
    try:
        return normalize_previous_snapshot(json.loads(SNAPSHOT_FILE.read_text(encoding="utf-8")))
    except Exception:
        return {}


def fetch_head_sha(repo: str) -> str:
    commits = github_api(f"/repos/{repo}/commits?per_page=1")
    if isinstance(commits, list) and commits and isinstance(commits[0], dict):
        return str(commits[0].get("sha") or "")
    return ""


def unseen_commit_shas(repo: str, baseline_sha: str, head_sha: str) -> list[str]:
    """Return commits introduced after the prior analyzed SHA, newest first."""
    if not head_sha or head_sha == baseline_sha:
        return []
    if not baseline_sha:
        return [head_sha]
    compared = github_api(f"/repos/{repo}/compare/{baseline_sha}...{head_sha}")
    commits = compared.get("commits", []) if isinstance(compared, dict) else []
    shas = [str(item.get("sha") or "") for item in commits if isinstance(item, dict)]
    return [sha for sha in shas if sha]


def load_candidate_pool() -> dict[str, Any]:
    if not CANDIDATE_POOL_FILE.exists():
        return {"schema_version": 1, "candidates": {}}
    try:
        data = json.loads(CANDIDATE_POOL_FILE.read_text(encoding="utf-8"))
        if isinstance(data, dict) and isinstance(data.get("candidates"), dict):
            return data
    except Exception:
        pass
    return {"schema_version": 1, "candidates": {}}


def save_candidate_pool(pool: dict[str, Any]) -> None:
    CANDIDATE_POOL_FILE.parent.mkdir(parents=True, exist_ok=True)
    CANDIDATE_POOL_FILE.write_text(json.dumps(pool, ensure_ascii=False, indent=2), encoding="utf-8")


def upsert_candidate(candidate: dict[str, Any]) -> dict[str, Any]:
    """Persist one candidate with an append-only decision history."""
    repo = str(candidate.get("repo") or "").strip()
    if not repo:
        raise ValueError("candidate repo is required")
    pool = load_candidate_pool()
    current = dict(pool["candidates"].get(repo) or {})
    history = list(current.get("history") or [])
    history.append({**candidate, "recorded_at": datetime.now(timezone.utc).isoformat()})
    current.update(candidate)
    current["history"] = history[-20:]
    pool["candidates"][repo] = current
    pool["updated_at"] = datetime.now(timezone.utc).isoformat()
    save_candidate_pool(pool)
    return current


def save_snapshot(repos: dict[str, dict[str, Any]], competitors: dict[str, list[str]]) -> None:
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "sources": {
            "competitors": str(COMPETITORS_MD),
        },
        "counts": {
            "categories": len(competitors),
            "repos": len(repos),
        },
        "repos": repos,
    }
    SNAPSHOT_FILE.parent.mkdir(parents=True, exist_ok=True)
    SNAPSHOT_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    append_history(repos)


def days_since_iso(iso: str) -> int:
    if not iso:
        return 999
    try:
        dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
        return (datetime.now(dt.tzinfo) - dt).days
    except Exception:
        return 999


def parse_extension(path: str) -> str:
    p = path.lower()
    if p.endswith(".tar.gz"):
        return ".tar.gz"
    idx = p.rfind(".")
    return p[idx:] if idx >= 0 else ""


def is_code_file(path: str) -> bool:
    return parse_extension(path) in CODE_EXTENSIONS


def is_doc_file(path: str) -> bool:
    return parse_extension(path) in DOC_EXTENSIONS


def is_code_only_noise(path: str) -> bool:
    # 仅做“噪声”判断的保守规则
    p = path.lower()
    return any(k in p for k in ("readme", "license", "changelog", "agents", ".github/workflows", "ci", "release", "dockerfile", "makefile", "pyproject.toml", "package.json", ".lock"))


def candidate_state(triage: str) -> str:
    return {
        "可融合候选": "pending_review",
        "观察/人工复核": "watching",
        "仅记录": "recorded",
    }.get(triage, "recorded")


def semantic_change_signals(files: list[dict[str, Any]]) -> dict[str, Any]:
    """Extract deterministic semantic hints from changed paths and diff additions."""
    tags: set[str] = set()
    symbols: list[str] = []
    for item in files:
        path = str(item.get("filename") or "").lower()
        patch = str(item.get("patch") or "")
        if any(token in path for token in ("runtime/", "core/", "orchestr", "router")):
            tags.add("runtime")
        if any(token in path for token in ("schema", "openapi", "contract")):
            tags.add("schema")
        if any(token in path for token in ("permission", "capabilit", "auth", "policy")):
            tags.add("permission")
        if "/test" in path or path.startswith("test"):
            tags.add("test_harness")
        for match in re.finditer(r"^\+\s*(?:class|def|async\s+def)\s+([A-Za-z_]\w*)", patch, re.MULTILINE):
            name = match.group(1)
            if name not in symbols:
                symbols.append(name)
    if symbols:
        tags.add("new_symbol")
    return {"tags": sorted(tags), "new_symbols": symbols[:20]}


def commit_fusion_signal(repo: str, commit_shas: list[str] | None = None) -> dict[str, Any]:
    commits = ([{"sha": sha} for sha in commit_shas] if commit_shas else github_api(f"/repos/{repo}/commits?per_page=3"))
    if not isinstance(commits, list):
        return {
            "repo": repo,
            "status": "fetch_error",
            "commits_examined": 0,
            "code_files": 0,
            "doc_files": 0,
            "files_total": 0,
            "additions": 0,
            "deletions": 0,
            "code_change_score": 0,
            "triage": "记录",
            "sample_paths": [],
            "commit_messages": [],
            "reason": commits.get("message") if isinstance(commits, dict) else "无法获取 commit 列表",
        }

    score = 0
    files_total = 0
    code_files = 0
    doc_files = 0
    additions = 0
    deletions = 0
    sample_paths: list[str] = []
    commit_messages: list[str] = []
    core_path_hits = 0
    noisy_only = True
    semantic_files: list[dict[str, Any]] = []

    for item in commits[:3]:
        sha = item.get("sha") if isinstance(item, dict) else None
        if not sha:
            continue
        msg = ((item.get("commit") or {}).get("message") or "") if isinstance(item, dict) else ""
        msg = re.sub(r"\s+", " ", msg).strip()
        if msg:
            commit_messages.append(msg[:120] if len(msg) <= 120 else msg[:117] + "...")
        detail = github_api(f"/repos/{repo}/commits/{sha}")
        if not isinstance(detail, dict):
            continue
        files = detail.get("files") or []
        for f in files:
            if not isinstance(f, dict):
                continue
            path = f.get("filename", "")
            if not path:
                continue
            files_total += 1
            sample_paths.append(path)

            is_doc = is_doc_file(path)
            is_code = is_code_file(path)
            if is_code:
                code_files += 1
                noisy_only = False
            elif not is_doc:
                noisy_only = False
            if is_doc:
                doc_files += 1

            additions += int(f.get("additions", 0) or 0)
            deletions += int(f.get("deletions", 0) or 0)

            p = path.lower()
            if any(k in p for k in CORE_PATH_KEYWORDS):
                core_path_hits += 1
            if is_code_only_noise(p):
                pass

    # 分数规则（严格对齐 monitor-driven-fusion-triage）
    if code_files >= 5:
        score += 3
    if additions >= 300 and code_files > 0:
        score += 2
    if core_path_hits > 0:
        score += 1
    msgs = " ".join(commit_messages).lower()
    if any(k in msgs for k in COMMIT_SCORE_KEYWORDS):
        score += 1

    if files_total > 0:
        if code_files == 0 and doc_files >= files_total:
            score -= 3  # 纯文档更新
        if noisy_only and files_total > 0 and additions <= 120:
            score -= 2

    if score >= 4:
        triage = "可融合候选"
    elif score >= 1:
        triage = "观察/人工复核"
    else:
        triage = "仅记录"

    semantic = semantic_change_signals(semantic_files)
    return {
        "repo": repo,
        "status": "ok",
        "commits_examined": min(3, len(commits)),
        "code_files": code_files,
        "doc_files": doc_files,
        "files_total": files_total,
        "additions": additions,
        "deletions": deletions,
        "code_change_score": score,
        "triage": triage,
        "sample_paths": sample_paths[:10],
        "commit_messages": commit_messages[:5],
        "semantic_signals": semantic,
    }


def print_fusion_summary(category: str, repo: str, triage: dict[str, Any], products: list[str]) -> None:
    products_txt = ", ".join(products) if products else "（未映射）"
    score = triage.get("code_change_score", 0)
    msg = triage.get("triage", "仅记录")
    files_total = triage.get("files_total", 0)
    code_files = triage.get("code_files", 0)
    additions = triage.get("additions", 0)
    deletions = triage.get("deletions", 0)
    commits = triage.get("commits_examined", 0)
    sample = ", ".join((triage.get("sample_paths") or [])[:3])
    print(f"  🧭 [{msg}] {repo} | score={score} | 文件 {files_total} / code {code_files} / +{additions}/-{deletions} | 对应产品: {products_txt}")
    print(f"     commit{'s' if commits != 1 else ''}={commits} paths={sample}")


def main() -> int:
    parser = argparse.ArgumentParser(description="竞品监控日报（含融合分诊）")
    parser.add_argument("--no-scan", action="store_true", help="跳过 commit 级融合分诊，仅输出数值告警")
    args = parser.parse_args()

    print("🔍 竞品仓库监控日报 v3")
    print("=" * 62)

    try:
        competitors = parse_competitors_md()
        product_map = parse_product_categories()
    except Exception as e:
        print(f"❌ {e}")
        return 2

    print(f"数据源: {COMPETITORS_MD}")
    print(f"产品映射: {PRODUCT_LIST_MD}")
    unique_repos = []
    seen = set()
    for repos in competitors.values():
        for r in repos:
            if r not in seen:
                seen.add(r)
                unique_repos.append(r)

    print(f"监控范围: {len(competitors)} 个分类 / {len(unique_repos)} 个唯一竞品仓库")
    print("口径: Stars/Forks/Issues/Pushed 均来自 GitHub API 原始值；delta 来自 schema-v2 快照；score 为近3次 commit 代码变化评分")

    prev = load_snapshot()
    current: dict[str, dict[str, Any]] = {}
    alerts: list[str] = []
    errors: list[str] = []
    fusion_records: list[dict[str, Any]] = []

    for category, repos in competitors.items():
        print(f"\n📂 {category}")
        products = map_category_to_products(category, product_map)
        for source_repo in repos:
            info = fetch_repo_info(source_repo)
            if "error" in info:
                line = f"  ❌ {source_repo}: {info['error']}"
                print(line)
                errors.append(line.strip())
                continue

            key = info["resolved_full_name"]
            prev_info = prev.get(key) or prev.get(source_repo) or {}
            stars_delta = info["stars"] - int(prev_info.get("stars", info["stars"]) or 0)
            forks_delta = info["forks"] - int(prev_info.get("forks", info["forks"]) or 0)
            pushed_days = days_since_iso(info.get("last_push", ""))

            head_sha = fetch_head_sha(key)
            history = load_history()
            trends = trend_windows(key, int(info["stars"]), history, datetime.now(timezone.utc).isoformat())
            repo_record = {
                **info,
                **trends,
                "head_sha": head_sha,
                "category": category,
                "stars_delta": stars_delta,
                "forks_delta": forks_delta,
                "pushed_days": pushed_days,
                "checked_at": datetime.now(timezone.utc).isoformat(),
            }
            current[key] = repo_record

            delta_txt = f"Δ⭐{stars_delta:+d} Δ🍴{forks_delta:+d}"
            print(f"  ✅ {source_repo} → {key}: ⭐{info['stars']} 🍴{info['forks']} Issues:{info['open_issues_count']} Pushed:{info['last_push'][:10]} {delta_txt}")

            starred = stars_delta >= ALERT_STARS
            pushed = pushed_days <= ALERT_PUSH_DAYS
            if starred or pushed:
                if starred:
                    alerts.append(f"📈 {key}: +{stars_delta}⭐ (now {info['stars']}⭐)")
                if pushed:
                    alerts.append(f"🆕 {key}: 最近3天有更新（{info['last_push'][:10]}）")

                if not args.no_scan:
                    unseen = unseen_commit_shas(key, str(prev_info.get("head_sha") or ""), head_sha)
                    if unseen:
                        triage = commit_fusion_signal(key, unseen[:3])
                        triage_item = {
                            "category": category,
                            "competitor": source_repo,
                            "resolved_repo": key,
                            "products": products,
                            "unseen_shas": unseen,
                            "triage": triage,
                        }
                        fusion_records.append(triage_item)
                        upsert_candidate({
                            "repo": key, "head_sha": head_sha, "status": candidate_state(triage.get("triage", "仅记录")),
                            "triage": triage.get("triage", "仅记录"),
                            "category": category, "products": products, "score": triage.get("code_change_score", 0),
                            "unseen_shas": unseen,
                        })
                    else:
                        print(f"  ↪ {key}: 无未分析 commit，跳过融合分诊")

            time.sleep(DELAY_SECONDS)

    save_snapshot(current, competitors)

    print("\n" + "=" * 62)
    print("📊 监控总结")
    print(f"  分类数: {len(competitors)}")
    print(f"  清单唯一仓库数: {len(unique_repos)}")
    print(f"  成功检查: {len(current)}")
    print(f"  错误数: {len(errors)}")
    print(f"  告警数: {len(alerts)}")
    print(f"  快照: {SNAPSHOT_FILE} (schema_version={SCHEMA_VERSION})")

    if alerts:
        print("⚠️ 关注更新（脚本原始判断，非LLM重算）")
        for a in alerts:
            print(f"  {a}")

    # 融合分诊
    if not args.no_scan:
        candidate_count = sum(1 for r in fusion_records if r["triage"].get("triage") == "可融合候选")
        review_count = sum(1 for r in fusion_records if r["triage"].get("triage") == "观察/人工复核")
        record_count = sum(1 for r in fusion_records if r["triage"].get("triage") == "仅记录")
        print("\n" + "=" * 62)
        print("🧠 竞品融合分诊（基于最近3次commit）")
        print(f"  可融合候选: {candidate_count} | 观察/复核: {review_count} | 仅记录: {record_count}")
        for item in fusion_records:
            triage = item["triage"]
            repo = item["resolved_repo"]
            cat = item["category"]
            print(f"  [ {cat} ] {repo}")
            print_fusion_summary(cat, repo, triage, item["products"])
            if triage.get("commit_messages"):
                print(f"     最近commit: {'; '.join(triage['commit_messages'][:3])}")

    if errors:
        print("❌ 获取失败清单")
        for e in errors:
            print(f"  {e}")

    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
