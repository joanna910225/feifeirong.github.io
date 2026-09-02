---
title: Codex Handoff Skill
lang: zh
role: 创建者 / 维护者
period: "2026.08 - 至今"
stack: [Codex, Multi-Agent Workflow, Markdown, Shell]
summary: "一个开源的 Codex Skill：自动检查上下文健康度，按成本选择模型和 Subagent，并在长时间 AI Coding 中用可验证的 Handoff 安全轮换会话。"
order: 4
currentEmployer: false
status: active
url: https://github.com/joanna910225/codex-handoff-skill
---
## 我做了什么

- 在上下文压力、阶段切换、重复工作或模型不匹配时，自动判断 `CONTINUE`、`CHECKPOINT` 或 `ROTATE`。
- 把关键决策留给主 Agent，将边界清晰的任务交给成本与能力匹配的 Subagent 和模型。
- 用精简 Handoff 保留已完成工作、改动文件、测试结果、关键决定、风险和唯一下一步。
- 提供公开安装脚本：备份已有配置、保留 `AGENTS.md`，并安装 Skill 和只读 Reviewer。

目标不是为了编排而编排，而是让长时间的 AI 开发更容易理解、审查、控制成本和继续推进。
