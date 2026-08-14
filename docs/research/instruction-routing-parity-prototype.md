# Instruction routing parity prototype

Date: 2026-08-14

Wayfinder ticket: [#8 — Design instruction routing without Consumer-project injection](https://github.com/ztemerbekov/Next-Move-Theory-Canon-and-Skills/issues/8)

## Question

Can the current routing and methodology guardrails move inside the globally installed Plugin without changing the behavior of any NMT Skill and without writing rules into a Consumer project's `AGENTS.md` or `CLAUDE.md`?

## Scope boundary

This is a packaging and disclosure prototype, not a redesign of the Skills.

The migration may change only:

- the enclosing directory tree;
- paths needed to reach bundled Plugin files;
- Client-specific invocation spelling and tool/executor wording moved behind `references/client-adapters.md`;
- strict portable frontmatter representation;
- short context pointers that replace moved, byte-preserved reference blocks;
- objectively broken path or invocation spellings.

The migration must not change:

- workflow steps or their order;
- inputs, outputs, modes, handoffs, prerequisites, or completion gates;
- methodology definitions or reasoning rules;
- whether a Skill is conversational or produces an artifact;
- when the current workflow asks the user, performs research, or delegates work.

## Existing behavior used as the baseline

`Skills/claude/` is the behavioral baseline because it contains the complete current descriptions and workflows. `Skills/codex/` is evidence for the four demonstrated host boundaries, not a second behavioral specification. Issue #5 records the places where the Codex copy lost or altered portable semantics.

Baseline SHA-256 values:

| Skill | SHA-256 |
| --- | --- |
| `nmt-analyze-interviews` | `a1cd54b4059bed6d6af80855833bc0e8f97afd6e2cc62b11089cfcc214f40525` |
| `nmt-chat` | `3f0e6d4ba614d2b715b6ad814c1be3a54f162c81114e8d8ce48b8038703ce2a5` |
| `nmt-craft-go-to-market` | `7af3db7787c808b2ed47cec57619d6ffa3390c2919213bedaf4c61e4aafb26b1` |
| `nmt-craft-value-proposition` | `97a7ff27bfc4e241903c5766452683aa7640f93e8246ceb56b4198b9d6c3e91b` |
| `nmt-diagnose` | `d29c831f2d41db8483e29a6f75d3af6395f7f0310a610dd4b130e3026e48c74e` |
| `nmt-market-research` | `e21d3eaaccd7ce1994ae060017105ee18c5809503e756f763ea925270a410add` |
| `nmt-product-requirements` | `713713be5ee6d014df12cf0b5a0aa494ecd691f4324fe7330b741196a7c95074` |
| `nmt-upgrade` | `c37afa3f65736acc247a0675f717f5e1232089cc4235ced5c3ba44903206033c` |

The hashes identify the reviewed baseline. They are not expected to match after path-only migration; the migration validator needs a normalized semantic comparison with an explicit allowlist.

## Router verdict

Use the existing `nmt-chat` Skill as the model-invoked front door. Do not add a ninth Skill and do not introduce a new routing state machine.

- `nmt-chat` already has a broad model-facing description, handles open-ended advice and methodology questions, and contains the current producer handoff.
- Exact artifact requests can continue to activate their specialized Skill directly through that Skill's existing description.
- A handoff loads or recommends another Skill; routing itself does not launch an additional agent. Agent/subagent execution remains inside the selected Skill and uses the existing executor behavior through the Client adapter.
- The existing rule remains: an ambiguous request stays conversational and receives an offer, while an explicit Skill request follows that Skill.

## Route parity matrix

| Existing request branch | Route after packaging | Behavior invariant |
| --- | --- | --- |
| General product advice or methodology explanation | `nmt-chat` | Existing advisor modes and Canon grounding remain unchanged. |
| Live product, metric movement, risks, or growth points | `nmt-diagnose` | Existing diagnostic and next-move handoff remain unchanged. |
| Existing interview or transcript files | `nmt-analyze-interviews` | Existing extraction, clustering, confidence, and executor flow remain unchanged. |
| New idea, market, competitors, or segment selection | `nmt-market-research` | Existing Quick/Deep research workflow remains unchanged. |
| Value proposition or differentiation for a chosen segment | `nmt-craft-value-proposition` | Existing value-mechanics workflow remains unchanged. |
| PRD or product requirements | `nmt-product-requirements` | Existing upstream/manual-input branches and challenge-the-build gate remain unchanged. |
| Positioning, landing copy, ads, launch, or GTM | `nmt-craft-go-to-market` | Existing accepted inputs and communication workflow remain unchanged. |
| Update the installed NMT distribution | `nmt-upgrade` | Migration behavior is decided separately in #9; #8 adds no update semantics. |
| Work outside NMT's product-methodology boundary | no NMT activation | The Plugin does not claim unrelated work. |

## Progressive disclosure hierarchy

The hierarchy moves existing material without rewriting its meaning:

```text
host-loaded Skill catalog
  └── existing name + model-facing description for each Skill

skills/nmt-chat/SKILL.md
  └── existing conversational/router workflow

references/methodology-guardrails.md
  └── existing shared NMT rules currently supplied through Consumer AGENTS.md / CLAUDE.md

references/canon-routing.md
  └── existing intent-to-Canon routing table and lazy-loading rules

references/skill-routing.md
  └── existing eight-Skill quick map, handoffs, and prerequisites

references/client-adapters.md
  └── only the four demonstrated host boundaries from issues #5 and #6
```

Every Skill keeps its existing workflow. A short pointer replaces only material moved verbatim into an authoritative shared reference. The pointer states when to load that reference. Material still needed on every path stays in `SKILL.md`.

## Consumer boundary

The default Plugin installation writes no Consumer files. The current repository-level `AGENTS.md` and `CLAUDE.md` remain contributor/Legacy-installer sources during the transition release, but the global Plugin does not copy or inject them. Their NMT guardrails travel inside the Plugin references and are reached through model-invoked Skill pointers.

## Parity gate for migration

The migration validator must compare every migrated Skill with its baseline after normalizing only the allowed mechanical changes:

1. directory and Plugin-relative path spelling;
2. `/nmt-*` and `$nmt-*` invocation spelling represented through the Client adapter;
3. interactive-tool and executor names represented through the Client adapter;
4. Client discovery and path anchors represented through the Client adapter;
5. strict portable frontmatter formatting;
6. exact reference blocks moved behind context pointers;
7. known broken references corrected as path/invocation defects.

Any other changed sentence or reordered workflow block fails the gate. The failure must show the unexpected diff. This check becomes part of the normal validation suite, not a separate user-facing command.

## Prototype result and remaining proof

The structural model preserves the current route for all eight existing Skills without a new routing algorithm and removes the need for Consumer instruction injection. It also provides a deterministic boundary for later migration review: only allowlisted mechanical transformations may change a Skill file.

This result does not prove host behavior after installation. Ticket #11 must still install the candidate Plugin in clean Codex and Claude Code environments and demonstrate model invocation, direct invocation, Canon access, handoff behavior, and zero Consumer-project changes.
