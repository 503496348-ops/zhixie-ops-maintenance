#!/usr/bin/env python3
"""
智械工坊产品仓库日报 — 飞书交互卡片版 v5
以 product-list.md 为产品单一数据源；competitors.md 为竞品单一数据源；snapshot 使用 schema v2，禁止硬编码清单/凭据。
"""
import json
import hashlib
import os
import re
import subprocess
import sys
from functools import lru_cache
from datetime import datetime, timezone
from pathlib import Path

# ── 配置 ──
GITHUB_ORG = "503496348-ops"
CARD_HEADER_COLOR = "indigo"
GITHUB_API = "https://api.github.com"
SNAPSHOT_PATH = "/root/.hermes/scripts/repo-snapshot.json"
SENT_MARKER_PATH = "/root/.hermes/scripts/product-repo-card-sent.json"
SNAPSHOT_SCHEMA_VERSION = 2
@lru_cache(maxsize=1)
def get_github_token() -> str:
    """Prefer env token; fall back to gh CLI auth token. Never hardcode credentials."""
    token = os.environ.get("GITHUB_TOKEN", "")
    if token:
        return token
    try:
        r = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True, timeout=5)
        if r.returncode == 0:
            return r.stdout.strip()
    except Exception:
        pass
    return ""


# ── 单一数据源：从 product-list.md 读取 ──
SKILL_DIR = Path("/root/.hermes/shared/skills/product-repo-monitor")
PRODUCT_LIST_MD = SKILL_DIR / "references" / "product-list.md"
AUDIT_REPORT_PATH = SKILL_DIR / "references" / "audit-report.json"

