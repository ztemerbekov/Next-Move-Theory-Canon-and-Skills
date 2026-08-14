# Next Move Theory repository migration specification

Status: locked by Wayfinder issue [#12](https://github.com/ztemerbekov/Next-Move-Theory-Canon-and-Skills/issues/12)

Release: `1.0.0`

This document turns the closed Wayfinder decisions into an executable repository
change list. It is the source of truth for the implementation tickets that follow
#12. It specifies the package boundary and file disposition; it does not itself
perform the migration.

## Destination and invariants

The repository root is both the Plugin root and the marketplace root. A fresh
user-global installation copies the Plugin into the Client's user state and does
not write to the Consumer project.

The final distribution has:

- one Plugin named `next-move-theory`;
- one pinned `1.0.0` bundle containing the Canon and all eight Skills;
- one hand-maintained `skills/` source tree;
- one hand-authored `references/client-adapters.md` registry;
- no generated Claude or Codex Skill copies;
- the existing `nmt-chat` Skill as the only model-invoked router;
- the existing `install.sh`, `install.ps1`, and `nmt-upgrade` behavior retained as
  the Legacy transition path;
- no default writes to a Consumer `AGENTS.md`, `CLAUDE.md`, `.nmt-version`,
  `.claude/`, `.agents/`, Canon directory, or Skill directory.

The migration changes packaging and mechanically relocates references. It does
not change a Skill's workflow, questions, modes, handoffs, outputs, methodology,
or completion gates. The current Claude tree is the reviewed behavioral baseline;
the current Codex tree is migration evidence, not a second specification.

## Authoritative final tree

```text
.
├── .agents/
│   └── plugins/marketplace.json       # Codex repository marketplace
├── .claude-plugin/
│   ├── marketplace.json               # Claude repository marketplace
│   └── plugin.json                    # Claude Plugin manifest
├── .codex-plugin/
│   └── plugin.json                    # Codex Plugin manifest
├── Next-Move-Theory-Canon/            # bundled Canon; exact name preserved
├── skills/                            # only editable Skill source tree
│   ├── nmt-analyze-interviews/
│   ├── nmt-chat/
│   ├── nmt-craft-go-to-market/
│   ├── nmt-craft-value-proposition/
│   ├── nmt-diagnose/
│   ├── nmt-market-research/
│   ├── nmt-product-requirements/
│   └── nmt-upgrade/
├── references/
│   ├── methodology-guardrails.md
│   ├── canon-routing.md
│   ├── skill-routing.md
│   ├── producer-contract.md
│   ├── readability-contract.md
│   └── client-adapters.md
├── scripts/                           # static, parity, and smoke tooling
├── tests/                             # fixtures and clean-environment tests
├── docs/                              # installation, updates, Legacy, evidence
├── install.sh                         # retained Legacy installer
├── install.ps1                        # retained Legacy installer
├── AGENTS.md                          # contributor/Legacy source, not installed
├── CLAUDE.md                          # contributor/Legacy source, not installed
├── CHANGELOG.md
├── LICENSE
└── README.md
```

The Plugin manifests contain no Agents, Hooks, MCP servers, or Apps. The
marketplace entries point at this same repository root; they do not create a
second package or a Client-specific content tree.

## File disposition

| Current path | Final path or disposition | Operation | Invariant / proof |
| --- | --- | --- | --- |
| `Next-Move-Theory-Canon/**` | `Next-Move-Theory-Canon/**` | Retain in place and bundle unchanged | Exact directory name, file inventory, and release digest remain stable. |
| `Skills/claude/<eight skills>/**` | `skills/<eight skills>/**` | Consolidate the reviewed Claude baseline into the sole source tree; apply only the mechanical allowlist below | No semantic workflow diff; parity gate reports any unexpected sentence or reorder. |
| `Skills/claude/PRODUCER-CONTRACT.md` | `references/producer-contract.md` | Move byte-preserved shared contract | All producer Skills resolve the new reference; one source only. |
| `Skills/claude/READABILITY-CONTRACT.md` | `references/readability-contract.md` | Move byte-preserved shared contract | All references resolve; no duplicate contract remains. |
| `Skills/claude/<producer>/references/glossary.md` | `skills/<producer>/references/glossary.md` | Retain beside the Skill | Existing glossary behavior and relative links stay intact. |
| `Skills/codex/**` | Retired after migration parity passes; never packaged | Use only as the migration comparison input, then remove the duplicate source tree | Final package has one `skills/` tree; the parity report records the baseline. |
| `AGENTS.md` and `CLAUDE.md` | Same repository paths | Retain as contributor and Legacy-installer sources; update only their agent-facing routing/documentation role | Global Plugin installation never copies or injects either file. |
| `README.md` | `README.md` | Update installation, update, Legacy, and Plugin structure sections | Primary path is user-global Plugin installation; Legacy is clearly marked. |
| `CHANGELOG.md` | `CHANGELOG.md` | Add the `1.0.0` bundle entry while preserving historical entries | Manifest and changelog all declare `1.0.0`; history is not rewritten. |
| `install.sh` | `install.sh` | Retain behavior for one transition release; label through documentation/comments only if needed | It remains project-mutating Legacy behavior and is not called by global Plugin install. |
| `install.ps1` | `install.ps1` | Retain behavior for one transition release; label through documentation/comments only if needed | Same Legacy boundary as `install.sh`. |
| `Skills/*/nmt-upgrade` workflow | `skills/nmt-upgrade/SKILL.md` | Retain workflow and name; only apply packaging-only path/frontmatter mechanics if required by validation | It continues to invoke the Legacy installer and is not the Plugin updater. |
| Existing research under `docs/research/` | Same paths | Retain as evidence | Research remains traceable and is not the runtime source of truth. |
| `docs/installation.md` | New | Document fresh user-global install in Claude Code and Codex | Commands, scope, cache boundary, and zero-Consumer-file guarantee are explicit. |
| `docs/updates.md` | New | Document Client-native update/reload behavior | No `npx upgrade`, no cache editing, no Skill-driven global update. |
| `docs/legacy-installer.md` | New | Document `install.sh`, `install.ps1`, and `nmt-upgrade` as transition-only | No migration, cleanup, reconciliation, or removal is promised. |
| `docs/repository-migration-specification.md` | This file | Lock the implementation contract | Downstream tickets can execute without another architecture decision. |
| `scripts/**` | New | Add deterministic validators, parity checks, inventory checks, and smoke harness | Every script has a documented input, output, exit status, and no Consumer write. |
| `tests/**` | New | Add fixtures for both Clients, package snapshots, and Consumer cleanliness | Tests use isolated user state and never credentials or checkout-relative assumptions. |

## Mechanical Skill allowlist

The source tree is not manually rewritten for behavior. An implementation script
may make only these objectively mechanical changes, recording each transformation:

1. Change references to shared contracts from the old `../...` location to the
   final `../../references/...` location.
2. Make Canon pointers use the relocation-safe Client adapter contract. Claude
   reads through `${CLAUDE_PLUGIN_ROOT}/Next-Move-Theory-Canon/...`; Codex reads
   from the installed Plugin-relative Canon path. No checkout, Consumer, or
   literal cache-version path is allowed.
3. Remove or normalize the proven Codex-incompatible `user-invocable: true`
   metadata without changing default visibility or model-invocation behavior.
4. Move repeated shared guardrail, Canon-routing, and Skill-routing blocks to
   their authoritative `references/` files and replace them with a short
   context pointer that names the condition for loading the reference. The moved
   text is byte-preserved; the pointer is not a new rule.
5. Represent `/nmt-*` versus `$nmt-*`, interactive input, executor lifecycle, and
   Client discovery wording through `references/client-adapters.md` rather than
   maintaining two Skill bodies.

Every other changed line is an unexpected semantic diff and fails migration.
The source and adapter registry are hand-maintained. No generated per-Client
Skill output is committed or shipped.

## Client adapter registry

`references/client-adapters.md` is the one adapter source. Each entry must contain
the supported Client, the exact proven incompatibility, the source evidence, the
portable instruction boundary, and the check that detects drift. The `1.0.0`
registry contains only:

- invocation spelling and namespacing;
- interactive-question tooling and limits;
- agent/subagent/executor lifecycle wording;
- Client discovery and installed-Canon path anchors;
- the Codex `user-invocable` validator compatibility finding.

An adapter is not a second Skill, a hidden routing state machine, or a general
place for Client preferences. `scripts/check_adapter_drift.py` must fail when a
host-specific rule appears in a shared Skill outside an allowlisted pointer or
when a declared adapter reference no longer resolves.

## Manifest and marketplace contract

Both Client manifests identify `next-move-theory` and `1.0.0`:

- `.codex-plugin/plugin.json` declares the root `./skills/` component and the
  complete Codex interface metadata required by the current validator.
- `.claude-plugin/plugin.json` declares the Plugin identity and `1.0.0` metadata.
- `.claude-plugin/marketplace.json` lists the repository-root Plugin with
  `source: "./"` and strict validation.
- `.agents/plugins/marketplace.json` lists the same repository-root Plugin with
  its Git URL source and `AVAILABLE` / `ON_INSTALL` / `Productivity` policy.

Manifest validation must reject nested `Next-Move-Theory-Canon/` copies, missing
Skills, version disagreement, extra runtime components, and paths that leave the
Plugin root.

## Installation and update contract

Documentation uses these user-global flows:

```text
Claude Code:
  claude plugin marketplace add ztemerbekov/Next-Move-Theory-Canon-and-Skills --scope user
  claude plugin install next-move-theory@next-move-theory --scope user

Codex:
  codex plugin marketplace add ztemerbekov/Next-Move-Theory-Canon-and-Skills --ref main
  codex plugin add next-move-theory@next-move-theory
```

The exact Client command syntax is verified by the clean-environment harness;
the documentation never tells a user to copy into a Consumer project or edit a
cache directory. Updates use marketplace refresh plus the Client-native Plugin
operation, followed by the Client reload/new-session boundary. `nmt-upgrade`
and the two Legacy installers remain separate and retain their existing
project-mutating semantics for the transition release.

## Validation and acceptance gates

Implementation is complete only when the repository can prove all of the
following:

1. Claude strict validation and Codex Plugin/Skill validation pass using the
   repository-provided runtime and the documented current compatibility adapter.
2. All eight Skills are present exactly once in `skills/`, and every declared
   Canon/reference path resolves from the installed package.
3. The semantic-parity gate passes the Claude baseline with only the mechanical
   allowlist and reports unexpected diffs with file and line context.
4. The adapter/source/package drift gate passes and detects changed registry,
   source, or package inventories.
5. A clean user-global Codex install discovers and directly smoke-tests all
   eight Skills, reads the bundled Canon from its installed cache, exercises the
   nmt-chat router and negative route, and leaves the Consumer unchanged.
6. The equivalent Claude Code checks pass when a functioning Claude runtime is
   available; no login or Claude repair is part of the repository migration.
7. A native update/reinstall refreshes the installed snapshot in both Clients,
   preserves Skill discovery and Canon access, and leaves the Consumer unchanged.
8. Installation, updating, Legacy behavior, and the no-migration boundary are
   documented and agree with the manifests and scripts.

The known unavailable Claude runtime is recorded as an evidence boundary until a
real functioning Claude environment runs the required checks. It is not converted
into an authentication task or a change to the Skills.

## Downstream implementation slices

After this specification is accepted, implementation work is split into
independently verifiable tickets:

1. scaffold the repository-root manifests and marketplace catalogs;
2. consolidate the Canon, shared references, and one Skill source tree with the
   mechanical transformation/parity gate;
3. author the adapter registry and adapter/source/package drift checks;
4. add package inventory, path, version, and static validation scripts;
5. add isolated Codex and Claude fixtures plus the clean-environment smoke/update
   harness;
6. update README, installation/update/Legacy documentation, AGENTS/CLAUDE
   pointers, and CHANGELOG;
7. run the acceptance matrix, record evidence, and remove the retired duplicate
   Skill source tree only after parity passes.

Each slice must preserve the user changes already present in this worktree and
must not create a commit, push, pull request, or marketplace release.
