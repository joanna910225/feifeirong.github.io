---
title: Codex Handoff Skill
lang: en
role: Creator / Maintainer
period: "2026.08 - present"
stack: [Codex, Multi-Agent Workflows, Markdown, Shell]
summary: "An open-source Codex skill for context-health checks, cost-aware model and subagent routing, and evidence-preserving rotation across long AI coding sessions."
order: 4
currentEmployer: false
status: active
url: https://github.com/joanna910225/codex-handoff-skill
---
## What I built and maintain

- Automatic `CONTINUE`, `CHECKPOINT`, or `ROTATE` decisions when context pressure, phase changes, repeated work, or model mismatch appear.
- Cost-aware routing that keeps consequential decisions with the main agent and delegates bounded work to an appropriate subagent and model.
- Compact handoffs that preserve completed work, changed files, test results, decisions, risks, and exactly one next step.
- A public installer that backs up existing configuration, preserves `AGENTS.md`, and installs the skill plus a read-only reviewer profile.

The goal is not more orchestration for its own sake. It is to keep long-running AI development understandable, reviewable, economical, and easy to resume.
