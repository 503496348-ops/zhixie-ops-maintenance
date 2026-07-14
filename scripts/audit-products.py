#!/usr/bin/env python3
"""
产品仓库质量审计脚本 v2
从 product-list.md 读取23款产品，逐个clone审计，输出评分报告。

修复v1 bug：只检查.py文件，漏掉了.ts/.tsx/.js等前端项目。
v2改为检查所有代码文件类型。
"""

import json
import os
import subprocess
import tempfile
import re
from pathlib import Path
from datetime import datetime


SKILL_DIR = Path(os.environ.get("ZHIXIE_OPS_SKILL_DIR", Path(__file__).resolve().parents[1]))
PRODUCT_LIST = SKILL_DIR / "references" / "product-list.md"
OUTPUT_FILE = SKILL_DIR / "references" / "audit-report.json"
GITHUB_ORG = "503496348-ops"

# 🔴 v2修复：必须包含所有代码文件类型，不能只检查.py
CODE_EXTS = {'.py', '.ts', '.tsx', '.js', '.jsx', '.go', '.rs', '.java',
             '.rb', '.swift', '.kt', '.c', '.cpp', '.h', '.vue', '.svelte'}
SKIP_DIRS = {'.git', 'node_modules', '__pycache__', '.next', 'dist', 'build', 'vendor', 'venv', '.venv'}


def load_products():
    """从 product-list.md 解析产品列表"""
    text = PRODUCT_LIST.read_text()
    products = []
    for line in text.split("\n"):
        line = line.strip()
        if not line.startswith("|") or line.startswith("|--") or line.startswith("| #"):
            continue
        cols = [c.strip() for c in line.split("|")]
        cols = [c for c in cols if c]
        if len(cols) >= 7:
            status = cols[6]
            # 跳过归档与映射补位（映射补位不计入正式日报/审计产品口径）
            if "映射补充" in status:
                continue
            if "归档" in status:
                continue
            products.append({
                "num": cols[0],
                "name": cols[1],
                "english": cols[2],
                "repo": cols[3],
                "category": cols[4],
                "branch": cols[5],
                "status": cols[6],
            })
    return products


def clone_repo(repo_name, branch, tmpdir):
    """克隆仓库"""
    url = f"https://github.com/{GITHUB_ORG}/{repo_name}.git"
    dest = os.path.join(tmpdir, repo_name)
    result = subprocess.run(
        ["git", "clone", "--depth", "1", "--branch", branch, url, dest],
        capture_output=True, text=True, timeout=60
    )
    if result.returncode != 0:
        result = subprocess.run(
            ["git", "clone", "--depth", "1", url, dest],
            capture_output=True, text=True, timeout=60
        )
    return dest if result.returncode == 0 else None


