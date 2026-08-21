---
title: ComfyUI Housekeeper — Frontend E2E Test Suite
lang: en
role: Solo
period: "2026.08"
stack: [Playwright, TypeScript, Google Chrome, GitHub Actions]
summary: A repeatable Chrome E2E test system for a ComfyUI Housekeeper extension whose behavior depends heavily on frontend UI, canvas geometry, node selection, and real mouse drag interactions.
order: 3
currentEmployer: false
status: active
---
## What I built

- A browser suite covering panel interaction, node selection / drag / layout, save and reload, shortcut rebinding, and subgraph flows, alongside Node unit tests.
- Real mouse-event-driven actions: read DOM / LiteGraph geometry dynamically rather than hard-coding screen coordinates.
- A CI matrix with a legacy canvas gating path and a Nodes 2.0 / Vue nightly compatibility signal.
