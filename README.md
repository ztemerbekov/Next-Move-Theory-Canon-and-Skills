# Next Move Theory Canon & Skills

**English** · [Русский](./README.ru.md)

## English

Next Move Theory Canon & Skills is a user-global Plugin for Codex and Claude Code that helps founders and product managers decide what to build, for whom, and what to test before spending months on the wrong build. It combines an open canon with skills that start from a product conversation and route from market research to a value proposition, a build-ready product requirements document, and go-to-market work; every decision is anchored in the customer’s desired task (Job), concrete success criteria, target segment, and riskiest assumption.

### At a glance

- **For product builders.** Founders, indie hackers, product managers, senior product leaders, and product marketers.
- **Start with `nmt-chat`.** It is the conversational entry point and router: paste an idea, notes, research, or a live product situation; it separates evidence from assumptions and points to the next concrete move.
- **Use the customer’s real task.** A Job is the transition a person wants to make from a current situation to an expected outcome. A segment is a group of people with similar Jobs and similar success criteria.
- **Make value concrete.** Value means helping a segment reach its outcome with better results and less total cost—money, time, effort, mental effort, negative emotion, or rework—against its success criteria.
- **Test the dangerous assumption first.** The riskiest assumption (RAT) is the assumption most likely to sink the initiative; test it cheaply before building.
- **License and author.** The canon and skills are by Ivan Zamesin and licensed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/).

### A tiny example

Suppose a founder says: “I want to build an AI planner for freelancers.” The useful starting point is not the feature. It is the decision underneath it:

> **Job:** “I want to turn a messy client request into a clear next step by tomorrow.”
>
> **Segment:** Freelancers who perform that same main task and judge success by speed and reduced uncertainty.
>
> **Value hypothesis:** Help them reach that outcome with less time and mental effort than their current option.
>
> **Riskiest assumption:** This segment will pay at the planned price. Test it with people who have already paid for similar help and a small demand test before building.

The sequence is deliberate: name the desired transition, choose the people with similar Jobs and criteria, define the value to deliver, then test the assumption most likely to kill the idea.

### Getting started

Install the suite globally:

```bash
npx skills@latest add ztemerbekov/Next-Move-Theory-Canon-and-Skills -g
```

Then:

1. Start with [`nmt-chat`](skills/nmt-chat/), the conversational entry point and router.
2. Paste whatever you have: a half-formed idea, messy notes, interview material, a product brief, or a live product problem.
3. Ask for the next move. The conversation can stay focused on a decision, or route to the producer skill that creates the artifact you need.

### The path from idea to build or launch

For a new idea, follow the producer path in this order:

```text
nmt-market-research
        ↓
nmt-craft-value-proposition
       ↙ ↘
nmt-product-requirements   nmt-craft-go-to-market
```

1. **`nmt-market-research`** — research the market, map and score segments, identify their Jobs, and decide whether to proceed, narrow, or pivot.
2. **`nmt-craft-value-proposition`** — turn a chosen segment and its Jobs into a concrete value proposition and implementation direction.
3. **`nmt-product-requirements`** — turn the chosen segment and value into a build-ready product requirements document: what to build and which edge cases matter.
4. **`nmt-craft-go-to-market`** — turn the value proposition into landing-page copy, ads, and a go-to-market communication plan: how to sell it.

The last two paths can run in either order, or both can be used. If you already have a live product, start with [`nmt-diagnose`](skills/nmt-diagnose/). If you have interviews, sales calls, support calls, or open-ended survey answers, use [`nmt-analyze-interviews`](skills/nmt-analyze-interviews/) to extract Jobs, success criteria, and value hypotheses.

### Skill map

| Skill | Use it for |
| --- | --- |
| [`nmt-chat`](skills/nmt-chat/) | Advice, explanation, pressure-testing, and routing to the next skill. |
| [`nmt-diagnose`](skills/nmt-diagnose/) | Finding where a live product or metric is breaking before prescribing a fix. |
| [`nmt-analyze-interviews`](skills/nmt-analyze-interviews/) | Turning interviews, notes, sales or support calls, and survey open-ends into Jobs, criteria, and value hypotheses. |
| [`nmt-market-research`](skills/nmt-market-research/) | Researching the market and choosing which segment and Jobs to compete for first. |
| [`nmt-craft-value-proposition`](skills/nmt-craft-value-proposition/) | Defining how the chosen segment will receive value and why it should choose this option. |
| [`nmt-product-requirements`](skills/nmt-product-requirements/) | Creating the build-ready product requirements document. |
| [`nmt-craft-go-to-market`](skills/nmt-craft-go-to-market/) | Creating landing-page copy, ads, and a go-to-market communication plan. |

### The decision model

The methodology follows one causal chain:

```text
Market with money
  → Segment + Job
  → Added Value
  → Unit economics + demand + ability to scale
  → Conversion + retention + repeat
  → Profit
```

The order matters. A market is defined by what people already spend to perform Jobs, not only by a category name. A segment is chosen by similarity of Jobs and success criteria, with economics and reachable demand attached. Value is the customer’s outcome over the costs of reaching it; a feature is only the delivery format. Aha Moments signal that the delivered result beat the customer’s prediction, while a Problem signals under-delivery. When a downstream metric breaks, investigate the upstream segment, Job, and value before optimizing the funnel.

Next Move Theory combines Advanced Jobs To Be Done (AJTBD), Unit Economics, the Riskiest Assumption Test (RAT), ABCDX Segmentation, and Theory of Constraints into one system for product decisions. Objectives and Key Results (OKR) are a supporting goal-setting methodology in the canon.

### Read the canon

For a short route through the public foundation, read:

1. [`nmt-key-theses.md`](skills/nmt-chat/references/Next-Move-Theory-Canon/Next-Move-Theory/nmt-key-theses.md) — how Jobs, value, economics, demand, and validation fit into one chain.
2. [`ajtbd-key-theses.md`](skills/nmt-chat/references/Next-Move-Theory-Canon/Advanced-Jobs-To-Be-Done/ajtbd-key-theses.md) — Jobs, Job Graphs, segments, success criteria, value, and behavior change.
3. [`communication.md`](skills/nmt-chat/references/Next-Move-Theory-Canon/Advanced-Jobs-To-Be-Done/communication.md) — how to communicate value in the language of Jobs and criteria.

The canon is also available in a more readable form at [nextmovetheory.com/library/canon](https://nextmovetheory.com/library/canon?utm_source=canon&utm_medium=github). The broader methodology, books, and related materials are at [nextmovetheory.com](http://nextmovetheory.com/?utm_source=canon&utm_medium=github).

### The book

[*The Nature of Product*](https://nextmovetheory.com/library/the-nature-of-product?utm_source=canon&utm_medium=github) is free to read on the site. It introduces the Advanced Jobs To Be Done foundation for founders, indie hackers, product managers, marketers, and designers who make product decisions with incomplete evidence.

### License and attribution

The canon and skills are licensed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/). See [`LICENSE`](LICENSE) and [`NOTICE.md`](NOTICE.md) for the license, attribution, and repository-specific notices. When sharing or adapting the material, credit Ivan Zamesin, link back to this repository and the license, and keep the same license for adaptations.

Methodology and text by **Ivan Zamesin** — [nextmovetheory.com](http://nextmovetheory.com/?utm_source=canon&utm_medium=github) · [X](https://x.com/zamesin) · [LinkedIn](https://www.linkedin.com/in/ivan-zamesin/).
