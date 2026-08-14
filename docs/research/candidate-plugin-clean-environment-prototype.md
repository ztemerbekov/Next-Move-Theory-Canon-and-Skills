# Candidate Plugin clean-environment prototype

Date: 2026-08-14

Wayfinder ticket: [#11 — Prove the candidate Plugin contract in clean environments](https://github.com/ztemerbekov/Next-Move-Theory-Canon-and-Skills/issues/11)

Related acceptance decision: [#10 — Define the clean-environment acceptance contract](https://github.com/ztemerbekov/Next-Move-Theory-Canon-and-Skills/issues/10)

## Question

Does the smallest concrete repository-root Plugin skeleton install in clean Codex and Claude Code fixtures, expose all eight Skills, read the bundled Canon from the installed copy, leave an unrelated Consumer project unchanged, and reveal any incompatibility that must be handled before migration?

## Prototype boundary

The candidate was assembled in `/private/tmp` from the current repository without changing any source Skill:

- `Next-Move-Theory-Canon/` was copied as one Plugin-root sibling;
- `Skills/claude/` was copied into one shared `skills/` tree;
- both `1.0.0` client manifests were added;
- a minimal `references/client-adapters.md` registry was added;
- separate local Codex and Claude marketplace fixtures pointed at the same candidate shape;
- each client received a temporary user state and an unrelated empty Git Consumer project.

This is a packaging/runtime probe, not the repository migration. It does not reconcile the two current Skill trees and does not change Skill instructions.

## Static results

| Check | Result |
| --- | --- |
| Claude plugin manifest, strict | Passed after adding explicit `author` metadata required by the current strict validator. |
| Claude marketplace manifest, strict | Passed. |
| Codex bundled Plugin preflight | Passed with the bundled workspace Python plus temporary PyYAML dependency. |
| Canon shape | Passed in the corrected candidate: one `Next-Move-Theory-Canon/` root containing 23 files. |
| Skill inventory | Eight immediate-child Skill directories were present. |
| Codex Skill quick validation | Failed for all eight current Skills because `user-invocable` is not in the validator's allowed frontmatter keys: `allowed-tools`, `description`, `license`, `metadata`, `name`. |

The frontmatter result is a demonstrated host/tooling boundary. It is not a license to rewrite Skill behavior in this ticket; the migration specification must choose the smallest cosmetic compatibility treatment and keep the semantic-parity gate.

## Codex installation and runtime

In an isolated `HOME` and `CODEX_HOME`, the local marketplace and Plugin install completed:

- marketplace: `next-move-theory-prototype-v2`;
- Plugin: `next-move-theory@next-move-theory-prototype-v2`;
- installed cache: `.../plugins/cache/next-move-theory-prototype-v2/next-move-theory/1.0.0`;
- `codex plugin list --json` reported the Plugin as installed and enabled;
- the cache contained exactly eight Skill directories and one Canon root.

A model smoke with an explicit `$nmt-chat` request loaded:

`.../1.0.0/skills/nmt-chat/SKILL.md`

and read Canon files from the same installed cache, including:

`.../1.0.0/Next-Move-Theory-Canon/Advanced-Jobs-To-Be-Done/ajtbd-key-theses.md`

and

`.../1.0.0/Next-Move-Theory-Canon/Next-Move-Theory/nmt-key-theses.md`.

The Codex runtime therefore proves user-global cache installation, direct Skill discovery/invocation, and installed-copy Canon access for the candidate.

## Claude Code installation and runtime

In isolated `CLAUDE_CONFIG_DIR` and `CLAUDE_CODE_PLUGIN_CACHE_DIR` directories:

- the local marketplace was added at user scope;
- `next-move-theory@next-move-theory-prototype-v2` was installed at user scope;
- `claude plugin list` reported version `1.0.0` as enabled;
- `claude plugin details` reported exactly eight Skills and no unexpected Agents, Hooks, or MCP servers;
- the cache contained the Plugin root, one Canon root, eight Skills, and the adapter registry.

The model smoke was not executed because Claude Code is unavailable as a functioning runtime in this workspace. The earlier isolated attempt returned:

`Not logged in · Please run /login`

This leaves Claude model invocation and Claude-side Canon reading unverified. No user login or authentication step is part of this prototype decision; the unavailable client is an environment limitation, not a package validation result.

## Consumer cleanliness

The Codex fixture started as an empty initialized Git repository. After marketplace registration, Plugin installation, two read-only Codex smoke calls, and all inspected runtime commands:

- `git status --porcelain` remained empty;
- no files were created in the Consumer project.

The Claude install and details commands also operated only on the temporary user/cache state; no Consumer files were written. The unavailable Claude runtime is recorded as an explicit verification boundary rather than converted into a user setup task.

## Design findings

The candidate package boundary itself is viable in both clients: one root, one Canon, one shared `skills/` tree, client manifests, and user-global cache copies.

Two migration constraints are now evidence-backed:

1. The current Skills use bare `Next-Move-Theory-Canon/...` references. A final package must make Canon resolution relocation-safe for both clients; a model finding a file by searching the cache is not a substitute for a deterministic Skill path contract.
2. The current `user-invocable` frontmatter is accepted by Claude but rejected by the current Codex Skill validator. The migration must resolve this as an explicitly allowlisted cosmetic/client-compatibility difference, without duplicating or semantically rewriting Skills.

The first temporary staging also exposed a packaging hazard: copying the Canon directory with the destination named after the source produced `Next-Move-Theory-Canon/Next-Move-Theory-Canon/`. The corrected candidate uses directory contents, not a nested directory, and the static inventory gate catches this class of error.

## Current verdict

The candidate skeleton passes package validation, user-global installation, Skill inventory, Codex direct invocation, Codex installed-Canon access, and Consumer cleanliness. It proves the selected package shape is viable and exposes the path/frontmatter work that belongs in the migration specification.

The prototype decision is closed with one environment boundary: Claude model invocation and Claude installed-Canon reading were not executable in this workspace. The package shape itself passed all available static and install/discovery checks; no authentication or Claude repair is required to interpret this prototype result.
