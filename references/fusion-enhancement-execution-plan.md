# 产品融合增强执行清单
生成时间：2026-07-23T10:29:03.689831

## 来源
- 产品审计：`references/audit-report.json`
- 竞品候选池：`references/competitor-candidate-pool.json`（若本地无效则回退共享路径）

## 执行约束
- 不直接改供应商核心仓库口径，优先产出可验证增量
- 每项融合需给出 `代码入口 / 验收命令 / 回退点`
- 首轮只做能力增强准备，不做跨仓库自动重构

## 候选池（共 26 项）

### 1. EverMind-AI/Raven
- 分类：智能体上下文
- 映射产品：hermes-doctor, pipixia-doctor, mindriver
- 融合判定：可融合候选
- 评分：8（状态：implemented）
- 审计信号：total=9.1, tech=8
- 缺口特征：无明显缺口
- 执行证据：
  - EverMind-AI/Raven status=可融合候选 score=8
  - products=['hermes-doctor', 'pipixia-doctor', 'mindriver']

### 2. OpenCut-app/OpenCut
- 分类：视频剪辑
- 映射产品：ideasphere, fractovision
- 融合判定：可融合候选
- 评分：7（状态：implemented）
- 审计信号：total=9.1, tech=8
- 缺口特征：无明显缺口
- 执行证据：
  - OpenCut-app/OpenCut status=可融合候选 score=7
  - products=['ideasphere', 'fractovision']

### 3. code2rich/agentwaker-wechat-official-account-operator
- 分类：内容创作
- 映射产品：artipen
- 融合判定：可融合候选
- 评分：7（状态：recorded）
- 审计信号：total=9.1, tech=8
- 缺口特征：无明显缺口
- 执行证据：
  - code2rich/agentwaker-wechat-official-account-operator status=可融合候选 score=7
  - products=['artipen']

### 4. brightdata/competitive-intelligence
- 分类：竞品分析
- 映射产品：energsolve
- 融合判定：可融合候选
- 评分：6（状态：implemented）
- 审计信号：total=9.6, tech=8
- 缺口特征：无明显缺口
- 执行证据：
  - brightdata/competitive-intelligence status=可融合候选 score=6
  - products=['energsolve']

### 5. crewAIInc/crewAI
- 分类：多Agent协作
- 映射产品：barren-order
- 融合判定：可融合候选
- 评分：6（状态：pending_review）
- 审计信号：total=9.1, tech=8
- 缺口特征：无明显缺口
- 执行证据：
  - crewAIInc/crewAI status=可融合候选 score=6
  - products=['barren-order']

### 6. huggingface/diffusers
- 分类：视频剪辑
- 映射产品：ideasphere
- 融合判定：可融合候选
- 评分：6（状态：pending_review）
- 审计信号：total=9.1, tech=8
- 缺口特征：无明显缺口
- 执行证据：
  - huggingface/diffusers status=可融合候选 score=6
  - products=['ideasphere']

### 7. langgenius/dify
- 分类：智能体健康
- 映射产品：hermes-doctor, pipixia-doctor
- 融合判定：可融合候选
- 评分：6（状态：pending_review）
- 审计信号：total=9.1, tech=8
- 缺口特征：无明显缺口
- 执行证据：
  - langgenius/dify status=可融合候选 score=6
  - products=['hermes-doctor', 'pipixia-doctor']

### 8. excalidraw/excalidraw
- 分类：飞书白板设计+PPT
- 映射产品：nichecraft
- 融合判定：可融合候选
- 评分：6（状态：pending_review）
- 审计信号：total=8.8, tech=8
- 缺口特征：无明显缺口
- 执行证据：
  - excalidraw/excalidraw status=可融合候选 score=6
  - products=['nichecraft']

### 9. frontend-slides
- 分类：飞书白板设计+PPT
- 映射产品：nichecraft
- 融合判定：可融合候选
- 评分：6（状态：implemented）
- 审计信号：total=8.8, tech=8
- 缺口特征：无明显缺口
- 执行证据：
  - frontend-slides status=可融合候选 score=6
  - products=['nichecraft']