def load_products_from_md() -> list[dict]:
    """从 product-list.md 解析产品列表，返回 [{name, name_en, repo, category, branch, status}, ...]。"""
    products = []
    if not PRODUCT_LIST_MD.exists():
        print(f"[WARN] product-list.md 不存在: {PRODUCT_LIST_MD}", file=sys.stderr)
        return products

    with open(PRODUCT_LIST_MD, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not re.match(r"^\|\s*\d+\s*\|", line):
                continue
            cols = [c.strip() for c in line.strip("|").split("|")]
            if len(cols) < 7:
                continue
            _, name, name_en, repo, category, branch, status = cols[:7]
            # 跳过仓库名为 — 的（未建仓）
            if repo and repo != "—":
                products.append({
                    "name": name,
                    "name_en": name_en,
                    "repo": repo,
                    "category": category,
                    "branch": branch,
                    "status": status,
                    "active": ("✅" in status),
                })
    return products

def load_audit_health() -> dict:
    """Read the latest local audit cache without triggering a second audit run."""
    unavailable = {"available": False, "healthy": 0, "attention": 0, "attention_products": [], "audit_date": ""}
    try:
        report = json.loads(AUDIT_REPORT_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return unavailable
    distribution = report.get("grade_distribution") or {}
    attention = [
        str(item.get("product") or item.get("repo") or "unknown")
        for item in report.get("results") or []
        if str(item.get("grade") or "") not in {"A", "N/A"}
    ]
    return {
        "available": True,
        "healthy": int(distribution.get("A", 0)),
        "attention": len(attention),
        "attention_products": attention[:8],
        "audit_date": str(report.get("audit_date") or "")[:10],
    }


# 启动时自动加载
PRODUCTS = load_products_from_md()
print(f"[INFO] 从 product-list.md 加载 {len(PRODUCTS)} 个产品")

# ── 竞品追踪：从 references/competitors.md 读取，禁止硬编码 ──
COMPETITORS_MD = SKILL_DIR / "references" / "competitors.md"

def load_competitors_from_md() -> dict[str, list[str]]:
    competitors: dict[str, list[str]] = {}
    if not COMPETITORS_MD.exists():
        print(f"[WARN] competitors.md 不存在: {COMPETITORS_MD}", file=sys.stderr)
        return competitors
    for line in COMPETITORS_MD.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line.startswith("|") or line.startswith("|--") or line.startswith("| 分类"):
            continue
        cols = [c.strip() for c in line.split("|") if c.strip()]
        if len(cols) < 2:
            continue
        repos = []
        for cell in cols[1:]:
            m = re.match(r"([\w\-.]+/[\w\-.]+)", cell)
            if m:
                repos.append(m.group(1))
        if repos:
            competitors[cols[0]] = repos
    return competitors

COMPETITORS = load_competitors_from_md()
print(f"[INFO] 从 competitors.md 加载 {len(COMPETITORS)} 个竞品分类，{sum(len(v) for v in COMPETITORS.values())} 个竞品仓库")


# ── GitHub API ──

def _curl_github(url: str):
    try:
        headers = ["-H", "Accept: application/vnd.github.v3+json"]
        token = get_github_token()
        if token:
            headers.extend(["-H", f"Authorization: token {token}"])
        r = subprocess.run(
            ["curl", "-s"] + headers + [url],
            capture_output=True, text=True, timeout=20,
        )
        if r.returncode != 0:
            return None
        data = json.loads(r.stdout)
        if isinstance(data, dict) and data.get("message") == "Not Found":
            return None
        return data
    except Exception:
        return None


def fetch_open_issue_count(repo_name: str) -> int:
    """获取真实 open issue 数，排除 GitHub API open_issues_count 中混入的 PR。"""
    total = 0
    page = 1
    while True:
        url = f"{GITHUB_API}/repos/{GITHUB_ORG}/{repo_name}/issues?state=open&per_page=100&page={page}"
        data = _curl_github(url)
        if not isinstance(data, list):
            return 0
        total += sum(1 for item in data if not item.get("pull_request"))
        if len(data) < 100:
            break
        page += 1
    return total


def fetch_repo_stats(repo_name: str) -> dict | None:
    """获取单个仓库的统计数据。"""
    url = f"{GITHUB_API}/repos/{GITHUB_ORG}/{repo_name}"
    data = _curl_github(url)
    if not isinstance(data, dict):
        return None
    return {
        "stars": data.get("stargazers_count", 0),
        "forks": data.get("forks_count", 0),
        "issues": fetch_open_issue_count(repo_name),
        "updated": data.get("updated_at", "")[:10],
        "pushed": data.get("pushed_at", "")[:10],
        "url": data.get("html_url", ""),
        "full_name": data.get("full_name", f"{GITHUB_ORG}/{repo_name}"),
        "default_branch": data.get("default_branch", ""),
        "archived": data.get("archived", False),
        "license": (data.get("license") or {}).get("spdx_id", ""),
        "description": data.get("description", "") or "",
    }


def fetch_all_repos() -> list:
    """拉取 org 下所有仓库（用于检测额外仓库）。"""
    all_repos = []
    page = 1
    while True:
        url = f"{GITHUB_API}/users/{GITHUB_ORG}/repos?per_page=100&page={page}&sort=updated"
        data = _curl_github(url)
        if not isinstance(data, list) or not data:
            break
        all_repos.extend(data)
        if len(data) < 100:
            break
        page += 1
    return all_repos


def days_since(date_str: str) -> int:
    try:
        d = datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        return (datetime.now(timezone.utc) - d).days
    except Exception:
        return 999


def freshness_emoji(days: int) -> str:
    if days <= 7:
        return "🟢"
    elif days <= 30:
        return "🟡"
    elif days <= 90:
        return "🟠"
    return "🔴"


# ── Snapshot persistence ──

def load_snapshot() -> dict:
    try:
        with open(SNAPSHOT_PATH, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_snapshot(date_str: str, products_data: list, competitors_data: dict):
    """Persist a normalized schema-v2 snapshot.

    Shape:
    {
      schema_version, generated_at, sources, products:{repo:{...}}, competitors:{full_name:{...}}
    }
    Old snapshots are only read for delta calculation; every save rewrites to one schema.
    """
    snap = {
        "schema_version": SNAPSHOT_SCHEMA_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "date": date_str,
        "sources": {
            "products": str(PRODUCT_LIST_MD),
            "competitors": str(COMPETITORS_MD),
            "github_org": GITHUB_ORG,
        },
        "counts": {
            "products_total": len(products_data),
            "products_with_repo": sum(1 for p in products_data if p.get("has_repo")),
            "competitor_categories": len(COMPETITORS),
            "competitor_repos": len(competitors_data),
        },
        "products": {},
        "competitors": {},
    }
    for p in products_data:
        if p.get("repo"):
            snap["products"][p["repo"]] = {
                "name": p.get("name", ""),
                "name_en": p.get("name_en", ""),
                "category": p.get("category", ""),
                "source_repo": p.get("repo", ""),
                "resolved_full_name": p.get("full_name", f"{GITHUB_ORG}/{p.get('repo', '')}"),
                "default_branch": p.get("default_branch", p.get("branch", "")),
                "archived": p.get("archived", False),
                "stars": p.get("stars", 0),
                "forks": p.get("forks", 0),
                "issues": p.get("issues", 0),
                "has_repo": p.get("has_repo", False),
                "updated": p.get("updated", ""),
                "pushed": p.get("pushed", ""),
                "url": p.get("url", ""),
            }
    for repo, info in competitors_data.items():
        key = info.get("full_name") or repo
        snap["competitors"][key] = {
            "source_repo": repo,
            "resolved_full_name": key,
            "stars": info.get("stars", 0),
            "forks": info.get("forks", 0),
            "issues": info.get("issues", 0),
            "updated": info.get("updated", ""),
            "pushed": info.get("pushed", ""),
            "default_branch": info.get("default_branch", ""),
            "archived": info.get("archived", False),
            "license": info.get("license", ""),
            "url": info.get("url", ""),
        }
    os.makedirs(os.path.dirname(SNAPSHOT_PATH), exist_ok=True)
    with open(SNAPSHOT_PATH, "w", encoding="utf-8") as f:
        json.dump(snap, f, ensure_ascii=False, indent=2)


def compute_product_diffs(products_data: list, prev_snap: dict) -> list:
    diffs = []
    prev_products = prev_snap.get("products", {})
    for p in products_data:
        if not p.get("repo"):
            continue
        prev = prev_products.get(p["repo"])
        if not prev:
            if p.get("has_repo"):
                diffs.append(f"🆕 **{p['name']}**: 仓库已创建 ({p.get('stars', 0)}⭐)")
            continue
        star_diff = p.get("stars", 0) - prev.get("stars", 0)
        if star_diff > 0:
            diffs.append(f"📈 **{p['name']}**: +{star_diff}⭐ (now {p['stars']}⭐)")
        elif star_diff < 0:
            diffs.append(f"📉 **{p['name']}**: {star_diff}⭐ (now {p['stars']}⭐)")
        issue_diff = p.get("issues", 0) - prev.get("issues", 0)
        if issue_diff > 0:
            diffs.append(f"⚠️ **{p['name']}**: 新增 {issue_diff} 个 Issue")
        elif issue_diff < 0:
            diffs.append(f"✅ **{p['name']}**: 关闭 {abs(issue_diff)} 个 Issue")
    return diffs


def fetch_github_repo(owner_repo: str) -> dict | None:
    url = f"{GITHUB_API}/repos/{owner_repo}"
    data = _curl_github(url)
    if not isinstance(data, dict):
        return None
    return {
        "stars": data.get("stargazers_count", 0),
        "forks": data.get("forks_count", 0),
        "issues": data.get("open_issues_count", 0),
        "updated": data.get("updated_at", "")[:10],
        "pushed": data.get("pushed_at", "")[:10],
        "url": data.get("html_url", ""),
        "full_name": data.get("full_name", owner_repo),
        "default_branch": data.get("default_branch", ""),
        "archived": data.get("archived", False),
        "license": (data.get("license") or {}).get("spdx_id", ""),
    }


# ── Build card ──

def build_card(products_data: list, competitor_changes: dict, product_diffs: list, extra_repos: list, competitors_data: dict = None, is_first_run: bool = False, audit_health: dict | None = None) -> dict:
    date_str = datetime.now().strftime("%Y-%m-%d")
    with_repo = [p for p in products_data if p.get("has_repo")]
    without_repo = [p for p in products_data if not p.get("has_repo")]
    total_stars = sum(p.get("stars", 0) for p in with_repo)
    active_30d = sum(1 for p in with_repo if p.get("days", 999) <= 30)
    alert_count = sum(1 for p in with_repo if p.get("active", True) and (p.get("days", 999) > 30 or p.get("issues", 0) > 0))

    # 有仓库的产品表格
    rows = []
    for p in with_repo:
        emoji = freshness_emoji(p.get("days", 999))
        if not p.get("active", True):
            status = "📦 非活跃"
        else:
            status = "🟢 正常" if p.get("issues", 0) == 0 and p.get("days", 999) <= 30 else "⚠️ 关注"
        rows.append({
            "status": status,
            "product": f'[{p["name"]}]({p["url"]})' if p.get("url") else p["name"],
            "stars": str(p.get("stars", 0)),
            "forks": str(p.get("forks", 0)),
            "issues": f'🔴 {p["issues"]}' if p.get("issues", 0) > 0 else "0",
            "updated": p.get("pushed", p.get("updated", "—")),
            "freshness": f'{emoji} {p.get("days", "?")}天',
        })

    elements = [
        {"tag": "column_set", "flex_mode": "stretch", "background_style": "grey", "columns": [
            {"tag": "column", "width": "weighted", "weight": 1, "vertical_align": "center",
             "elements": [{"tag": "div", "text": {"tag": "lark_md", "content": f"📦 **{len(products_data)}**\n产品总数"}}]},
            {"tag": "column", "width": "weighted", "weight": 1, "vertical_align": "center",
             "elements": [{"tag": "div", "text": {"tag": "lark_md", "content": f"🔗 **{len(with_repo)}**\n有仓库"}}]},
            {"tag": "column", "width": "weighted", "weight": 1, "vertical_align": "center",
             "elements": [{"tag": "div", "text": {"tag": "lark_md", "content": f"⭐ **{total_stars}**\n总 Stars"}}]},
            {"tag": "column", "width": "weighted", "weight": 1, "vertical_align": "center",
             "elements": [{"tag": "div", "text": {"tag": "lark_md", "content": f"🔥 **{active_30d}**\n近30天活跃"}}]},
            {"tag": "column", "width": "weighted", "weight": 1, "vertical_align": "center",
             "elements": [{"tag": "div", "text": {"tag": "lark_md", "content": f"⚠️ **{alert_count}**\n需关注"}}]},
        ]},
        {"tag": "hr"},
        {"tag": "table", "columns": [
            {"data_type": "text", "display_name": "状态", "name": "status", "width": "auto"},
            {"data_type": "text", "display_name": "产品", "name": "product", "width": "auto"},
            {"data_type": "text", "display_name": "⭐", "name": "stars", "width": "auto"},
            {"data_type": "text", "display_name": "🍴", "name": "forks", "width": "auto"},
            {"data_type": "text", "display_name": "Issues", "name": "issues", "width": "auto"},
            {"data_type": "text", "display_name": "最后推送", "name": "updated", "width": "auto"},
            {"data_type": "text", "display_name": "新鲜度", "name": "freshness", "width": "auto"},
        ], "header_style": {"background_style": "grey", "bold": True, "lines": 1, "text_align": "center"},
         "page_size": 20, "rows": rows},
    ]

    # 最近一次产品质量审计（只读取缓存，日报不隐式触发重审）
    if audit_health and audit_health.get("available"):
        attention_names = "、".join(audit_health.get("attention_products") or []) or "无"
        elements.append({"tag": "hr"})
        elements.append({"tag": "markdown", "content": (
            "**🩺 质量健康（最近审计）**\n"
            f"A级：{audit_health.get('healthy', 0)} ｜需关注：{audit_health.get('attention', 0)} ｜"
            f"审计日期：{audit_health.get('audit_date') or '未知'}\n"
            f"关注产品：{attention_names}"
        )})

    # 未建仓产品
    if without_repo:
        no_repo_lines = ["**📭 尚未建仓的产品**"]
        for p in without_repo:
            no_repo_lines.append(f"  {p['name']}（{p['name_en']}）— {p['category']}")
        elements.append({"tag": "hr"})
        elements.append({"tag": "markdown", "content": "\n".join(no_repo_lines)})

    # 告警
    alerts = []
    for p in with_repo:
        if not p.get("active", True):
            continue
        if p.get("days", 999) > 90:
            alerts.append(f'🔴 **{p["name"]}**：已 {p["days"]} 天未推送')
        elif p.get("days", 999) > 30:
            alerts.append(f'🟠 **{p["name"]}**：已 {p["days"]} 天未推送')
        if p.get("issues", 0) > 0:
            alerts.append(f'⚠️ **{p["name"]}**：有 {p["issues"]} 个未关闭 Issue')
    if alerts:
        elements.append({"tag": "hr"})
        elements.append({"tag": "markdown", "content": "**📋 需关注项**\n" + "\n".join(alerts)})

    # 产品变更
    if product_diffs:
        elements.append({"tag": "hr"})
        elements.append({"tag": "markdown", "content": "**📊 产品变更**\n" + "\n".join(product_diffs)})

    # 额外仓库（非产品）
    if extra_repos:
        extra_lines = ["**🔍 额外仓库（非产品，不计入统计）**"]
        for r in extra_repos:
            arch = "📦已归档" if r.get("archived") else ""
            extra_lines.append(f"  {r['name']} — ⭐{r.get('stargazers_count', 0)} {arch}")
        elements.append({"tag": "hr"})
        elements.append({"tag": "markdown", "content": "\n".join(extra_lines)})

    # 竞品对标（有diff显示变化，首次跑显示基线）
    if competitor_changes:
        comp_lines = []
        for category, changes in competitor_changes.items():
            if not changes:
                continue
            comp_lines.append(f"**{category}**")
            for c in changes:
                comp_lines.append(f"  {c}")
        if comp_lines:
            elements.append({"tag": "hr"})
            elements.append({"tag": "markdown", "content": "**🔍 竞品动态**\n" + "\n".join(comp_lines)})
    elif competitors_data and is_first_run:
        # 首次运行无旧快照，展示当前竞品基线
        needed_categories = set(p.get("category", "") for p in products_data)
        comp_lines = ["**🔍 竞品对标（基线快照，明日开始对比变化）**"]
        for cat in sorted(needed_categories):
            repos = COMPETITORS.get(cat, [])
            if not repos:
                continue
            cat_items = []
            for repo in repos:
                info = competitors_data.get(repo, {})
                if info:
                    cat_items.append(f"  {repo}: ⭐{info.get('stars', 0)}")
            if cat_items:
                comp_lines.append(f"**{cat}**")
                comp_lines.extend(cat_items)
        if len(comp_lines) > 1:
            elements.append({"tag": "hr"})
            elements.append({"tag": "markdown", "content": "\n".join(comp_lines)})

    elements.append({"tag": "note", "elements": [{"tag": "plain_text", "content": f"🤖 自动生成 · {date_str} · v5 schema-v2 · 产品源: product-list.md · 竞品源: competitors.md · 数据源: GitHub API 原始数值"}]})

    return {
        "config": {"wide_screen_mode": True},
        "header": {"title": {"tag": "plain_text", "content": f"🏗️ 智械工坊产品仓库日报 · {date_str}"}, "template": CARD_HEADER_COLOR},
        "elements": elements,
    }


def send_card(card: dict, chat_id: str) -> bool:
    profile = os.environ.get("HERMES_LARK_CLI_PROFILE", "default")
    content = json.dumps(card, ensure_ascii=False)
    try:
        r = subprocess.run(
            ["lark-cli", "--profile", profile, "im", "+messages-send",
             "--chat-id", chat_id, "--msg-type", "interactive", "--content", content, "--as", "bot"],
            capture_output=True, text=True, timeout=30,
        )
        if r.returncode == 0:
            print(f"[OK] 卡片已发送到 {chat_id}")
            return True
        print(f"[ERROR] lark-cli: {r.stderr[:300]}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        return False


def sent_marker_key(date_str: str, chat_id: str) -> str:
    """Stable per-day/per-chat key without storing chat IDs in the marker file."""
    chat_hash = hashlib.sha256(chat_id.encode("utf-8")).hexdigest()[:16]
    return f"{date_str}:{chat_hash}"


def load_sent_markers() -> dict:
    try:
        p = Path(SENT_MARKER_PATH)
        if not p.exists():
            return {}
        data = json.loads(p.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except Exception as e:
        print(f"[WARN] 读取发送幂等标记失败，将继续执行: {e}", file=sys.stderr)
        return {}


def already_sent_today(date_str: str, chat_id: str) -> bool:
    return sent_marker_key(date_str, chat_id) in load_sent_markers()


def mark_sent(date_str: str, chat_id: str) -> None:
    markers = load_sent_markers()
    markers[sent_marker_key(date_str, chat_id)] = {
        "date": date_str,
        "sent_at": datetime.now().isoformat(timespec="seconds"),
        "script": "product-repo-card.py",
    }
    markers = {k: v for k, v in markers.items() if isinstance(v, dict) and v.get("date") == date_str}
    Path(SENT_MARKER_PATH).write_text(json.dumps(markers, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    if "--help" in sys.argv or "-h" in sys.argv:
        print("Usage: product-repo-card.py [--dry-run]\n\nGenerates the product repository report card.\n  --dry-run  generate card and snapshot without sending to Feishu")
        return
    if "--dry-run" in sys.argv:
        os.environ["PRODUCT_MONITOR_DRY_RUN"] = "1"

    chat_id = os.environ.get("FEISHU_CHAT_ID", "oc_44b5962120c4c149fe672acdb59a62db")
    date_str = datetime.now().strftime("%Y-%m-%d")

    prev_snap = load_snapshot()

    # ── 以 product-list.md 产品清单为准，逐个拉 GitHub 统计 ──
    print(f"[INFO] 产品总数: {len(PRODUCTS)}（Bitable 权威）")
    products_data = []
    for p in PRODUCTS:
        info = {
            "name": p["name"],
            "name_en": p["name_en"],
            "repo": p["repo"],
            "category": p["category"],
            "branch": p.get("branch", ""),
            "status": p.get("status", ""),
            "active": p.get("active", True),
            "has_repo": False,
            "stars": 0, "forks": 0, "issues": 0,
            "updated": "", "pushed": "", "url": "", "days": 999,
        }
        if p["repo"]:
            rd = fetch_repo_stats(p["repo"])
            if rd:
                info.update(rd)
                info["has_repo"] = True
                info["days"] = days_since(rd.get("pushed", "") or rd.get("updated", ""))
            else:
                print(f"[WARN] 仓库 {p['repo']} 在 GitHub 上不存在或 API 失败")
        products_data.append(info)

    with_repo = sum(1 for p in products_data if p["has_repo"])
    without_repo = len(products_data) - with_repo
    print(f"[INFO] 有仓库: {with_repo}, 未建仓: {without_repo}")

    # ── 检测额外仓库（非产品的 GitHub 仓库） ──
    product_repos = {p["repo"] for p in PRODUCTS if p["repo"]}
    # 排除 config 仓库
    exclude_patterns = ["-hermes-config", "openclaw-"]
    all_repos = fetch_all_repos()
    extra_repos = []
    for r in all_repos:
        name = r["name"]
        if name in product_repos:
            continue
        if any(pat in name for pat in exclude_patterns):
            continue
        extra_repos.append(r)
    if extra_repos:
        print(f"[INFO] 额外仓库（非产品）: {len(extra_repos)} 个")

    # ── 竞品数据 ──
    needed_categories = set(p["category"] for p in PRODUCTS)
    all_competitors = set()
    for cat in needed_categories:
        for repo in COMPETITORS.get(cat, []):
            all_competitors.add(repo)

    competitors_data = {}
    for repo in sorted(all_competitors):
        rd = fetch_github_repo(repo)
        if rd:
            competitors_data[repo] = rd
        else:
            competitors_data[repo] = {"stars": 0, "forks": 0, "issues": 0, "updated": "", "pushed": ""}

    product_diffs = compute_product_diffs(products_data, prev_snap)

    prev_competitors = prev_snap.get("competitors", {})
    competitor_changes = {}
    for cat in sorted(needed_categories):
        changes = []
        for repo in COMPETITORS.get(cat, []):
            cur = competitors_data.get(repo, {})
            canonical = cur.get("full_name") or repo
            prev = prev_competitors.get(canonical) or prev_competitors.get(repo)
            if not prev:
                continue
            star_diff = cur.get("stars", 0) - prev.get("stars", 0)
            if star_diff > 0:
                changes.append(f"📈 {repo}: +{star_diff}⭐ (now {cur['stars']}⭐)")
            elif star_diff < 0:
                changes.append(f"📉 {repo}: {star_diff}⭐ (now {cur['stars']}⭐)")
            pushed = cur.get("pushed", "")
            if pushed and days_since(pushed) <= 3:
                changes.append(f"🆕 {repo}: 最近3天有更新")
        if changes:
            competitor_changes[cat] = changes

    is_first_run = not prev_snap.get("products")
    audit_health = load_audit_health()
    card = build_card(products_data, competitor_changes, product_diffs, extra_repos, competitors_data, is_first_run, audit_health)
    dry_run = os.environ.get("PRODUCT_MONITOR_DRY_RUN") == "1"
    already_sent = False
    if dry_run:
        success = True
        print("[DRY_RUN] 跳过飞书发送，仅生成卡片和快照")
    elif already_sent_today(date_str, chat_id) and os.environ.get("PRODUCT_MONITOR_FORCE_SEND") != "1":
        success = True
        already_sent = True
        print(f"[SKIP] {date_str} 产品仓库日报今天已发送过；跳过重复发送。如需强制重发，设置 PRODUCT_MONITOR_FORCE_SEND=1")
    else:
        success = send_card(card, chat_id)
        if success:
            mark_sent(date_str, chat_id)

    save_snapshot(date_str, products_data, competitors_data)

    total_stars = sum(p.get("stars", 0) for p in products_data if p.get("has_repo"))
    if dry_run:
        send_status = "未发送（dry-run）"
    elif already_sent:
        send_status = "已跳过（今日已发送）"
    else:
        send_status = "成功" if success else "失败"
    print(f"产品仓库日报: {len(PRODUCTS)}个产品, {with_repo}有仓, 总⭐{total_stars}, 发送{send_status}")
    if product_diffs:
        print(f"产品变更: {len(product_diffs)}项")
    if extra_repos:
        print(f"额外仓库: {len(extra_repos)}个")


if __name__ == "__main__":
    main()
