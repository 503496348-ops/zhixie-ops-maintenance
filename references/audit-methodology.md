# 产品仓库质量审计方法论

## 何时触发审计
- 用户要求"排查/审计/检查产品质量"
- 新增产品后需要质量验收
- 竞品融合后需要回归验证
- 定期质量巡检（建议月度）

## 审计维度（5项，各10分）

### 1. SKILL.md 质量（权重25%）
- 有frontmatter(`---`开头): +2
- 有triggers字段: +3
- 有workflow/步骤/流程: +3
- 有技术细节(API/代码/脚本): +2
- 不是README风格(无Getting Started/Installation): +2

### 2. README.md 质量（权重10%）
- 有安装说明: +3
- 有使用说明/示例: +3
- 描述>200字: +2
- 描述>500字: +2

### 3. 代码质量（权重25%）
- 检查所有代码文件类型：.py .ts .tsx .js .jsx .go .rs .java .rb .swift .kt .c .cpp .h
- 代码文件≥10个: +3，≥3个: +1
- 代码行数≥1000: +3，≥100: +1
- 有>50行的实际逻辑文件: +2

### 4. 技术特性（权重20%）
检查10项技术特性，每项+1，上限10分。**必须根据仓库主要语言选择对应的检查规则**。

#### Python项目检查项

| 检查项 | 判定规则（正则） |
|--------|-----------------|
| API集成 | `api`, `endpoint`, `request`, `response`, `fetch`, `axios`, `requests` |
| 数据处理 | `pandas`, `numpy`, `dataframe`, `csv`, `json`, `parse` |
| 机器学习 | `model`, `train`, `predict`, `inference`, `tensor`, `torch`, `sklearn` |
| Web框架 | `flask`, `fastapi`, `django`, `express`, `http` |
| 数据库 | `sqlite`, `postgres`, `mysql`, `redis`, `mongo`, `sqlalchemy` |
| 文件处理 | `read_file`, `write_file`, `open(`, `Path(` |
| CLI工具 | `argparse`, `click`, `typer`, `sys.argv` |
| 测试 | `test_`, `pytest`, `unittest`, `assert` |
| 多Provider/引擎 | `provider`, `engine`, `backend`, `adapter`, `multi.?model` |
| 核心业务逻辑 | `def predict/analyze/generate/extract/detect/scan/crawl/recommend` |

#### TypeScript/JavaScript项目检查项

| 检查项 | 判定规则（正则） |
|--------|-----------------|
| LLM/AI集成 | `openai`, `anthropic`, `groq`, `huggingface`, `predict`, `chatCompletion`, `ai sdk` |
| 图片/媒体生成 | `sdxl`, `dall-e`, `replicate`, `stable.?diffusion`, `image.?gen`, `canvas`, `webgl` |
| 组件架构 | `component`, `useState`, `useEffect`, `props`, `jsx`, `tsx` |
| 状态管理 | `zustand`, `redux`, `useContext`, `store`, `pinia`, `vuex` |
| API路由 | `api/`, `route.`, `app.get`, `app.post`, `NextResponse`, `fetch(` |
| 类型系统 | `interface \w+`, `type \w+ =`, `: (string\|number\|boolean)` |
| 样式系统 | `tailwind`, `styled`, `css`, `sass`, `theme`, `className` |
| 测试 | `describe(`, `it(`, `test(`, `jest`, `vitest`, `cypress` |
| 构建配置 | `webpack`, `vite`, `next.config`, `tsconfig`, `package.json` |
| 多Provider/引擎 | `provider`, `engine`, `backend`, `fallback`, `adapter`, `multi` |

#### 语言判定规则
```python
is_frontend = ts_count > 0 or js_count > py_count
# is_frontend → 用TS/JS检查项
# not is_frontend → 用Python检查项
```

**分级**：≥7分=🟢独立技术产品，4-6分=🟡有技术深度，<4分=🔴技术单薄/可能只是包装

**用户反馈映射**（2026-06-23）：用户说"没有技术特性，跟使用的模型有关"——实际检查后5个被质疑产品全部≥6分。"拼凑感"来自SKILL.md格式不规范（缺frontmatter/triggers），不是代码质量问题。**修复SKILL.md格式即可消除拼凑感。**

### 5. 模板残留（权重20%）
检查hello.world/example.com/your.api.key/REPLACE_ME/TODO/FIXME/placeholder
命中≥3个=拼凑感强，扣分

## 等级划分
- A (≥8.0): 优秀
- B (6.0-7.9): 良好，需改进
- C (4.0-5.9): 及格，需较大改进
- D (2.0-3.9): 不及格
- F (<2.0): 严重问题

## 🔴 踩坑：必须检查所有代码文件类型

审计脚本不能只检查 `.py` 文件。召物少年(summoner)是TypeScript/React前端项目，
有139个.ts/.tsx文件共11,743行代码，但首次审计因只检查.py而被误判为"空壳"。

**铁律**：代码文件类型检查必须包含至少：
```python
code_exts = {'.py','.ts','.tsx','.js','.jsx','.go','.rs','.java','.rb','.swift','.kt','.c','.cpp','.h'}
```

## 🔴 踩坑：SKILL.md-only 仓库不等于空壳

智脑星河(mindriver)只有SKILL.md和README.md，没有代码。但SKILL.md本身是完整的
skill定义（有triggers、有技术细节、有版本号）。这类产品是"skill即产品"模式，
不能简单标记为"空壳"，需要单独评估SKILL.md的质量。

## 使用方式
```bash
# 运行审计脚本
python3 /root/.hermes/scripts/audit-products.py

# 报告保存位置
/root/.hermes/skills/product-repo-monitor/references/audit-report.json
```
