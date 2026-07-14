#!/usr/bin/env python3
"""
OPS 产品监控统一编排器 v1

设计原则：
- 串联产品日报、竞品监控、质量审计、cron健康检查
- 输出统一 JSON + 人类可读摘要
- 失败时生成诊断报告，不盲目重试
- 所有数字来自脚本原始输出，禁止 LLM 改写
"""

import json
import subprocess
import sys
import os
from datetime import datetime
from pathlib import Path
from typing import Any

SKILL_DIR = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = SKILL_DIR / "scripts"
REFERENCES_DIR = SKILL_DIR / "references"

# 脚本路径
PRODUCT_CARD_SCRIPT = SCRIPTS_DIR / "product-repo-card.py"
COMPETITOR_MONITOR_SCRIPT = SCRIPTS_DIR / "competitor-monitor.py"
AUDIT_PRODUCTS_SCRIPT = SCRIPTS_DIR / "audit-products.py"

# 输出路径
ORCHESTRATOR_OUTPUT = REFERENCES_DIR / "orchestrator-run-result.json"
SUMMARY_OUTPUT = REFERENCES_DIR / "orchestrator-summary.md"


class StepResult:
    """单步骤执行结果"""
    def __init__(self, name: str, success: bool, output: str = "", 
                 duration_seconds: float = 0, error: str = ""):
        self.name = name
        self.success = success
        self.output = output
        self.duration_seconds = duration_seconds
        self.error = error
        self.timestamp = datetime.now().isoformat()
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "success": self.success,
            "output_lines": len(self.output.split("\n")) if self.output else 0,
            "duration_seconds": round(self.duration_seconds, 2),
            "error": self.error[:500] if self.error else "",
            "timestamp": self.timestamp,
        }


def run_step(name: str, command: list[str], timeout: int = 300) -> StepResult:
    """执行单个步骤"""
    print(f"\n{'='*60}")
    print(f"▶ 执行: {name}")
    print(f"  命令: {' '.join(command[:3])}...")
    
    start_time = datetime.now()
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(SKILL_DIR)
        )
        duration = (datetime.now() - start_time).total_seconds()
        
        if result.returncode == 0:
            print(f"  ✅ 成功 ({duration:.1f}s)")
            # 输出摘要（前5行）
            output_lines = result.stdout.strip().split("\n")
            for line in output_lines[:5]:
                print(f"     {line}")
            if len(output_lines) > 5:
                print(f"     ... (共 {len(output_lines)} 行)")
            return StepResult(name, True, result.stdout, duration)
        else:
            print(f"  ❌ 失败 (exit code: {result.returncode})")
            print(f"     错误: {result.stderr[:200]}")
            return StepResult(name, False, result.stdout, duration, result.stderr)
            
    except subprocess.TimeoutExpired:
        duration = (datetime.now() - start_time).total_seconds()
        print(f"  ⏰ 超时 ({timeout}s)")
        return StepResult(name, False, "", duration, f"Timeout after {timeout}s")
    except Exception as e:
        duration = (datetime.now() - start_time).total_seconds()
        print(f"  💥 异常: {e}")
        return StepResult(name, False, "", duration, str(e))


def generate_summary(results: list[StepResult]) -> str:
    """生成人类可读摘要"""
    lines = [
        "# OPS 产品监控编排报告",
        f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "## 执行结果",
        ""
    ]
    
    total = len(results)
    success = sum(1 for r in results if r.success)
    failed = total - success
    
    lines.append(f"总计: {total} 步骤 | 成功: {success} | 失败: {failed}")
    lines.append("")
    
    for r in results:
        status = "✅" if r.success else "❌"
        lines.append(f"{status} **{r.name}** ({r.duration_seconds}s)")
        if r.error:
            lines.append(f"   错误: {r.error[:200]}")
        lines.append("")
    
    # 关键指标提取
    lines.extend([
        "## 关键指标",
        ""
    ])
    
    for r in results:
        if r.success and r.output:
            # 从输出中提取关键数字
            for line in r.output.split("\n"):
                if any(keyword in line for keyword in ["个产品", "个分类", "成功检查", "总⭐", "评分"]):
                    lines.append(f"- {r.name}: {line.strip()}")
    
    return "\n".join(lines)


def main():
    """主编排流程"""
    print("🚀 OPS 产品监控统一编排器 v1")
    print(f"   时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"   工作目录: {SKILL_DIR}")
    
    # 检查 --dry-run 参数
    dry_run = "--dry-run" in sys.argv
    
    if dry_run:
        print("\n⚠️  DRY_RUN 模式：仅执行只读步骤，跳过发送操作")
    
    results: list[StepResult] = []
    
    # Step 1: 产品日报（dry-run 模式）
    if PRODUCT_CARD_SCRIPT.exists():
        cmd = ["python3", str(PRODUCT_CARD_SCRIPT)]
        if dry_run:
            cmd.append("--dry-run")
        results.append(run_step("产品仓库日报", cmd))
    else:
        results.append(StepResult("产品仓库日报", False, error="脚本不存在"))
    
    # Step 2: 竞品监控日报
    if COMPETITOR_MONITOR_SCRIPT.exists():
        results.append(run_step("竞品仓库监控", [
            "python3", str(COMPETITOR_MONITOR_SCRIPT)
        ]))
    else:
        results.append(StepResult("竞品仓库监控", False, error="脚本不存在"))
    
    # Step 3: 产品质量审计（可选，耗时较长）
    if "--with-audit" in sys.argv and AUDIT_PRODUCTS_SCRIPT.exists():
        results.append(run_step("产品质量审计", [
            "python3", str(AUDIT_PRODUCTS_SCRIPT)
        ], timeout=600))
    
    # 生成汇总
    print(f"\n{'='*60}")
    print("📊 生成汇总报告...")
    
    summary = generate_summary(results)
    SUMMARY_OUTPUT.write_text(summary, encoding="utf-8")
    print(f"   摘要已保存: {SUMMARY_OUTPUT}")
    
    # 保存结构化结果
    run_result = {
        "schema_version": 1,
        "generated_at": datetime.now().isoformat(),
        "dry_run": dry_run,
        "total_steps": len(results),
        "success_count": sum(1 for r in results if r.success),
        "failure_count": sum(1 for r in results if not r.success),
        "steps": [r.to_dict() for r in results],
    }
    ORCHESTRATOR_OUTPUT.write_text(
        json.dumps(run_result, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    print(f"   JSON 已保存: {ORCHESTRATOR_OUTPUT}")
    
    # 最终状态
    print(f"\n{'='*60}")
    all_success = all(r.success for r in results)
    if all_success:
        print("✅ 全部步骤成功完成")
        return 0
    else:
        failed_names = [r.name for r in results if not r.success]
        print(f"❌ 存在失败步骤: {', '.join(failed_names)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
