# 产品清单（2026-07-01）

来源：Bitable `[REDACTED_BASE_TOKEN]` 项目总览表，25 个产品。此文件由 Bitable 重建，GitHub 默认分支/归档状态经 `gh api /repos/503496348-ops/<repo>` 实查。

统计：✅ 活跃 23｜⏸️ 已暂停 0｜🔒 已归档 2

| # | 产品名 | 英文代号 | GitHub 仓库 | 分类 | 默认分支 | 状态 |
|---|--------|---------|------------|------|---------|------|
| 1 | 裂变创作 | Fission Creative | fission-creative | 长文创作 | main | ✅ |
| 2 | 别样觉醒 | Awake Differently | awake-differently | 身份蒸馏 | main | ✅ |
| 3 | 白龙马医生 | Bailongma Doctor | hermes-doctor | 智能体健康 | main | ✅ |
| 4 | 皮皮虾医生 PipiXia Doctor | PipiXia Doctor | pipixia-doctor | 智能体健康 | main | ✅ |
| 5 | 深度方略 | Stratapro | stratapro | 量化投资 | main | ✅ |
| 6 | 灵感象限 | Ideasphere | ideasphere | 视频剪辑 | main | ✅ |
| 7 | 有点东西 | Nichecraft | nichecraft | 飞书白板设计+PPT | main | ✅ |
| 8 | 破窗造视 Fractovision | Fractovision | fractovision | 多媒体生成 | main | ✅ |
| 9 | 荒原序列 BarrenOrder | BarrenOrder | barren-order | 多Agent协作 | main | ✅ |
| 10 | 艺游未境 | Wanderix | canvas-design | 视觉创作 | main | ✅ |
| 11 | 奇点造物 | Genesisix | hermes-security-suite | 安全检测 | main | ✅ |
| 12 | 艺术生花 | Aestheflow | aestheflow | 内容分析 | main | 🔒 已归档 |
| 13 | 松弛有度 | EasyRhythm | easyrhythm | 智能客服 | main | ✅ |
| 14 | 他山之石 | HerPeakGem | herpeakgem | 智能教育 | main | ✅ |
| 15 | 自然良品 | PurePicks | purepicks | 电商推荐 | main | ✅ |
| 16 | 元气方程 | Energsolve | energsolve | 竞品分析 | main | ✅ |
| 17 | 召物少年 | Summoner | summoner | 漫画生成 | main | ✅ |
| 18 | 此地无垠 | Icilllimite | football-predictor | 体育分析 | main | ✅ |
| 19 | 绿茵智脑 | WorldCup Predictor | worldcup-predictor | 体育分析 | main | ✅ |
| 20 | 意识浓缩 | minddistill | minddistill | 内容分析 | main | ✅ |
| 21 | 智脑星河 | MindRiver | mindriver | 智能体运维 | main | ✅ |
| 22 | AtomGuard | atomguard | atomguard | 安全检测 | main | 🔒 已归档 |
| 23 | 妙笔生花 | ArtiPen | artipen | 内容创作 | main | ✅ |
| 24 | 无限循环 | Neverend | neverend | 知识管理 | main | ✅ |
| 25 | 暴躁因子 | blastogene | blastogene | 智能体运维 | main | ✅ |

## 额外仓库（非产品，不计入日报统计）

| 仓库 | 说明 |
|------|------|
| hermes-agent | 工坊基础设施 |
| dag-workflow-engine | 基础设施 |
| genesisix | 已归档，被 hermes-security-suite 替代 |
| genesisix-hermes | 已归档，被 hermes-security-suite 替代 |
| hermes-skill-gpt-image-gen | 已归档，被 canvas-design 替代 |
| Wanderix | 已归档，被 canvas-design 替代 |
| atomcollide-tianlai | Bitable 当前未列为产品，历史归档仓库 |
| lusi-hermes-config | 配置仓库（自动排除） |
| openclaw-hejunzongda | 配置仓库（自动排除） |
| yifei-hermes-config | 配置仓库（自动排除） |

