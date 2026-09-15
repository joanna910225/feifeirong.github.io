---
title: "Procedural Graphs: An Updatable Execution Map for Long-Horizon Agents"
date: 2026-09-15
lang: en
category: Engineering
tags: [ai-agents, agent-engineering, procedural-memory, llm]
description: "Procedural Graphs store steps, conditions, and common failure modes in a workflow that can guide long-horizon agents locally and improve through validation."
translationKey: procedural-graphs-long-horizon-agents
draft: false
---

Paper: [arXiv abstract](https://arxiv.org/abs/2609.09153) · [PDF](https://arxiv.org/pdf/2609.09153)

An agent can usually choose the next step in a short task from its immediate context. Over a longer run, that becomes much harder. The agent may lose track of the goal, skip a prerequisite check, call tools in the wrong order, or repeat the same failed actions.

Two common responses are to add memory or hard-code a workflow. Memory preserves experience, but the model still has to decide when and where each lesson applies. A fixed workflow makes the order explicit, but is expensive to maintain and difficult to improve automatically from execution data.

The paper proposes **Procedural Graphs (PGs)** as a middle layer. A PG stores what the agent can do next, when a transition applies, and which mistakes to avoid in a model-independent graph. At each step, the agent reads only the part of the graph near its current position. After a batch of tasks, a separate LLM can propose graph changes based on successful and failed trajectories, while a validation set decides whether those changes are accepted.

This places PGs between unconstrained ReAct and a hard-coded state machine: the graph provides explicit process guidance without forcing the solver to take a particular action.

## What the graph stores

A Procedural Graph contains nodes and directed edges:

- A node may represent a tool call, skill, reasoning step, or task state.
- An edge describes which step may follow another.
- Each edge carries `condition`, `guidance`, and `pitfalls` fields for applicability, execution advice, and common errors.

A search agent, for example, might follow this structure:

```text
Search → Read → Extract Evidence → Check Answer → Output
```

If the current node is `Extract Evidence`, the system can surface `Check Answer` together with its conditions and warnings, reducing the chance that the agent jumps directly to an answer.

Unlike plain-text memory, the graph already encodes dependencies between steps. The agent does not need to reconstruct the sequence from a collection of past observations on every run.

![Knowledge graphs and Procedural Graphs compared](/feifeirong.github.io/blog/procedural-graphs/figure-1.png)

*Figure 1 from the paper: a knowledge graph organizes what things are, while a Procedural Graph organizes what to do next. Source: Lu et al., [original paper](https://arxiv.org/pdf/2609.09153).*

## How online execution works

The online path in the paper is compact:

```text
Current task + recent trajectory
              ↓
Match the current node
              ↓
Retrieve a local subgraph within two hops
              ↓
Generate step-specific guidance
              ↓
Let the solver choose and execute an action
```

The system matches the current node against the agent's recent actions. By default, it retrieves only the subgraph within two hops and combines it with the last three trajectory steps. It falls back to the full graph only when node matching fails.

The Guidance LLM turns static graph rules into advice for the current situation. The Solver still reasons about and selects the action. A PG is therefore soft guidance, not a permission boundary or deterministic state machine.

![The Procedural Graph framework](/feifeirong.github.io/blog/procedural-graphs/figure-2.png)

*Figure 2 from the paper: the graph is on the left, local online guidance is in the center, and offline refinement, validation, and rollback are on the right. Source: Lu et al., [original paper](https://arxiv.org/pdf/2609.09153).*

## How the graph evolves

Self-evolution happens after a batch of tasks. The graph does not change during an online run.

The update loop has four stages:

1. Run a batch of tasks with the current graph and record trajectories and scores.
2. Have a Refiner LLM compare high- and low-scoring runs and propose node or edge additions, deletions, or edits.
3. Check the candidate graph's structure and evaluate it on a separate validation set.
4. Accept the change only when validation does not regress. Otherwise, roll it back and store the rejected proposal in rejection memory.

The system updates an external execution structure, not model weights. An LLM may propose the patch, but validation determines whether it becomes the next version.

## What the experiments show

The main evaluation covers six benchmarks and four LLMs, producing 24 model-benchmark settings. All methods use the same ReAct solver, tool interface, and decoding configuration; methods that learn from trajectories receive the same training data. PG ranks first or joint first in 21 settings. Against the strongest baseline in each setting, it records 19 wins, 2 ties, and 3 losses (§5.1, Table 1). The margins are small on HotpotQA, and PG loses with some models, so the benefit is not uniform across tasks.

EnterpriseArena tests long-horizon business decisions. An agent acts as a CFO in a monthly financial simulation for up to 132 simulated months, or 11 simulated years. During each month, it may inspect cash and market conditions, decide whether to seek funding, and then close the books to advance to the next month. The run ends early if cash falls below zero. Three undisclosed crises occur in months 32, 59, and 112.

PG mainly changes when tools are called rather than merely increasing call volume. For example, full-horizon survival rises from 6% to 34% for Gemini 3.1 Pro and from 44% to 58% for Claude Sonnet 4.6 (§5.2).

![Survival rates and cash trajectories for four LLMs in EnterpriseArena](/feifeirong.github.io/blog/procedural-graphs/figure-3.png)

*Figure 3 from the paper: survival rates and cash trajectories across three crises for four LLMs. Blue represents Procedural Graph; red is the no-graph baseline. Source: Lu et al., [original paper](https://arxiv.org/pdf/2609.09153).*

The graph-construction experiments add two useful findings:

- Starting from only a `Start → End` skeleton, repeated execution and validation can grow a useful procedure.
- A flawed expert graph reduced MultiChallenge success from 87.50% to 58.93%. Iterative updates with validation recovered it to 92.86%, while a single static update pushed it down further to 53.57% (§5.3, Table 2).

Validation and rollback are not optional details. An LLM-generated procedure is not necessarily an improvement and should not overwrite the current version automatically.

![Ten rounds of Procedural Graph self-evolution](/feifeirong.github.io/blog/procedural-graphs/figure-4.png)

*Figure 4 from the paper: average survival months and funding amounts across ten self-evolution rounds. Gray shows training results, red validation results, and green dots the test results for accepted versions. Source: Lu et al., [original paper](https://arxiv.org/pdf/2609.09153).*

## Why retrieve only a local subgraph

Putting the full graph into every prompt introduces irrelevant rules and extra tokens. The paper compares raw full-graph injection, full-graph generated guidance, and local-subgraph generated guidance. The local method performs best on all three ablation datasets and uses 14.8%–70.9% fewer tokens than full-graph generated guidance (§5.5, Table 3).

Local guidance still has a cost. Compared with the no-graph baseline, it reduces execution steps on GDPval and ALFWorld but increases total token usage by 33.4% and 55.4%, respectively, because every step adds a Guidance LLM call.

PGs therefore make the most sense when sequence, conditions, and failure recovery matter. A tool chain that finishes in a few steps may not justify another model call at every transition.

## Mapping the idea to agent engineering

In practice, start by breaking one long-running task into a small set of states and transitions. A compatibility-maintenance agent might use:

```text
Detect upstream version
→ Reproduce issue
→ Locate the cause
→ Propose a patch
→ Apply the change
→ Run regression tests
→ Request human approval
→ Release
```

Edges can say that a patch is allowed only after reproduction, failed tests return the agent to diagnosis, and release requires human approval. These rules guide the Solver, but they do not technically prevent an invalid transition.

High-risk actions such as deployment, deletion, payment, or publication still need hard controls in code, permissions, state machines, or approval systems. They should never rely on PG prompts alone.

The paper's design maps to a few straightforward engineering components:

- Store the versioned graph in JSON or YAML so changes can be diffed and rolled back.
- Log the current node, actual action, tool result, and final score for each run.
- Give the guidance layer only a local subgraph instead of repeating every rule in the prompt.
- Let the Refiner produce candidate patches, then merge them only after the validator completes its tests.

For a low-volume workflow, manual graph maintenance is the better starting point. Add LLM-driven refinement only after enough successful and failed trajectories exist and the task has a stable automatic score.

## Limitations to check before adoption

- This is an arXiv preprint released in September 2026, not a peer-reviewed result.
- Self-evolution requires a measurable task score and a separate validation set. Without reliable acceptance criteria, the validation gate cannot tell whether a candidate graph is better.
- The current implementation locates the active node through exact matching against recent actions. Changes to tool names, action formats, or interfaces can break that mapping.
- Some datasets are small or use an LLM judge. The EnterpriseArena self-evolution experiment uses only 20 independent runs each for training, validation, and testing. The authors note that a single acceptance decision can depend on just one or two runs.
- The paper does not yet show that learned procedures transfer reliably across solver models, tool interfaces, or real production systems.
- The Guidance LLM adds latency and token cost. That overhead has to be weighed against fewer errors, retries, and human interventions.

Most teams do not need the full self-evolution system on day one. Start with one failure-prone long task, write down the smallest useful graph, retrieve only the rules near the current node, and use existing tests to decide whether a process change survives. Automate graph refinement only when the execution data is strong enough to support it.
