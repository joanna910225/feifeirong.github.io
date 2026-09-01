---
title: ComfyUI Node Maintainer
lang: zh
role: 创建者 / 维护者
period: "2026.04 - 至今"
stack: [GitHub Apps, GitHub Actions, ComfyUI, AI Agents]
summary: 一个面向 ComfyUI Custom Node 的开源 AI Maintainer，持续发现上游兼容性风险，规划并验证适配，整理 Issue，并提交附带验证证据的 Draft PR。
order: 3.5
currentEmployer: false
status: in-progress
url: https://github.com/joanna910225/comfyui-node-maintainer
---
## 我在做什么

- 用 GitHub 原生流程完成接入：安装 App、选择仓库、接受 Setup PR，并把 Creator 的 AI Key 留在 GitHub Actions Secrets 中。
- 建立完整的维护闭环：比较上游版本、复现失败、生成受限范围内的补丁、无 Secret 测试，再提交带兼容性证据的 Draft PR。
- 明确无测试仓库、GPU 任务和私有环境的能力边界，区分 verified 与 unverified 结果。

第一个里程碑会先在 ComfyUI Housekeeper 上 dogfooding，验证闭环后再接入外部 Custom Node Creator。
