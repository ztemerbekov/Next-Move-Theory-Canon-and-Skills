# Client adapters

This is the one hand-authored registry for proven Claude Code ↔ Codex
boundaries. It is a compatibility contract, not a second Skill tree, a hidden
router, or a place for Client preferences. Shared Skills keep portable
instructions; the Client supplies only the boundary described here.

### 1. Invocation spelling and namespacing

- **Client:** Claude Code and Codex.
- **Proven incompatibility:** the same Skill may be displayed or directly
  invoked with `/nmt-*` in Claude Code and `$nmt-*` in Codex, and a Plugin may
  add a Client namespace to the visible name.
- **Evidence:** [the divergence matrix](../docs/research/claude-codex-divergence-matrix.md#executive-matrix)
  classifies invocation spelling as a recurring boundary across all eight
  Skill pairs; the [migration specification](../docs/repository-migration-specification.md#mechanical-skill-allowlist)
  limits it to the adapter contract.
- **Portable boundary:** shared source names Skills as `nmt-*` and keeps
  routing semantics in `nmt-chat`. Client-facing markers and namespaces are
  presentation/invocation details; they do not create another router or alter
  a Skill workflow.
- **Drift check:** `scripts/check_adapter_drift.py` fingerprints the shared
  source and rejects any new or changed host-specific invocation wording until
  this registry is explicitly reviewed.

### 2. Interactive-question tooling and limits

- **Client:** Claude Code and Codex.
- **Proven incompatibility:** Claude uses `AskUserQuestion`; Codex exposes
  `request_user_input` with a smaller structured-question contract (one to
  three questions and two to three choices) plus chat fallback.
- **Evidence:** [the divergence matrix](../docs/research/claude-codex-divergence-matrix.md#pair-by-pair-audit)
  records the tool substitution, batching, choice, and fallback differences;
  the producer contract is preserved in `references/producer-contract.md`.
- **Portable boundary:** shared Skill logic describes the information needed
  and the human gate. The Client adapter maps that request to its available
  interaction surface and limits; it must not change the questions' meaning,
  order of work, or completion gate.
- **Drift check:** `scripts/check_adapter_drift.py` fingerprints the shared
  producer contract and every Skill source file, and rejects an unregistered
  interaction API or changed host-specific line.

### 3. Agent/subagent executor lifecycle

- **Client:** Claude Code and Codex.
- **Proven incompatibility:** Claude can expose `Agent`, `subagent_type`, and
  `run_in_background`; Codex uses the execution facilities available in its
  current task and falls back to sequential work when parallel execution is
  unavailable.
- **Evidence:** [the divergence matrix](../docs/research/claude-codex-divergence-matrix.md#pair-by-pair-audit)
  records the executor wording and lifecycle differences in the producer
  Skills; the [portable Skills contract](../docs/research/portable-agent-skills-contract.md)
  defines the shared behavior boundary.
- **Portable boundary:** shared source specifies the work product, evidence
  floor, allowed file side effects, and synthesis gate. It does not assume a
  particular executor API. The Client may parallelize independent work or run
  the same waves sequentially without changing the result contract.
- **Drift check:** `scripts/check_adapter_drift.py` fingerprints all shared
  Skill and contract files and rejects changed executor wording outside this
  reviewed boundary.

### 4. Client discovery and installed-Canon path anchors

- **Client:** Claude Code, Codex, and the explicitly separate Legacy installer.
- **Proven incompatibility:** Claude's relocation-safe installed Plugin anchor
  is `${CLAUDE_PLUGIN_ROOT}/Next-Move-Theory-Canon/`; Codex Skills use the
  installed Plugin-relative `../../Next-Move-Theory-Canon/` path. Legacy uses a
  Consumer-project `Next-Move-Theory-Canon/` root.
- **Evidence:** [the locked migration specification](../docs/repository-migration-specification.md#mechanical-skill-allowlist)
  and [the Canon routing reference](canon-routing.md) define the three
  anchors; [Claude's install research](../docs/research/claude-code-plugin-and-global-install-contract.md#skill-discovery-and-canon-references)
  documents `${CLAUDE_PLUGIN_ROOT}`.
- **Portable boundary:** the Plugin bundles exactly one Canon root. Shared
  source may refer only to the adapter-defined installed anchor; checkout paths,
  Consumer paths, and literal versioned cache paths are not valid Plugin
  dependencies. Legacy paths belong only to `nmt-upgrade` and the transition
  installers.
- **Drift check:** `scripts/check_adapter_drift.py` resolves every declared
  registry link, rejects checkout/cache anchors, and verifies that the eight
  Skills and one Canon root remain inside the Plugin.

### 5. Codex `user-invocable` validator compatibility

- **Client:** Codex.
- **Proven incompatibility:** the current Codex Skill frontmatter validator
  rejects the redundant `user-invocable: true` key; Claude's historical source
  contained that extension.
- **Evidence:** [the source-consolidation report](../docs/migration/source-tree-consolidation.md#mechanical-transformations)
  records the validator finding and the allowlisted normalization; the
  [local Client-validator procedure](../docs/migration/plugin-manifest-and-marketplace-validation.md#client-validators)
  keeps the check outside account authentication.
- **Portable boundary:** omit the redundant key from the shared frontmatter.
  Model discoverability comes from the Skill description and the Plugin
  surface; no workflow, routing, or default visibility rule is added.
- **Drift check:** `scripts/check_adapter_drift.py` fails if
  `user-invocable` reappears in any shared Skill frontmatter or if a second
  client-specific Skill tree is introduced.

## What is not an adapter

Frontmatter information loss, altered Job criteria, missing triggers, mixed
invocation typos, dangling Canon references, and workflow changes are source
defects. They are not Client adapters and must fail parity or source validation.
No additional adapter is valid without new primary evidence and an explicit
map decision.

## Shared-source fingerprint allowlist

The current reviewed shared source is frozen by content fingerprints. This is
deliberate: the existing source contains the reviewed host-boundary wording,
and a later edit must be visible to the drift gate before it can become a new
adapter or semantic change. Update a fingerprint only together with evidence
and a reviewed registry change.

| Shared source file | SHA-256 |
| --- | --- |
| `skills/nmt-analyze-interviews/SKILL.md` | `27ff2cf5421512e84e0651672e91fb3a2c4f6648c7da3cf7fe637f0f5a42e685` |
| `skills/nmt-chat/SKILL.md` | `bbb1300b98136fdf7670331464039f73b2b678b12b0f170549053425ab70663b` |
| `skills/nmt-craft-go-to-market/SKILL.md` | `7409f9d234020b37bc959b4e0ad2372df309a3c12409b736a68b4b60d8d4ff11` |
| `skills/nmt-craft-go-to-market/references/glossary.md` | `414df7118480c0c976ef79f37891ac96e1ad90827e9dbe1f3a2c0c42dd12a2dc` |
| `skills/nmt-craft-value-proposition/SKILL.md` | `73c849662fd5c25ab50d150f22b1b6e6e3633ae2826d191f96c9ce4bf6e25fb5` |
| `skills/nmt-craft-value-proposition/references/glossary.md` | `414df7118480c0c976ef79f37891ac96e1ad90827e9dbe1f3a2c0c42dd12a2dc` |
| `skills/nmt-diagnose/SKILL.md` | `fe8a84235a43bb738de7402417775638f7ca71e9ea0d3b1c82e5d190036f49e8` |
| `skills/nmt-market-research/SKILL.md` | `616cd8566fdb3671e1d7284398dbf4873b0642ff0c58364acf679a3eb143c996` |
| `skills/nmt-market-research/references/glossary.md` | `414df7118480c0c976ef79f37891ac96e1ad90827e9dbe1f3a2c0c42dd12a2dc` |
| `skills/nmt-product-requirements/SKILL.md` | `2868180a3632e6b73b167c692322f2a08a7fbaaf689da3dea6d65f302117bd65` |
| `skills/nmt-product-requirements/references/glossary.md` | `414df7118480c0c976ef79f37891ac96e1ad90827e9dbe1f3a2c0c42dd12a2dc` |
| `skills/nmt-upgrade/SKILL.md` | `b46197976098b75bb695380c7a793c3d888b2c997c15c70c45fcc803665ac2e2` |
| `references/producer-contract.md` | `8da86a00c70a665138e50947a6620a5c4c2f5c3a0fcc32673fc681b1f4c9d974` |
| `references/readability-contract.md` | `4befd0a09fb1b9cf9e4cb515e7d80845edf5784080757b826f0c5927a03e7ada` |
| `references/canon-routing.md` | `7a9796a180893f637b5c754cb8dd0a06ca384591c9e90eed67bdadad177754f0` |
| `references/skill-routing.md` | `a6d7c97a8d0f9ec8e0ea45c9211bfe701c46c6023d5fd76cdc5200b2b9b81e39` |
| `references/methodology-guardrails.md` | `9477b5cb3262a930fdfcf9f0e3af48397606bda7382e6a0fcfd4e40f8c6a2abb` |