## 更新记录

- 2026-07-15: 方案A临时执行：将 `艺术生花/Aestheflow` 标注为 `🔒 已归档`（保持产品清单行数不变），用于隔离单点缺仓噪音。
- 2026-07-02: ClaudeTeam 桥接能力二次融合：荒原序列 BarrenOrder 新增 Agent Team Bridge Runtime（manager inbox、worker pane、稳定 drop reason、Codex device-auth 恢复计划）；智脑星河 MindRiver 新增 Agent Fleet Ops Panel（语义健康、事件流停摆、登录恢复、上下文完整性）。
- 2026-07-02: 完成 ClaudeTeam 类研究/协作能力拆分融合：元气方程 Energsolve 新增公司研究双层 memo 与双信源验证矩阵；荒原序列 BarrenOrder 新增会前人物情报四线 manager-only 任务流；深度方略 Stratapro 新增带时间戳与原句证据的播客投资信号层。三仓均已测试、提交、推送并远端 SHA 对齐。
- 2026-07-02: 完成 GordenSuperPPTSkills 反向融合落地：有点东西新增可编辑 PPTX 四层资产契约；破窗造视新增幻灯片图片提示词包；艺游未境新增商业信息图密度评估；妙笔生花新增演示稿内容加厚；裂变创作新增长文到演示节奏规划；召物少年新增漫画页分层布局；荒原序列新增阶段证据 manifest；智脑星河新增交付证据账本。8 仓均已测试、提交、推送并远端 SHA 对齐。
- 2026-07-02: 无限循环 Neverend 升级至 v1.3.0，新增 Markdown/Obsidian Vault 索引、双链健康检查、断链/孤儿笔记检测与 SQLite/JSON/Markdown 报告；远端 main 已推送并从零 clone 复验，产品审计分数 8.2/10（A）。荒原序列 BarrenOrder 升级至 v1.3.0，新增常驻团队命令面与 manager-only 路由契约；智脑星河 MindRiver 升级至 v1.3.0，新增运行时可观测包。
- 2026-07-02: 荒原序列 BarrenOrder 升级至 v1.2.0；新增运行时路由状态机、intent锚定审批状态机、团队经验池、健康验证与 8 项单元测试，已从零 clone 复验。
- 2026-07-01: 第一批竞品能力融合完成并同步 Bitable：Genesisix v2.4.0、Fission Creative v8.1.0、Fractovision v1.4.0、ArtiPen v1.2.0、MindRiver v1.2.0、Neverend v1.2.0；新增第二批融合排期 `references/second-batch-fusion-plan-2026-07-01.md`。
- 2026-07-01: 按 Bitable 全量重建产品清单；同步第25项为暴躁因子-Blastogene；补充 GitHub 默认分支/归档状态实查；旧 AtomCollide Tianlai 移入额外仓库。
- 2026-06-24: 新增无限循环(Neverend/neverend)，24产品。知识管理分类。
- 2026-06-23: 新增AtomGuard(已归档)+妙笔生花(ArtiPen)，23产品。新增默认分支列+状态列。
- 2026-06-22: 新增意识浓缩(minddistill)+智脑星河(mindriver)，21产品。
- 2026-06-22: 新增绿茵智脑-世界杯版(worldcup-predictor)，19产品。
- 2026-06-21: 艺游未境更名(Wanderix)，新增绿茵智脑(Football Predictor)，18产品。
- 2026-06-19: 初始版本，16 产品对齐 Bitable。

|| 22a | GEO诊断映射补位 | GEO Map (临时) | minddistill | GEO诊断 | main | 映射补充 |
|| 22b | 智能体上下文映射补位A | Memory+Context | hermes-doctor | 智能体上下文 | main | 映射补充 |
|| 22c | 智能体上下文映射补位B | Memory+Context | pipixia-doctor | 智能体上下文 | main | 映射补充 |
