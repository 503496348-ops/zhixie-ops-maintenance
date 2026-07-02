#!/usr/bin/env python3
"""
竞品持续监控脚本 v2

事实源：../references/competitors.md（或 ZHIXIE_OPS_SKILL_DIR 指定目录）
快照：../references/competitor-snapshot.json

设计原则：
- GitHub 认证只读 GITHUB_TOKEN 或 gh auth token，禁止硬编码凭据。
- 每次保存 schema_version=2 的单一结构，旧 nested/flat 混合快照只用于兼容读取，不再续写。
- 输出只包含脚本实查原始数值和 delta，避免 LLM 二次总结重算。
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from functools import lru_cache
from pathlib import Path
from typing import Any

SKILL_DIR = Path(os.environ.get("ZHIXIE_OPS_SKILL_DIR", Path(__file__).resolve().parents[1]))
COMPETITORS_MD = SKILL_DIR / "references" / "competitors.md"
SNAPSHOT_FILE = SKILL_DIR / "references" / "competitor-snapshot.json"
SCHEMA_VERSION = 2
GITHUB_API = "https://api.github.com"


def parse_competitors_md() -> dict[str, list[str]]:
    if not COMPETITORS_MD.exists():
        raise FileNotFoundError(f"竞品清单不存在: {COMPETITORS_MD}")
    competitors: dict[str, list[str]] = {}
    for line in COMPETITORS_MD.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line.startswith("|") or line.startswith("|--") or line.startswith("| 分类"):
            continue
        cols = [c.strip() for c in line.split("|") if c.strip()]
        if len(cols) < 2:
            continue
        category = cols[0]
        repos: list[str] = []
        for cell in cols[1:]:
            if cell == "—":
                continue
            match = re.match(r"([\w\-.]+/[\w\-.]+)", cell)
            if match:
                repos.append(match.group(1))
        if repos:
            competitors[category] = repos
    return competitors


@lru_cache(maxsize=1)
def get_github_token() -> str:
    token = os.environ.get("GITHUB_TOKEN", "").strip()
    if token:
        return token
    try:
        r = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True, timeout=5)
        if r.returncode == 0:
            return r.stdout.strip()
    except Exception:
        pass
    return ""


def github_api(path_or_url: str) -> Any | None:
    url = path_or_url if path_or_url.startswith("http") else f"{GITHUB_API}{path_or_url}"
    headers = ["-H", "Accept: application/vnd.github.v3+json"]
    token = get_github_token()
    if token:
        headers.extend(["-H", f"Authorization: token {token}"])
    try:
        result = subprocess.run(["curl", "-sS"] + headers + [url], capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            return None
        data = json.loads(result.stdout)
        if isinstance(data, dict) and data.get("message"):
            msg = str(data.get("message", ""))
            if "rate limit" in msg.lower():
                return {"_rate_limited": True, "message": msg}
            if msg in {"Not Found", "Bad credentials"} or "API rate limit" in msg:
                return {"_error": msg}
        return data
    except Exception as e:
        return {"_error": str(e)}


def fetch_repo_info(repo: str) -> dict[str, Any]:
    data = github_api(f"/repos/{repo}")
    if not isinstance(data, dict) or data.get("_error") or data.get("_rate_limited"):
        return {"repo": repo, "error": data.get("message") or data.get("_error") or "无法获取信息" if isinstance(data, dict) else "无法获取信息"}
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
    }


def normalize_previous_snapshot(raw: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Return previous repo snapshot keyed by canonical/source repo.

    Supports:
    - schema v2: {repos:{full_name:{...}}}
    - old flat: {owner/repo:{stars,...}}
    - old nested: {competitors:{owner/repo:{stars,...}}}
    """
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


def save_snapshot(repos: dict[str, dict[str, Any]], competitors: dict[str, list[str]]) -> None:
    snapshot = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "sources": {"competitors": str(COMPETITORS_MD)},
        "counts": {
            "categories": len(competitors),
            "repos": len(repos),
        },
        "repos": repos,
    }
    SNAPSHOT_FILE.parent.mkdir(parents=True, exist_ok=True)
    SNAPSHOT_FILE.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2), encoding="utf-8")


def days_since_iso(iso: str) -> int:
    if not iso:
        return 999
    try:
        d = datetime.fromisoformat(iso.replace("Z", "+00:00"))
        return (datetime.now(d.tzinfo) - d).days
    except Exception:
        return 999


def main() -> int:
    print("🔍 竞品仓库监控日报 v2")
    print("=" * 60)
    try:
        competitors = parse_competitors_md()
    except Exception as e:
        print(f"❌ {e}")
        return 2

    unique_repos: list[str] = []
    seen = set()
    for repos in competitors.values():
        for repo in repos:
            if repo not in seen:
                seen.add(repo)
                unique_repos.append(repo)

    print(f"数据源: {COMPETITORS_MD}")
    print(f"监控范围: {len(competitors)} 个分类 / {len(unique_repos)} 个唯一竞品仓库")
    print("口径: Stars/Forks/Issues/Pushed 均来自 GitHub API 原始值；delta 来自 schema-v2 快照。")

    prev = load_snapshot()
    current: dict[str, dict[str, Any]] = {}
    alerts: list[str] = []
    errors: list[str] = []

    for category, repos in competitors.items():
        print(f"\n📂 {category}")
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
            repo_record = {
                **info,
                "category": category,
                "stars_delta": stars_delta,
                "forks_delta": forks_delta,
                "pushed_days": pushed_days,
                "checked_at": datetime.now(timezone.utc).isoformat(),
            }
            current[key] = repo_record
            delta_txt = f"Δ⭐{stars_delta:+d} Δ🍴{forks_delta:+d}"
            print(f"  ✅ {source_repo} → {key}: ⭐{info['stars']} 🍴{info['forks']} Issues:{info['open_issues_count']} Pushed:{info['last_push'][:10]} {delta_txt}")
            if stars_delta >= 50:
                alerts.append(f"📈 {key}: +{stars_delta}⭐ (now {info['stars']}⭐)")
            if pushed_days <= 3:
                alerts.append(f"🆕 {key}: 最近3天有更新（{info['last_push'][:10]}）")
            time.sleep(0.2)

    save_snapshot(current, competitors)

    print("\n" + "=" * 60)
    print("📊 监控总结")
    print(f"  分类数: {len(competitors)}")
    print(f"  清单唯一仓库数: {len(unique_repos)}")
    print(f"  成功检查: {len(current)}")
    print(f"  错误数: {len(errors)}")
    print(f"  告警数: {len(alerts)}")
    print(f"  快照: {SNAPSHOT_FILE} (schema_version={SCHEMA_VERSION})")
    if alerts:
        print("\n⚠️ 需要关注的更新（脚本原始判断，非LLM重算）")
        for a in alerts:
            print("  " + a)
    else:
        print("\n✅ 所有竞品暂无显著更新")
    if errors:
        print("\n❌ 获取失败清单")
        for e in errors:
            print("  " + e)
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
