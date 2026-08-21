---
title: AI 短视频工作流平台
lang: zh
role: AI Platform / Backend Engineer
period: "2026.04 – 至今"
stack: [TypeScript, Node.js, Fastify, PostgreSQL, Vue 3, FFmpeg, 阿里云 FC/OSS]
summary: 面向批量短视频生产的 TypeScript 工作流平台，串联文案、语音、数字人、B-roll、字幕与成片交付；我负责付费节点的可靠性与可验证性工程。
order: 1
currentEmployer: true
---
## 我的工作方向

- 治理长耗时、易失败且会产生真实费用的视频操作：跨执行 checkpoint、任务复用，以及不确定结果下的 fail-closed 行为。
- 统一 HTTP 节点可靠性分层：超时策略、body-idle watchdog 与结构化上下文日志。
- 抽象本地 / 远端统一 FFmpeg runner，将媒体计算外置到函数计算与对象存储。
- 建立自包含依赖治理与验收门禁，包括 SHA 固定的 vendored registry、AST 网络门禁与 validate/check 工具链。
