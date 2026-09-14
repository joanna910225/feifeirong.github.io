---
title: "GPT-Live-1：让语音 Agent 处理停顿和插话"
date: 2026-09-14
lang: zh
category: Engineering
tags: [openai, voice-agent, realtime, api, full-duplex]
description: "GPT-Live-1 如何在同一个模型中处理听说、停顿和插话，并把复杂任务交给后端模型。"
translationKey: gpt-live-1-full-duplex-voice
draft: false
---

[原文：Build more natural voice experiences with GPT‑Live‑1 in the API](https://openai.com/index/introducing-gpt-live-1-in-the-api/)

现在的语音助手，声音已经挺自然了，但停顿和插话仍然处理得不好。用户稍微停一下，它可能抢话；用户想插一句，它又不一定停。

GPT-Live-1 主要解决这些问题。它把**输入和输出音频放在同一个模型里处理**，并允许开发者把复杂推理和工具调用交给后端模型。

## 架构

常见的语音 Agent 分成三段：

```text
语音识别 STT → 文本模型 LLM → 语音合成 TTS
```

模块之间的交接会增加延迟。遇到停顿、插话或改口，系统还要判断用户是否已经说完，对话很容易卡住。

GPT-Live-1 把语音处理放在一个模型里：

```text
GPT-Live-1：实时听 + 实时说 + 管理轮次与中断
                    ↓
        后端模型：深度推理 + 工具调用 + 执行动作
```

GPT-Live-1 负责听、说、轮次和中断。后端模型负责检索、推理、编码或操作业务系统。复杂任务可以交给 GPT-6 Astra、其他文本模型或第三方模型。

这样可以**分别控制语音延迟、后端能力和成本**。语音模型不需要同时承担所有推理任务。

## 停顿、插话和沉默

GPT-Live-1 同时处理输入和输出音频。用户可以停顿、插话、改口、笑或简单附和，不必等 Agent 说完。系统也可以在短暂停顿时继续等待，不必马上抢话或播报后台处理过程。

产品可以设置**什么时候回应、什么时候等待、什么时候只做简短确认**。语言学习、访谈和医疗预约都需要处理好这些时机，不能只看音质是否自然。

GPT-Live-1 仍然支持显式轮次。它原生支持 turn detection，提供 ASR 转录文本和回复文本，也支持字母数字识别与 keyword biasing。

开发者可以通过 system prompt 调整语气、语速和对话风格。GPT-Live-1 也增加了不同口音、方言和语言的声音选项。定制声音需要联系 OpenAI 销售，并满足相应资格和申请流程。

OpenAI 还提到长会话和电话支持，包括长时间交互中的上下文保持，以及预约、订单和客户支持等电话工作流。这些能力还需要放进实际环境测试。

## 发布材料里的测试数据

- 根据 [OpenAI 公布的测试](https://openai.com/index/introducing-gpt-live-1-in-the-api/)，GPT-Live-1 在 Full Duplex Bench 上比 GPT-Realtime-2.1 提升 **30 个百分点**，主要改善轮次延迟和互动行为。
- 与 GPT-6 Astra（medium reasoning）组合时，它在端到端语音 Agent 任务基准 Tau3 上**排名第一**。
- Speak 的早期测试显示，相比此前的轮次制系统，语言学习者思考时被打断的情况减少接近 **80%**。
- 一家医疗语音产品团队称，从级联语音架构迁移后，代码量减少约 **80%**，删去了约 **2.3 万行代码**。

这些数字来自 OpenAI 及其客户，我没有独立验证，暂时不能直接当成实际产品效果。

## 成本

GPT-Live-1 已经在 API 中开放。[官方定价](https://openai.com/index/introducing-gpt-live-1-in-the-api/)是前端语音层 **0.05 美元 / 分钟**，连续使用一小时约 **3 美元**。

实际产品还需要后端模型和 Agent harness。后端使用什么模型、调用多少次，也会产生费用。评估成本时，需要计算一次完整任务的花费，不能只看语音价格。