def audit_repo(repo_path, product):
    """审计单个仓库"""
    report = {
        "product": product["name"],
        "repo": product["repo"],
        "category": product["category"],
        "status": product["status"],
        "scores": {},
        "issues": [],
        "details": {},
    }

    if not repo_path or not os.path.exists(repo_path):
        report["issues"].append("❌ 仓库不存在或无法克隆")
        report["scores"]["total"] = 0
        return report

    # 1. SKILL.md 分析
    skill_md = os.path.join(repo_path, "SKILL.md")
    if os.path.exists(skill_md):
        content = Path(skill_md).read_text()

        has_triggers = "triggers:" in content or "trigger:" in content
        has_version = bool(re.search(r'^version:\s*["\']?v?\d', content, re.M))
        # 严格模式：检查章节标题，不靠散落关键词
        has_workflow = bool(re.search(r'^##\s+(工作流|Workflow|Steps|步骤|流程)', content, re.M))
        has_frontmatter = content.strip().startswith("---")
        has_technical = bool(re.search(r'^##\s+(技术架构|Technical|Architecture|算法|Pipeline)', content, re.M))
        has_line_numbers = bool(re.search(r'^\d+\|', content, re.M))
        has_generic_readme = bool(re.search(r'(Getting Started|Installation|Quick Start|Overview)', content, re.IGNORECASE))

        skill_score = 0
        if has_frontmatter and not has_line_numbers: skill_score += 2
        if has_line_numbers:
            report["issues"].append("🔴 SKILL.md有行号前缀污染（read_file写回导致）")
        if not has_version:
            report["issues"].append("⚠️ SKILL.md缺version字段")
        if has_triggers: skill_score += 3
        if has_workflow: skill_score += 3
        if has_technical: skill_score += 2
        if not has_generic_readme: skill_score += 2
        if has_generic_readme:
            report["issues"].append("⚠️ SKILL.md 看起来像README，不是真正的skill")

        report["scores"]["skill_md"] = min(skill_score, 10)
        report["details"]["skill_md"] = {
            "has_triggers": has_triggers,
            "has_workflow": has_workflow,
            "has_frontmatter": has_frontmatter,
            "has_technical": has_technical,
            "has_line_numbers": has_line_numbers,
            "has_version": has_version,
            "looks_like_readme": has_generic_readme,
            "length": len(content),
        }
    else:
        report["scores"]["skill_md"] = 0
        report["issues"].append("❌ 没有 SKILL.md")

    # 2. README.md 分析
    readme = os.path.join(repo_path, "README.md")
    if os.path.exists(readme):
        content = Path(readme).read_text()
        has_install = bool(re.search(r'(安装|install|pip|npm|docker)', content, re.IGNORECASE))
        has_usage = bool(re.search(r'(使用|usage|example|示例|quickstart)', content, re.IGNORECASE))

        readme_score = 0
        if has_install: readme_score += 3
        if has_usage: readme_score += 3
        if len(content) > 200: readme_score += 2
        if len(content) > 500: readme_score += 2

        report["scores"]["readme"] = min(readme_score, 10)
    else:
        report["scores"]["readme"] = 0
        report["issues"].append("⚠️ 没有 README.md")

    # 3. 代码质量 — v2: 检查所有代码文件类型
    code_files = []
    total_code_lines = 0
    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext in CODE_EXTS:
                fpath = os.path.join(root, f)
                try:
                    lines = len(Path(fpath).read_text(errors='ignore').split('\n'))
                    code_files.append({"file": f, "ext": ext, "lines": lines})
                    total_code_lines += lines
                except:
                    pass

    report["details"]["code"] = {
        "code_files": len(code_files),
        "total_lines": total_code_lines,
        "by_ext": {},
        "top_files": [],
    }

    # 按扩展名统计
    ext_counts = {}
    for cf in code_files:
        ext_counts[cf["ext"]] = ext_counts.get(cf["ext"], 0) + 1
    report["details"]["code"]["by_ext"] = ext_counts
    report["details"]["code"]["top_files"] = [
        f["file"] for f in sorted(code_files, key=lambda x: -x["lines"])[:5]
    ]

    code_score = 0
    if len(code_files) >= 10: code_score += 3
    elif len(code_files) >= 3: code_score += 1
    if total_code_lines >= 1000: code_score += 3
    elif total_code_lines >= 100: code_score += 1
    if total_code_lines >= 10000: code_score += 2

    has_real_code = any(cf["lines"] > 50 for cf in code_files)
    if has_real_code: code_score += 2

    report["scores"]["code"] = min(code_score, 10)

    if len(code_files) == 0:
        # 检查是否是skill-only产品（SKILL.md质量高但无代码）
        skill_quality = report["details"].get("skill_md", {}).get("length", 0)
        if skill_quality > 1500:
            report["issues"].append("⚠️ 无代码，但SKILL.md完整（skill即产品模式）")
        else:
            report["issues"].append("❌ 没有代码文件")
    if 0 < total_code_lines < 100:
        report["issues"].append("⚠️ 代码量不足100行")

    # 4. 技术特性检查
    all_text = ""
    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            if os.path.splitext(f)[1].lower() in CODE_EXTS | {'.md', '.yaml', '.yml', '.json'}:
                fpath = os.path.join(root, f)
                try:
                    all_text += Path(fpath).read_text(errors='ignore') + "\n"
                except:
                    pass

    unique_features = []
    checks = [
        ("API集成", r'(api|endpoint|request|response|fetch|axios|requests)'),
        ("数据处理", r'(pandas|numpy|dataframe|csv|json|parse)'),
        ("机器学习", r'(model|train|predict|inference|tensor|torch)'),
        ("Web框架", r'(flask|fastapi|django|express|http\.server)'),
        ("数据库", r'(sqlite|postgres|mysql|redis|mongo)'),
        ("文件处理", r'(read_file|write_file|open\(|Path\()'),
        ("CLI工具", r'(argparse|click|typer|sys\.argv|commander|yargs)'),
        ("测试", r'(test_|pytest|unittest|assert|describe\(|it\()'),
    ]

    for name, pattern in checks:
        if re.search(pattern, all_text, re.IGNORECASE):
            unique_features.append(name)

    report["details"]["features"] = unique_features
    tech_score = min(len(unique_features), 10)
    report["scores"]["tech"] = tech_score

    if len(unique_features) < 2:
        report["issues"].append("⚠️ 技术特性单薄，可能只是模型API包装")

    # 5. 拼凑感检查（仅检查SKILL.md和README，不扫代码——代码中的TODO/placeholder是正常开发惯例）
    doc_text = ""
    for doc_file in ["SKILL.md", "README.md"]:
        doc_path = os.path.join(repo_path, doc_file)
        if os.path.exists(doc_path):
            doc_text += Path(doc_path).read_text(errors='ignore') + "\n"
    template_indicators = [
        r'example\.com', r'your.api.key', r'REPLACE_ME', r'placeholder',
    ]
    template_count = sum(1 for p in template_indicators if re.search(p, doc_text, re.IGNORECASE))
    if template_count >= 3:
        report["issues"].append("🔴 拼凑感强：多处模板/占位符未替换")
        report["scores"]["template"] = max(0, 10 - template_count * 2)
    else:
        report["scores"]["template"] = 10

    # 总分
    weights = {"skill_md": 0.25, "readme": 0.10, "code": 0.25, "tech": 0.20, "template": 0.20}
    total = sum(report["scores"].get(k, 0) * w for k, w in weights.items())
    total = round(total, 1)
    report["scores"]["total"] = total

    if total >= 8: report["grade"] = "A"
    elif total >= 6: report["grade"] = "B"
    elif total >= 4: report["grade"] = "C"
    elif total >= 2: report["grade"] = "D"
    else: report["grade"] = "F"

    return report


