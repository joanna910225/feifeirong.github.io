---
title: "CS153 Lecture 2 — The Future of Voice Systems"
date: 2026-04-20
lang: en
category: CS153
tags: ["course", "stanford", "cs153", "audio", "voice", "agents", "text-to-speech", "dubbing"]
description: "How ElevenLabs grew from a text-to-speech wedge into a production stack for dubbing, localization, and real-time voice agents."
translationKey: cs153-lecture-2
draft: false
---

[Stanford CS153: Frontier Systems](https://cs153.stanford.edu/) · [Lecture recording](https://www.youtube.com/watch?v=TnL10oBZc6U)

*From AI dubbing to real-time voice agents*

> **Speaker**: Mati Staniszewski — CEO @ ElevenLabs
> **Date**: Spring 2026 · **Duration**: ~66m

---

## TL;DR

Mati Staniszewski explains how ElevenLabs went from a narrow text-to-speech wedge to a broader audio platform spanning dubbing, speech recognition, localization, and real-time voice agents. The core lesson is that frontier audio systems are not won by a single model alone, but by choosing the right system boundary, staying extremely close to users, and balancing emotional expressivity, latency, and reliability.

---

## Key Concepts

### The original problem: broken dubbing as a systems opportunity

Mati frames ElevenLabs around a very concrete user pain: foreign films dubbed into Polish often used a single flat narrator voice for every character. That made the company’s initial thesis unusually grounded. The future they imagined was not “better AI voice” in the abstract, but a world where any piece of content could be accessed in any language while preserving tone, performance, and emotional fidelity.

That starting point matters because it shaped the company as both a research lab and a product company from day one. The founding question was simultaneously:

1. Is the research frontier open enough to improve speech quality?
2. Is there a product pain severe enough that users will adopt it immediately?

### Audio dubbing is a stack, not a single model

Mati breaks speech localization into three model layers:

1. **Speech-to-text / transcription**
2. **Translation / language transformation**
3. **Text-to-speech / voice generation**

In theory, a full dubbing system needs all three. In practice, 2022-era models were too weak across the whole pipeline to deliver a strong end product. That forced ElevenLabs to make a classic frontier-systems decision: do not solve the entire stack at once if the full stack is too brittle.

Instead, they chose the narrowest high-value wedge: make text-to-speech dramatically more natural and emotionally expressive in English first. That reduced system complexity while still addressing many adjacent use cases such as voiceover fixes, script narration, audiobooks, and creator tooling.

### Why text-to-speech became the first wedge

The lecture highlights two limitations of earlier voice systems:

- they could not reliably preserve a speaker’s voice characteristics
- they could not read long passages with the right context, tone, pacing, or emotion

Mati’s argument is that natural speech is not just local token prediction. To read well, a model must use the context of the entire passage. A happy sentence should sound happy; dialogue should sound like dialogue; pacing should reflect structure and intent.

ElevenLabs’ early progress came from combining stronger sequence modeling with a more abstract representation of voice. Instead of hard-coding traits like age, accent, and gender, they let the model learn higher-level latent characteristics directly. This made the generated voice both more natural and more flexible.

### Product-led growth as a context feedback loop

A recurring theme from Lecture 1 returns here: context feedback loops. ElevenLabs began with a strongly product-led, creator-led motion. Discord communities, creators, and developers acted as an early sensor network for unexpected demand.

That loop changed the roadmap. Users initially confirmed interest in dubbing, but then revealed nearer-term pain points:

- patching mis-recorded lines
- generating voiceovers from scripts
- narrating articles and books
- preserving a creator’s own voice

So the research frontier stayed ambitious, but the product surface stayed tightly coupled to real-world workflows. The company’s early success came from minimizing the distance between user behavior and model iteration.

### The audio timeline: from TTS to agents

Mati sketches a useful chronology for the audio frontier:

- **2022**: better contextual text-to-speech
- **2023**: broader narration, multilingual voice use, user-created voices, voice marketplace
- **2024**: strong enough speech-to-text + translation + generation for AI dubbing/localization
- **2025**: real-time voice agents become viable
- **2026**: deeper blending of cascaded and fused architectures

The lecture uses concrete examples like Javier Milei speeches, Lex Fridman multilingual interviews, and broader localization workflows to show how each system layer matured before the full product stack became compelling.

### Cascaded vs fused voice architectures

One of the most valuable parts of the lecture is the architecture tradeoff for real-time agents.

**Cascaded approach**:
- speech-to-text
- language model
- text-to-speech

**Fused approach**:
- a more unified model that reasons directly over speech and response generation

Mati’s view is not ideological. He treats this as an engineering choice with different optimization targets:

- **Fused models** can win on latency
- **Cascaded systems** are currently better for enterprise reliability, tool use, observability, and guardrails

For business workflows like support, booking, payments, and authentication, reliability matters more than shaving every last millisecond. That is why ElevenLabs still favors cascaded systems for many production deployments, even while exploring more unified models in parallel.

### Emotionality is a data and control problem

A major capability gap in today’s audio agents is emotional understanding. Mati argues that much of this gap is not mysterious; it is a data-labeling and control problem.

If a user sounds angry, stressed, excited, or uncertain, the model should not merely transcribe words. It should pass those emotional signals into the reasoning layer and generate an appropriately matched reply. ElevenLabs’ recent work tries to infer that emotional metadata during transcription and feed it forward into the response pipeline.

The hard part was not only modeling but building the dataset and control interface:

- label enough speech for emotion and delivery
- make the model respond expressively
- make the expressivity controllable rather than random

This is a good example of frontier progress depending on annotation systems, preference collection, and product control surfaces, not just bigger models.

### Reliability, tool use, and enterprise deployment

For enterprise voice agents, the real benchmark is not “sounds human.” It is whether the system can complete multi-step workflows safely:

- authenticate users
- pull account information
- execute tool calls correctly
- maintain traceability across the pipeline

Mati repeatedly emphasizes that business customers care about intelligent behavior under operational constraints. A customer-support agent must not hallucinate a booking change or silently fail a payment flow. This is why he sees a long future for observable, partially modular systems even if unified approaches improve rapidly.

### Safety, licensing, and voice authentication

The lecture also covers the safety side of audio:

- tracing generated content back to the source
- stopping fraud or scam attempts before generation
- watermarking or AI-detection infrastructure
- supporting legitimate voice licensing

Mati’s most concrete security takeaway is that voice should not be treated as a robust authentication factor going forward. If high-quality voice cloning is cheap, then voice-based verification becomes structurally weak.

Interestingly, he also mentions the reverse use case: deploying voice agents against likely scammers to waste their time. That captures how the same infrastructure can be used for defense as well as attack.

---

## Industry Insights

- ElevenLabs started with founders drawing from savings and iterating very close to users before raising serious capital.
- Open source mattered early: Mati explicitly highlights Tortoise TTS as proof that frontier audio could emerge outside hyperscalers.
- Community distribution was not a side tactic; Discord and creator ecosystems were part of the research loop.
- Real-time voice agents are constrained by three moving targets at once: emotionality, reliability, and latency.
- Mati’s pricing rule is strikingly clear: price from user value, not from model cost; work backward from the value created.
- Over a 5-year horizon, he expects a small number of dominant “conversational platforms,” analogous to cloud platforms for compute.

---

## Memorable Moments

- The company originally tried running itself on Discord because the founders were “allergic to meetings” and wanted to redesign company communication from scratch.
- The origin story comes from the absurdity of Polish film dubbing with one monotone narrator reading every role.
- Mati describes a future where businesses interact with customers through voice agents the way they now interact through websites and apps.
- One charity used a voice agent to keep scammers occupied on the phone, effectively turning the system into an anti-scam time sink.

---

## Notable Quotes

> "You need to be extremely problem obsessed."

> "We decided that the first set of the biggest potential will be the more basic version."

> "Never start from the cost, start from the value and work backwards from there."

> "We think the cascaded approach is the right thing for the next few years."

> "Voice authentication... is the wrong approach."

---

## Reading Materials

### Official Readings

No formal reading appears to be assigned in the lecture itself.

### Unofficial / Supplementary

1. **Tortoise TTS** (James Betker)
   - Mentioned as an important early open-source milestone for high-quality text-to-speech.
2. **AI dubbing / localization case studies**
   - ElevenLabs’ examples around multilingual speeches and interviews are useful for understanding where the full stack became viable.
3. **Voice-agent architecture debates**
   - The cascaded-vs-fused tradeoff is the conceptual reading assignment embedded in the talk.

---

## Connections

- Part of [CS153: Frontier Systems](https://cs153.stanford.edu/) — Stanford, Spring 2026
- Builds directly on [Lecture 1 - Introduction to Frontier Systems](/feifeirong.github.io/blog/cs153-lecture-1-introduction-to-frontier-systems-en/) and its themes of context feedback loops, deployment context, and system bottlenecks.
- Connects forward to [Lecture 3 - Frontier Visual Intelligence Systems](/feifeirong.github.io/blog/cs153-lecture-3-frontier-visual-intelligence-systems-en/) by giving an audio-side version of the same frontier-lab playbook.
- Reinforces Lecture 1’s claim that the key bottlenecks are not only compute and capital, but also data, deployment structure, and culture.