### 10. beautiful-feishu-whiteboard
- 分类：飞书白板设计+PPT
- 映射产品：nichecraft
- 融合判定：可融合候选
- 评分：5（状态：implemented）
- 审计信号：total=8.8, tech=8
- 缺口特征：无明显缺口
- 执行证据：
  - beautiful-feishu-whiteboard status=可融合候选 score=5
  - products=['nichecraft']

### 11. Nutlope/hallmark
- 分类：内容创作
- 映射产品：nichecraft, canvas-design, artipen
- 融合判定：可融合候选
- 评分：5（状态：implemented）
- 审计信号：total=8.8, tech=8
- 缺口特征：无明显缺口
- 执行证据：
  - Nutlope/hallmark status=可融合候选 score=5
  - products=['nichecraft', 'canvas-design', 'artipen']

### 12. scrapy/scrapy
- 分类：竞品分析
- 映射产品：energsolve
- 融合判定：可融合候选
- 评分：4（状态：pending_review）
- 审计信号：total=9.6, tech=8
- 缺口特征：无明显缺口
- 执行证据：
  - scrapy/scrapy status=可融合候选 score=4
  - products=['energsolve']

### 13. camel-ai/camel
- 分类：多Agent协作
- 映射产品：barren-order
- 融合判定：可融合候选
- 评分：4（状态：watching）
- 审计信号：total=9.1, tech=8
- 缺口特征：无明显缺口
- 执行证据：
  - camel-ai/camel status=可融合候选 score=4
  - products=['barren-order']

### 14. assafelovic/gpt-researcher
- 分类：长文创作
- 映射产品：fission-creative
- 融合判定：可融合候选
- 评分：4（状态：implemented）
- 审计信号：total=8.8, tech=8
- 缺口特征：无明显缺口
- 执行证据：
  - assafelovic/gpt-researcher status=可融合候选 score=4
  - products=['fission-creative']

### 15. huggingface/transformers
- 分类：内容分析
- 映射产品：minddistill, minddistill
- 融合判定：可融合候选
- 评分：4（状态：pending_review）
- 审计信号：total=8.3, tech=8
- 缺口特征：无明显缺口
- 执行证据：
  - huggingface/transformers status=可融合候选 score=4
  - products=['minddistill', 'minddistill']

### 16. feishu-base-custom-api
- 分类：知识管理
- 映射产品：neverend
- 融合判定：观察/人工复核
- 评分：2（状态：watching）
- 审计信号：total=8.7, tech=6
- 缺口特征：机器学习, Web框架
- 建议动作：
  - 补齐可复用 API/服务能力边界，先补充 HTTP 输入输出契约与异常码策略
  - 补齐模型推理链路/评分链路的最小闭环，并补充 smoke 测试
- 执行证据：
  - feishu-base-custom-api status=观察/人工复核 score=2
  - products=['neverend']

### 17. jokecamp/FootballData
- 分类：体育分析
- 映射产品：football-predictor, worldcup-predictor
- 融合判定：观察/人工复核
- 评分：2（状态：watching）
- 审计信号：total=8.7, tech=6
- 缺口特征：Web框架, 数据库
- 建议动作：
  - 补齐可复用 API/服务能力边界，先补充 HTTP 输入输出契约与异常码策略
  - 补齐持久化落库与迁移脚本（至少持久化关键指标与证据凭证）
- 执行证据：
  - jokecamp/FootballData status=观察/人工复核 score=2
  - products=['football-predictor', 'worldcup-predictor']

### 18. vrtmrz/obsidian-livesync
- 分类：知识管理
- 映射产品：neverend
- 融合判定：观察/人工复核
- 评分：1（状态：watching）
- 审计信号：total=8.7, tech=6
- 缺口特征：机器学习, Web框架
- 建议动作：
  - 补齐可复用 API/服务能力边界，先补充 HTTP 输入输出契约与异常码策略
  - 补齐模型推理链路/评分链路的最小闭环，并补充 smoke 测试
- 执行证据：
  - vrtmrz/obsidian-livesync status=观察/人工复核 score=1
  - products=['neverend']

