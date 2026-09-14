---
title: "GPT-Live-1: Handling Pauses and Interruptions in Voice Agents"
date: 2026-09-14
lang: en
category: Engineering
tags: [openai, voice-agent, realtime, api, full-duplex]
description: "How GPT-Live-1 handles speech, pauses, and interruptions in one model while delegating complex work to a backend model."
translationKey: gpt-live-1-full-duplex-voice
draft: false
---

[Source: Build more natural voice experiences with GPT‑Live‑1 in the API](https://openai.com/index/introducing-gpt-live-1-in-the-api/)

Voice assistants already sound fairly natural, but many still handle pauses and interruptions poorly. Pause briefly and they may jump in; interrupt them and they may not stop.

GPT-Live-1 is designed to address these problems. It **processes incoming and outgoing audio in one model** and lets developers delegate deeper reasoning and tool calls to a backend model.

## Architecture

A common voice-agent stack has three stages:

```text
Speech-to-text STT → language model LLM → text-to-speech TTS
```

Every handoff adds latency. When a user pauses, interrupts, or changes direction, the system must also decide whether the turn is over. That is where the conversation often breaks down.

GPT-Live-1 puts the voice layer into one model:

```text
GPT-Live-1: listens + speaks + manages turns and interruptions
                              ↓
             Backend model: deeper reasoning + tool calls + actions
```

GPT-Live-1 handles listening, speaking, turns, and interruptions. A backend model handles retrieval, reasoning, coding, or actions in business systems. Complex tasks can go to GPT-6 Astra, another text model, or a third-party model.

This setup lets developers **control voice latency, backend capability, and cost separately**. The voice model does not have to perform every reasoning task itself.

## Pauses, interruptions, and silence

GPT-Live-1 processes incoming and outgoing audio together. Users can pause, interrupt, correct themselves, laugh, or give a short acknowledgment without waiting for the agent to finish. The system can also wait through a short pause instead of jumping in or narrating every background step.

A product can define **when to reply, when to wait, and when to give only a brief acknowledgment**. Language learning, interviews, and medical scheduling all depend on this timing. Natural-sounding audio alone is not enough.

Explicit turn boundaries are still available. GPT-Live-1 supports turn detection, provides ASR transcripts and response text, and supports alphanumeric recognition and keyword biasing.

Developers can use the system prompt to control tone, pace, and conversational style. GPT-Live-1 also adds more voice options across accents, dialects, and languages. Custom voices require contacting OpenAI sales and going through the eligibility and request process.

OpenAI also lists better long-session reliability and telephony support, including reservation, order, and customer-support workflows. These capabilities still need to be tested in real deployment conditions.

## Metrics from the release materials

- According to [OpenAI's evaluations](https://openai.com/index/introducing-gpt-live-1-in-the-api/), GPT-Live-1 improves Full Duplex Bench performance by **30 percentage points** over GPT-Realtime-2.1, mainly in turn-taking latency and interactive behavior.
- Paired with GPT-6 Astra at medium reasoning effort, it **ranks first** on Tau3, an end-to-end voice-agent benchmark.
- In Speak's early evaluations, interruptions during learners' thinking pauses fell by almost **80%** compared with its previous turn-based systems.
- A medical voice-product team said that moving from a cascaded architecture reduced its codebase by about **80%** and removed roughly **23,000 lines of code**.

These numbers come from OpenAI and its customers. I have not independently verified them, so I do not treat them as proven product results.

## Cost

GPT-Live-1 is available in the API. The [front-end voice layer costs](https://openai.com/index/introducing-gpt-live-1-in-the-api/) **$0.05 per minute**, or about **$3 per hour** of continuous use.

A working product still needs a backend model and an agent harness. The backend model and the number of calls add to the bill. Cost estimates should cover a complete task, not just the per-minute voice price.
