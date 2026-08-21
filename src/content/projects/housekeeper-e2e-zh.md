---
title: ComfyUI Housekeeper 前端自动化测试
lang: zh
role: Solo
period: "2026.08"
stack: [Playwright, TypeScript, Google Chrome, GitHub Actions]
summary: 为重度依赖前端 UI、canvas、鼠标拖拽与节点选择的 ComfyUI Housekeeper 扩展建立可重复的 Chrome E2E 测试体系。
order: 3
currentEmployer: false
status: active
---
## 我做了什么

- 建立浏览器测试体系，覆盖面板交互、节点选择 / 拖拽 / 排列、保存重载、快捷键重绑定与 subgraph，同时配套 Node 单元测试。
- 使用真实鼠标事件驱动操作：动态读取 DOM / LiteGraph 几何，不写死屏幕坐标。
- 建立 CI 矩阵：legacy canvas 作为 gating 路径，Nodes 2.0 / Vue 作为 nightly 兼容性信号。