def main():
    products = load_products()
    print(f"📋 加载 {len(products)} 个产品")
    print("=" * 60)

    results = []

    with tempfile.TemporaryDirectory() as tmpdir:
        for p in products:
            print(f"\n🔍 [{p['num']}] {p['name']} ({p['repo']})...")

            if "404" in p["status"] or "归档" in p["status"] or "映射补充" in p["status"]:
                print(f"  ⏭️ 跳过（{p['status']}）")
                results.append({
                    "product": p["name"], "repo": p["repo"],
                    "status": p["status"], "grade": "N/A",
                    "scores": {"total": 0},
                    "issues": [f"⏭️ 跳过：{p['status']}"],
                })
                continue

            repo_path = clone_repo(p["repo"], p["branch"], tmpdir)
            if not repo_path:
                print(f"  ❌ 克隆失败")
                results.append({
                    "product": p["name"], "repo": p["repo"],
                    "grade": "F", "scores": {"total": 0},
                    "issues": ["❌ 仓库克隆失败"],
                })
                continue

            report = audit_repo(repo_path, p)
            results.append(report)

            grade = report.get("grade", "?")
            total = report.get("scores", {}).get("total", 0)
            issues = report.get("issues", [])

            print(f"  📊 评分: {total}/10 ({grade})")
            for issue in issues[:3]:
                print(f"  {issue}")

    # 汇总
    print("\n" + "=" * 60)
    print("📊 审计汇总")
    print("=" * 60)

    grade_count = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0, "N/A": 0}
    for r in results:
        g = r.get("grade", "?")
        grade_count[g] = grade_count.get(g, 0) + 1

    for g in ["A", "B", "C", "D", "F", "N/A"]:
        if grade_count[g] > 0:
            print(f"  {g}: {grade_count[g]} 个")

    sorted_results = sorted(results, key=lambda x: x.get("scores", {}).get("total", 0))

    print("\n🔴 最差产品（需优先修复）:")
    for r in sorted_results[:5]:
        total = r.get("scores", {}).get("total", 0)
        grade = r.get("grade", "?")
        print(f"  {r['product']} ({r['repo']}): {total}/10 ({grade})")

    print("\n🟢 最佳产品:")
    for r in sorted_results[-3:]:
        total = r.get("scores", {}).get("total", 0)
        grade = r.get("grade", "?")
        print(f"  {r['product']} ({r['repo']}): {total}/10 ({grade})")

    OUTPUT_FILE.write_text(json.dumps({
        "audit_date": datetime.now().isoformat(),
        "total_products": len(results),
        "grade_distribution": grade_count,
        "results": results,
    }, ensure_ascii=False, indent=2))
    print(f"\n💾 完整报告已保存: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
