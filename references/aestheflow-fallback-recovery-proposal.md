# Aestheflow 缺仓单点恢复/归档替代方案（最小落地版）

## 现状核验（本次已复核）
- `aestheflow` 在 `503496348-ops` 下 `git ls-remote` 与 GitHub API 均返回 `Repository not found`。
- 因此当前审计中保留 `F: 1`，为历史单点缺失问题。
- 该问题不会触发竞品日报或旧快照“诈尸”；仅影响产品日报/审计口径。

## 目标
把 `aestheflow` 的单点失败收敛为**可维护状态**，避免重复噪音，并给出可执行替代方案。

## 方案A（推荐，先落地）：短期归档冻结
1. 在产品治理层将 `艺术生花/aestheflow` 标记为已归档项（不再参与审计主闭环）。
2. 保留 25 行产品清单口径不动（避免上层 BI/Bitable 变更）。
3. 在 runbook/候选台账新增 `aestheflow` 为「治理外部缺失」标签。

**验收动作**
- 统一编排器 DRY_RUN：`python3 scripts/ops-product-monitor-orchestrator.py --with-audit --with-fusion-plan --dry-run`
- 预期：`产品仓库日报` 与 `产品质量审计` 都不再把该项列为新增失败（由脚本治理逻辑决定）；全局 `F` 不包含新噪音。

**回滚点**
- 回滚该归档标记；恢复 `aestheflow` 为活跃状态并保留该项复核。

**复测命令**
- `python3 scripts/product-repo-card.py --dry-run`
- `python3 scripts/audit-products.py`

---

## 方案B：映射补位替代（中期）
1. 若组织确定有同系替代（如内容分析平台），新增 `aestheflow` 映射补位行，主仓库口径不变。
2. 映射补位不参与新增仓库计数（保持历史“25 产品口径”与实际仓库数分离）。

**验收动作**
- 更新 product-list 映射补位清单并触发 DRY_RUN。

**回滚点**
- 删除映射补位行。

---

## 方案C：直接恢复仓库（恢复成本高）
1. 在 GitHub 组织内恢复/重建 `aestheflow` 仓库。
2. 补齐最小交付：README + SKILL.md + `scripts/doctor.py`。

**验收动作**
- 复跑：`python3 scripts/product-repo-card.py --dry-run && python3 scripts/audit-products.py`

**回滚点**
- 将仓库重新置为归档，不再参与审计。

## 建议
先执行方案A（可控、最少面影响），再根据业务侧确认决定是否在方案B或C扩展。