### 19. black-forest-labs/flux
- 分类：多媒体生成
- 映射产品：fractovision
- 融合判定：观察/人工复核
- 评分：1（状态：watching）
- 审计信号：total=8.7, tech=6
- 缺口特征：Web框架, 数据库
- 建议动作：
  - 补齐可复用 API/服务能力边界，先补充 HTTP 输入输出契约与异常码策略
  - 补齐持久化落库与迁移脚本（至少持久化关键指标与证据凭证）
- 执行证据：
  - black-forest-labs/flux status=观察/人工复核 score=1
  - products=['fractovision']

### 20. Auriti-Labs/geo-optimizer-skill
- 分类：GEO诊断
- 映射产品：minddistill
- 融合判定：观察/人工复核
- 评分：1（状态：watching）
- 审计信号：total=8.3, tech=8
- 缺口特征：无明显缺口
- 执行证据：
  - Auriti-Labs/geo-optimizer-skill status=观察/人工复核 score=1
  - products=['minddistill']

### 21. AUTOMATIC1111/stable-diffusion-webui
- 分类：多媒体生成
- 映射产品：fractovision
- 融合判定：仅记录
- 评分：-5（状态：recorded）
- 审计信号：total=8.7, tech=6
- 缺口特征：Web框架, 数据库
- 建议动作：
  - 补齐可复用 API/服务能力边界，先补充 HTTP 输入输出契约与异常码策略
  - 补齐持久化落库与迁移脚本（至少持久化关键指标与证据凭证）
- 执行证据：
  - AUTOMATIC1111/stable-diffusion-webui status=仅记录 score=-5
  - products=['fractovision']

### 22. Comfy-Org/ComfyUI
- 分类：多媒体生成
- 映射产品：fractovision
- 融合判定：仅记录
- 评分：-5（状态：recorded）
- 审计信号：total=8.7, tech=6
- 缺口特征：Web框架, 数据库
- 建议动作：
  - 补齐可复用 API/服务能力边界，先补充 HTTP 输入输出契约与异常码策略
  - 补齐持久化落库与迁移脚本（至少持久化关键指标与证据凭证）
- 执行证据：
  - Comfy-Org/ComfyUI status=仅记录 score=-5
  - products=['fractovision']

### 23. linuxserver/docker-obsidian
- 分类：知识管理
- 映射产品：neverend
- 融合判定：仅记录
- 评分：-5（状态：recorded）
- 审计信号：total=8.7, tech=6
- 缺口特征：机器学习, Web框架
- 建议动作：
  - 补齐可复用 API/服务能力边界，先补充 HTTP 输入输出契约与异常码策略
  - 补齐模型推理链路/评分链路的最小闭环，并补充 smoke 测试
- 执行证据：
  - linuxserver/docker-obsidian status=仅记录 score=-5
  - products=['neverend']

### 24. aaron-he-zhu/seo-geo-claude-skills
- 分类：GEO诊断
- 映射产品：minddistill
- 融合判定：仅记录
- 评分：-5（状态：recorded）
- 审计信号：total=8.3, tech=8
- 缺口特征：无明显缺口
- 执行证据：
  - aaron-he-zhu/seo-geo-claude-skills status=仅记录 score=-5
  - products=['minddistill']

### 25. explosion/spaCy
- 分类：内容分析
- 映射产品：minddistill, minddistill
- 融合判定：仅记录
- 评分：-5（状态：recorded）
- 审计信号：total=8.3, tech=8
- 缺口特征：无明显缺口
- 执行证据：
  - explosion/spaCy status=仅记录 score=-5
  - products=['minddistill', 'minddistill']

### 26. zubair-trabzada/geo-seo-claude
- 分类：GEO诊断
- 映射产品：minddistill
- 融合判定：仅记录
- 评分：-5（状态：recorded）
- 审计信号：total=8.3, tech=8
- 缺口特征：无明显缺口
- 执行证据：
  - zubair-trabzada/geo-seo-claude status=仅记录 score=-5
  - products=['minddistill']

## 交付验收
1. 产出/更新本文件后，运行 `python3 scripts/audit-products.py`
2. 产出后对比 `total_products` 与 25 产品一致，`products_with_issues` 无历史污染项
3. 在 PR/候选动作中附上 `orchestrator` 汇总输出
