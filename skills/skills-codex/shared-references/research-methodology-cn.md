# ARIS Codex 科研方法协议（中文定制版）

本协议是 `skills/skills-codex/` 各阶段共同遵守的研究语义层。它把用户的 Notion 科研方法嵌入 ARIS 的既有编排、Reviewer、Pilot、Research Wiki 和实验队列；各 Skill 负责在自己的实际阶段落实，不能只把本协议作为说明文字。

## 1. 证据与知识边界

- 用户 Notion 三类库（文献库、Idea 与验证库、研究认知与经验库）是长期科研知识来源。`/notion-research` 负责读取和按用户要求写回，不擅自改变 Notion schema。
- Research Wiki 是 ARIS/Codex 运行过程的持久化状态、缓存、图谱和查询包，记录论文节点、Idea、Pilot/实验结果和依赖关系。它服务于当前工作流，不能替代用户 Notion 的长期知识库。
- 每项关键判断标记来源：`论文明确内容`、`跨论文归纳` 或 `本文推导`。推导不得伪装成论文结论；实验结果不得直接升级为形式证明。

## 2. 两轮文献协议

每个研究方向必须执行两轮，每轮都包含 `收集 → 精读 → 五集合 → 跨论文归纳`：

1. 第一轮建立领域地图，覆盖代表性方法、共性问题和候选线索。
2. 从第一轮的共性问题和 P0–P4 线索中选择第二轮问题。
3. 第二轮围绕这些问题定向补充论文，分析最近工作解决了什么、依赖哪些机制条件、留下哪些限制。
4. 第二轮结果形成 `PROBLEM_EVIDENCE_PACK`，供 Idea 生成和精炼直接消费。发现相近工作时深入分析剩余空间，不因关键词相似自动否决方向。

每篇重点论文的五集合固定为：`解决的问题`、`作者 Intuition`、`核心方法`、`方法局限`、`潜在改进方向`。缺少字段时写明“未找到”，不得用猜测填充。

## 3. 线索优先级 P0–P4

P0：作者在 Limitation、Future Work、Discussion 或 Conclusion 中明确提出的局限、未解决问题或后续方向。优先定位原文，理解成立条件，并检查后续工作是否已经解决或部分缓解。

P1：实验直接暴露的问题，包括 failure case、negative result、性能边界、反常现象和有解释价值的消融结果。实验支持现象本身，不能把作者或当前模型对机制的解释直接当成事实。

P2：多个相关工作共同支持的归纳，例如相似 limitation、失败模式、机制约束或数据/反馈/资源瓶颈。必须列出共同论文、共同条件、重合范围和证据边界。

P3：根据方法的假设、可用信息、状态、更新规则、优化目标、反馈机制、数据流或决策链推导出的潜在机制性 limitation。这是研究者自己的推导，需要通过定向检索、Pilot 或正式实验检验。

P4：探索性构想，包括类比、跨领域或结构性迁移、新问题定义、新评测视角和探索性机制构想。初始证据通常较弱，需要补足问题依据、机制解释和验证路径。

P0–P4 表示研究线索的优先追踪顺序，不表示正确概率、Idea 分数、novelty 分数，也不是自动淘汰标准。存在合适 P0/P1 时优先围绕它建立研究主线，再通过五集合、跨论文分析和机制推导深化。作者提出问题不等于必须采用作者建议的解决方法。

失败 Idea 按 ARIS 原生规则进入 `failed ideas` banlist，避免下一轮重复生成；失败背景和 lesson 另行记录，不改变 banlist 语义。

## 4. Insight、Idea 与 H/Q/M/B/E

在写具体 Idea 前先生成 Insight Card：研究问题、证据出处、跨论文新认识、最强竞争解释、可区分预测、最小验证、最近相关工作、风险与适用条件。只有竞争解释能产生不同预测时，Insight 才进入候选池。

- **H（Hypothesis）**：可被证据支持或反驳的机制假设。
- **Q（Question）**：论文要回答的学术子问题。
- **M（Module）**：承载机制的最小方法组件；能删除、合并或复用时优先简化。
- **B（Build）**：可复现的代码、配置、数据或版本构建。
- **E（Experiment）**：回答一个 H/Q 的具体实验及其对照、预算和退出条件。

按语义需要使用这些标记，不为每个段落机械编号。主链必须能闭合：`证据 → 问题/Insight → H/Q → M → B/E → claim`。

## 5. Pilot 与正式实验

ARIS 原生路径保持为“多 Idea → Top 2–3 → Minimum Pilot → empirical reranking”。Pilot 的目标是用最低成本获得尽可能有诊断性的真实信号：默认 single seed、小数据、少 epoch、低 scale、约 30 分钟至 2 小时；若便宜的端到端 Pilot 已足以判断核心 Idea，直接使用，不强制拆模块。

只有在结果阴性/不确定且无法归因、Idea 是多阶段机制、存在便宜的中间信号，或主张本身是机制性主张时，才按需拆解 M/B/E。每个诊断 Pilot 记录：`目标 H/Q`、`被隔离的 M/B/E`、`输入与对照`、`观测指标`、`预期区分模式`、`预算/超时`、`failure attribution`、`verdict`。verdict 只能是 `strong_positive`、`weak_positive`、`clear_negative`、`inconclusive`，另记录 `pilot_skipped` 或 `needs_manual_pilot` 的原因。

`strong_positive` 可进入 refine/scale；`clear_negative` 进入 ARIS 原有失败 Idea 条件化 banlist；`weak_positive` 和 `inconclusive` 进入补充诊断或保守排序。失败记录模型、数据、预算和实现条件，不能形成脱离条件的科学永久否决。Pilot evidence 与 Formal Evaluation 分开，Pilot 不直接支持论文最终 claim。

## 6. 资源规则

单 GPU 是默认值，不是硬限制。如果模型单卡放不下、项目基线已使用多卡，或单卡不能在 time-to-signal 预算内给出有效信号且项目已有成熟启动方式，可使用 2/4/更多 GPU。只需支持项目已有的 GPU 列表/启动方式（例如 `CUDA_VISIBLE_DEVICES=0,1`），不引入新的调度器或资源优化系统。

## 7. 语义影响传播式修订

收到用户评论、Reviewer 反馈、新论文或实验结果后，先做 Impact Check：它改变了哪个研究判断？哪些 H/Q/M/B/E/claim 依赖它？哪些内容有独立证据可以保留？修改后 `证据 → 问题 → H/Q → M → E → claim` 是否仍闭合？

修订按语义依赖传播，不按文档位置机械重跑。措辞和局部实现细节可局部修改；研究判断变化要检查所有相关下游；结构性反馈才扩大范围。每轮完成 Revision Propagation & Consistency Check，并记录保留、重推和拒绝的 Reviewer 建议。ARIS 原有 Reviewer 循环、score 9 门槛和 AUTO_PROCEED 能力继续有效。
