---
title: ComfyUI Node Maintainer
lang: en
role: Creator / Maintainer
period: "2026.09 - present"
stack: [GitHub Apps, GitHub Actions, ComfyUI, AI Agents]
summary: An open-source AI maintainer for ComfyUI custom nodes that detects upstream compatibility risks, plans and tests adaptations, maintains issues, and opens evidence-backed draft pull requests.
order: 3.5
currentEmployer: false
status: in-progress
url: https://github.com/joanna910225/comfyui-node-maintainer
---
## What I am building

- A GitHub-native onboarding flow: install the app, select a repository, accept a setup PR, and keep the creator's AI key in GitHub Actions Secrets.
- A maintenance loop that compares upstream versions, reproduces failures, proposes a constrained patch, runs secretless tests, and opens a draft PR with compatibility evidence.
- Clear boundaries for repositories without tests or with GPU and private-environment requirements, including verified and unverified outcomes.

The first milestone is being dogfooded on ComfyUI Housekeeper before the platform expands to external custom-node creators.
