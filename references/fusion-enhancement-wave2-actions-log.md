# 融合增强 Wave-2 行动日志（续）

> 时间：2026-07-15 10:20 (延续 `wave1`)

## 已执行（本轮）

### 2) hermes-doctor（映射: `langgenius/dify`, `mem0ai/mem0`；缺口: Web框架 + 数据库）
- 目标：补齐 Web 接口能力，并提供可选持久化日志底座。
- 变更：
  - 新增 `scripts/api_server.py`
    - 提供 `FastAPI` 轻量服务（`/health`, `/diag`, `/diag/latest`, `/doctor/run`）
    - 与现有 `doctor.py` 复用检查逻辑
  - 新增 `scripts/history_store.py`
    - 基于 SQLite 的运行记录持久化：记录诊断 run 的时间戳、通过率、失败项、摘要
    - 查询最近记录接口
  - `scripts/doctor.py`
    - 增加 `collect_run_report()`（非侵入式抽取），用于 API 与命令行复用
  - `package.json`
    - 新增 `api` 启动脚本：`python3 scripts/api_server.py`
    - 增加可选依赖：`fastapi`, `uvicorn`
- 提交：`8316119`（repo: `503496348-ops/hermes-doctor`）
- 推送：成功（`main -> main`）

## 验证与回归
- 本地验收命令：
  - `PYTHONPATH=. pytest -q`（hermes-doctor）
  - 结果：13 passed
  - `python3 scripts/doctor.py` 结果：PASS
  - `python3 scripts/api_server.py --help` 可正常启动参数解析
- 运维仓库审计：`python3 scripts/audit-products.py`
  - 结果：`F: 1`（`aestheflow`，与本次增强无关）


### 3) pipixia-doctor（映射: `langgenius/dify`, `mem0ai/mem0`；缺口: Web框架）
- 目标：补齐 Web 接口能力，并提供可选的诊断运行持久化。
- 变更：
  - 新增 `scripts/pipixia_api.py`
    - 提供 `FastAPI` 轻量服务（`/health`, `/diag/run`, `/diag/latest`）
  - 新增 `scripts/pipixia_history_store.py`
    - 基于 SQLite 的运行记录持久化
  - `package.json`
    - 新增 `api` 启动脚本：`python3 scripts/pipixia_api.py`
    - 增加可选依赖：`fastapi`, `uvicorn`
    - 更新 `check:syntax` 为全量 `py_compile scripts/*.py`
- 提交：`f6a42e5`（repo: `503496348-ops/pipixia-doctor`）
- 推送：成功（`main -> main`）

## 验证与回归
- 本地验收命令：
  - `PYTHONPATH=. pytest -q`
  - 结果：13 passed
  - `python3 scripts/pipixia_api.py --help` 可正常输出帮助
- 运维仓库审计：`python3 scripts/audit-products.py`
  - 结果：`F: 1`（`aestheflow`，与本次增强无关）


### 4) barren-order（映射: crewAIInc/crewAI；缺口: 数据库）
- 目标：补齐数据库持久化底座（可选，非破坏性）并提供轻量诊断 API。
- 变更：
  - `scripts/doctor.py`
    - 新增 `collect_run_report()`，支持结构化检查结果输出。
    - `--format json` 时可输出可机读健康报告。
  - 新增 `scripts/barren_order_history_store.py`
    - SQLite 运行记录持久化（通过率、失败项、时间戳）
  - 新增 `scripts/barren_order_api.py`
    - 提供可选 `FastAPI` 服务（`/health`, `/diag`, `/diag/run`, `/diag/latest`）
  - `package.json`
    - 新增 `api` 脚本：`python3 scripts/barren_order_api.py`
    - 增加可选依赖 `fastapi`, `uvicorn`
    - 强化 `check:syntax` 覆盖 `scripts/*.py`
- 提交：`a940171`（repo: `503496348-ops/barren-order`）
- 推送：成功（`main -> main`）

- 本地验收：
  - `PYTHONPATH=. pytest -q`
  - 结果：35 passed
  - `python3 scripts/barren_order_api.py --help` 正常


### 5) nichecraft（映射: excalidraw/excalidraw；缺口: 数据库）
- 目标：补齐数据库持久化底座（可选，非破坏性）并提供轻量诊断 API。
- 变更：
  - `scripts/doctor.py`
    - 新增 `collect_run_report()`，支持结构化 JSON 健康报告。
  - 新增 `scripts/nichecraft_history_store.py`
    - SQLite 运行记录持久化（通过率、失败项、时间戳）
  - 新增 `scripts/nichecraft_api.py`
    - 提供可选 `FastAPI` 服务（`/health`, `/diag`, `/diag/run`, `/diag/latest`）
  - `package.json`
    - 新增 `api` 脚本：`python3 scripts/nichecraft_api.py`
    - 增加可选依赖 `fastapi`, `uvicorn`
    - 强化 `check:syntax` 覆盖 `scripts/*.py`
- 提交：`98b322d`（repo: `503496348-ops/nichecraft`）
- 推送：成功（`main -> main`）

- 本地验收：
  - `PYTHONPATH=. pytest -q`
  - 结果：19 passed
  - `python3 scripts/nichecraft_api.py --help` 正常


### 6) ideasphere（映射: huggingface/diffusers；缺口: Web框架, 数据库）
- 目标：补齐 Web + 数据库持久化能力（可选，非侵入式），形成诊断 API 与 SQLite 运行记录。
- 变更：
  - `scripts/doctor.py`
    - 新增 `collect_run_report()`，支持结构化 JSON 健康报告。
  - 新增 `scripts/ideasphere_history_store.py`
    - SQLite 运行记录持久化（通过率、失败项、时间戳）
  - 新增 `scripts/ideasphere_api.py`
    - 提供可选 `FastAPI` 服务（`/health`, `/diag`, `/diag/run`, `/diag/latest`）
  - `package.json`
    - 新增 `api` 脚本：`python3 scripts/ideasphere_api.py`
    - 增加可选依赖 `fastapi`, `uvicorn`
    - 强化 `check:syntax` 覆盖 `scripts/*.py`
- 提交：`b3fe3aa`（repo: `503496348-ops/ideasphere`）
- 推送：成功（`main -> main`）

- 本地验收：
  - `PYTHONPATH=. pytest -q`
  - 结果：5 passed
  - `python3 scripts/ideasphere_api.py --help` 正常


## 未执行（保留）
- 其余候选项进入下一波次：
  - `hermes-security-suite`（NVIDIA/SkillSpector，需先 commit 语义回放）
  - `fission-creative`（assafelovic/gpt-researcher）
  - `minddistill`（huggingface/transformers）
