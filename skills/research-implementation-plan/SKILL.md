---
name: "research-implementation-plan"
description: "把已确认的科研方案和实验计划映射到真实代码仓库，生成可执行的 IMPLEMENTATION_PLAN.md。"
---

# 科研实现计划

计划阶段只读检查仓库，不修改科研源码、不部署、不运行 GPU 实验。读取 `FINAL_PROPOSAL.md`、`EXPERIMENT_PLAN.md`、阶段日志和授权，定位真实文件、函数、入口、数据加载、split、评分路径和已有实验脚本。

输出唯一的 `IMPLEMENTATION_PLAN.md`，逐项映射 H/Q/M/B/E、来源段落、输入处理输出接口、数据构造、命令、配置、预算、种子、资源、原始工件、推进条件和停止条件。找不到路径或发现计划与仓库不一致时报告阻塞，不虚构实现。
