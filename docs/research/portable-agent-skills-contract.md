# Portable Agent Skills contract

Research date: 2026-08-14

## Question

Which Skill directory, frontmatter, invocation, reference, script, and capability conventions are genuinely portable across the current Agent Skills specification, Codex, and Claude Code, and which documented incompatibilities require a client adapter?

## Source boundary and labels

This report uses only the current [Agent Skills specification](https://agentskills.io/specification), its first-party [client implementation guide](https://agentskills.io/client-implementation/adding-skills-support) and [script guidance](https://agentskills.io/skill-creation/using-scripts), [official OpenAI documentation for Codex skills](https://learn.chatgpt.com/docs/build-skills), and [official Claude Code skill documentation](https://code.claude.com/docs/en/skills). It does not infer behavior from third-party clients or this repository's current installers.

The findings distinguish:

- **Standard** — required or defined by the Agent Skills specification.
- **Client extension** — behavior documented only for Codex or Claude Code.
- **Inference** — a packaging recommendation derived from those facts, not a standard guarantee.

## Answer in one sentence

Maintain one strict Agent Skills source tree: a directory whose name matches the required `name`, a `SKILL.md` with standard frontmatter and Markdown instructions, and optional relatively referenced `scripts/`, `references/`, and `assets/`; keep invocation policy, literal invocation syntax, argument interpolation, dynamic shell injection, subagent/model/tool policy, discovery paths, and dependency/UI metadata outside that portable core.

The shared Skill source does **not** need Codex and Claude copies. Client adapters are needed only when the product relies on behavior that the standard does not define.

## The genuinely portable contract

### Directory and entry point

The strict common directory is:

```text
<skill-name>/
├── SKILL.md
├── scripts/       # optional
├── references/    # optional
├── assets/        # optional
└── ...            # optional additional files
```

**Standard.** A Skill is a directory containing `SKILL.md`. `scripts/`, `references/`, and `assets/` are recommended conventions, not required directories; additional files and directories are permitted. The parent directory name must match the frontmatter `name`. See the specification's [directory structure, name constraints, and optional directories](https://agentskills.io/specification).

**Portable rule.** Use lowercase ASCII letters, digits, and single hyphens; keep the name at 1–64 characters; do not begin or end with a hyphen; do not use consecutive hyphens; and make the folder and `name` identical. Claude Code is more lenient — it can derive a missing name from the directory and uses the name differently for command display — but relying on that leniency would violate the standard. Claude documents this difference in its [frontmatter reference and command-name rules](https://code.claude.com/docs/en/skills#frontmatter-reference).

### Frontmatter

The complete standard frontmatter vocabulary is:

| Field | Standard status | Portable use |
| --- | --- | --- |
| `name` | Required | Use strict standard syntax and match the directory. |
| `description` | Required | Describe both what the Skill does and when it applies; front-load the trigger. |
| `license` | Optional | Portable as declarative metadata. |
| `compatibility` | Optional | Portable as a declaration of runtime, product, package, network, or environment requirements; do not assume a client enforces it. |
| `metadata` | Optional | Use a string-to-string map only. |
| `allowed-tools` | Optional, experimental | Syntactically standard only as a space-separated string; its tool vocabulary and permission effect are not portable. |

The limits are `name` ≤ 64 characters, `description` ≤ 1,024 characters, and `compatibility` ≤ 500 characters. `metadata` is a map from string keys to string values. These are the normative [frontmatter constraints](https://agentskills.io/specification#frontmatter).

A behaviorally portable file should normally stay within the first five fields:

```yaml
---
name: example-skill
description: Explain what the Skill does and the concrete requests that should trigger it.
license: MIT
compatibility: Requires Git and filesystem access.
metadata:
  author: example-org
  version: "1.0.0"
---
```

`allowed-tools` belongs to the standard syntax but not the reliable common behavior. The specification calls it experimental and says support may vary. Claude Code gives it a concrete, one-turn permission-grant meaning, while the official Codex Skill page does not document equivalent `SKILL.md` permission semantics. A portable Skill may carry the field only if correct execution does not depend on the grant. See the specification's [`allowed-tools` definition](https://agentskills.io/specification#allowed-tools-field) and Claude's [permission semantics](https://code.claude.com/docs/en/skills#pre-approve-tools-for-a-skill).

### Instructions, disclosure, and activation

**Standard.** The body after frontmatter is Markdown with no prescribed section schema. Clients expose `name` and `description` first, load the full `SKILL.md` on activation, then load bundled resources on demand. The specification recommends keeping `SKILL.md` below 500 lines and its instruction tier below roughly 5,000 tokens. See [progressive disclosure](https://agentskills.io/specification#progressive-disclosure).

**Common client behavior.** Codex and Claude Code both document implicit activation from the description and explicit user activation. Codex uses `@` in ChatGPT and `$skill-name` in Codex CLI or IDE (with `/skills` for discovery); Claude Code uses `/skill-name`. The Agent Skills client guide explicitly leaves the user's invocation syntax to the client. Therefore literal `$`, `@`, or `/` invocation commands are not part of a portable Skill contract. See [Codex activation](https://learn.chatgpt.com/docs/build-skills#how-chatgpt-and-codex-use-skills), [Claude activation](https://code.claude.com/docs/en/skills), and [standard client guidance](https://agentskills.io/client-implementation/adding-skills-support#user-explicit-activation).

**Portable rule.** Make the default shared Skill usable through both implicit and explicit activation. Put every model-invocation trigger in `description` rather than a client-only field. Put client-specific command examples in client-facing installation/help material, not in the core instructions.

Descriptions must be front-loaded and compact. The standard caps them at 1,024 characters. Claude Code truncates its combined `description` and extension field `when_to_use` at 1,536 characters, while Codex applies a total initial-catalog budget and can shorten or omit descriptions when many Skills are installed. See [Claude's frontmatter reference](https://code.claude.com/docs/en/skills#frontmatter-reference) and [Codex progressive-disclosure limits](https://learn.chatgpt.com/docs/build-skills).

### References and assets

**Standard.** Reference files by relative path from the Skill root and keep reference chains shallow. A portable pointer looks like:

```markdown
Read [the interview guide](references/interview-guide.md) when preparing interview questions.
```

The standard recommends one-level-deep references and on-demand loading. Claude likewise tells authors to link supporting files from `SKILL.md`; Codex documents `references/` and `assets/` as optional Skill directories. See [standard file references](https://agentskills.io/specification#file-references), [Claude supporting files](https://code.claude.com/docs/en/skills#add-supporting-files), and [Codex Skill structure](https://learn.chatgpt.com/docs/build-skills).

**Portable rule.** Use normal Markdown links or plain relative paths and state the condition for reading each file. Do not use Claude's `@path` attachment behavior as the only way a resource is supplied. Do not hard-code a repository checkout path or a user's home directory.

### Scripts and capability assumptions

**Standard.** A Skill may bundle executable code in `scripts/`. Scripts should be self-contained or document dependencies, be non-interactive, handle edge cases, and return useful errors. Supported languages depend on the agent implementation. The first-party script guide recommends relative paths, pinned dependencies, a `--help` interface, and structured output where useful. See [the standard script convention](https://agentskills.io/specification#scripts) and [using scripts in Skills](https://agentskills.io/skill-creation/using-scripts).

The standard does not define a guaranteed shell, runtime, network connection, MCP server, tool-name vocabulary, permission model, or writable location. Those are environment capabilities, not properties of the Skill format. Declare true prerequisites in `compatibility`, and write instructions that let the agent check them before running a script.

**Portable path rule.** Refer to `scripts/foo` relative to the directory containing `SKILL.md`; the client integration guide tells agents to resolve such references against the Skill directory and use absolute paths in tool calls. Do not rely on the process already running with the Skill directory as its current working directory. See the [activation and path-resolution guidance](https://agentskills.io/client-implementation/adding-skills-support#behavioral-instructions).

**Inference.** If a script needs a deterministic install path, keep path resolution in the agent instructions or in a small wrapper that receives the resolved path. `${CLAUDE_SKILL_DIR}` is convenient in Claude Code but is not a portable variable.

## Documented incompatibilities and adapter boundary

| Area | Documented difference | When an adapter is required |
| --- | --- | --- |
| Standalone discovery | The standard does not mandate install locations. Codex scans repository and user `.agents/skills` locations; Claude Code documents `.claude/skills` locations. Both also load Skills bundled by their plugin system. | A standalone global installer needs client-specific placement or symlinks. This is an installation adapter, not a second Skill source. |
| Manual invocation | ChatGPT uses `@`, Codex CLI/IDE uses `$`, and Claude Code uses `/`. | Only user-facing help, launchers, or tests that type the invocation need client variants. The Skill body does not. |
| Manual-only policy | Codex documents `agents/openai.yaml` with `policy.allow_implicit_invocation: false`; Claude Code uses non-standard `disable-model-invocation: true` in `SKILL.md`. | Required when a Skill must never be selected implicitly. There is no standard field for this policy. |
| User visibility | Claude Code adds `user-invocable: false`; the Codex Skill documentation does not define an equivalent standard field. | Required when a Skill must be model-only or hidden from the user's command surface. |
| Claude frontmatter extensions | Claude Code adds `when_to_use`, `argument-hint`, `arguments`, `disable-model-invocation`, `user-invocable`, `disallowed-tools`, `model`, `effort`, `context`, `agent`, `background`, `hooks`, `paths`, and `shell`. | Required whenever the workflow depends on one of those behaviors. Keep these keys out of the portable `SKILL.md`; Claude documents that uploads outside Claude Code hard-fail on non-standard keys. |
| Standard-field leniency | Claude Code permits omitted `name` and `description`, accepts broader boolean spellings, allows richer `metadata`, and accepts list/comma forms for `allowed-tools`; the standard is stricter. | No adapter is needed if the source follows the strict standard. A normalization adapter is needed only for existing Claude-authored Skills that rely on the leniency. |
| Arguments and substitutions | Claude Code expands `$ARGUMENTS`, indexed and named arguments, and `${CLAUDE_*}` variables. The standard defines none of them, and Codex's Skill documentation does not promise them. | Required if the body expects textual interpolation. Prefer natural-language task context or a script with explicit arguments in the shared source. |
| Dynamic context injection | Claude Code supports ``!`command` `` and fenced `!` blocks before the model sees the Skill. The standard and Codex Skill documentation do not define this. | Required if pre-render shell output is essential. A portable alternative is an instruction telling the agent to run the command after activation. |
| Forked execution and lifecycle controls | Claude Code adds `context: fork`, `agent`, `background`, model/effort overrides, Skill hooks, and path-scoped activation. | Required if isolation, a fixed subagent, backgrounding, hooks, or path routing is part of correctness. These are host orchestration, not Skill content. |
| Tool permissions | Standard `allowed-tools` is experimental. Claude gives it a specific one-turn permission effect and adds `disallowed-tools`; tool identifiers and enforcement are host-specific. | Required when execution must depend on pre-approved or denied tools. Otherwise omit behavior-critical permission assumptions. |
| UI and dependency metadata | Codex adds optional `agents/openai.yaml` for appearance, default prompt, implicit-invocation policy, and MCP tool dependencies. This is outside `SKILL.md`. | No duplicated Skill is necessary: a Codex sidecar can coexist in the shared directory. A client wrapper is required only when equivalent dependency provisioning or UI metadata must be expressed for another host. |
| Name collisions and overrides | Codex says same-named Skills are not merged and both may appear. Claude defines source precedence and namespaces plugin Skills. The standard does not give portable override/alias semantics. | Use globally distinct names. An adapter is required only if the product intentionally depends on shadowing, aliases, or a particular command namespace. |
| Runtime and operating system | Script languages, shells, network access, packages, and sandbox permissions vary by implementation and environment. Claude's `shell: powershell` is a client extension. | An environment-specific script/wrapper is required when one implementation cannot satisfy the declared `compatibility`; this is not evidence for separate Codex and Claude instruction copies. |

The Claude-specific extension list and the hard-error behavior for non-standard upload frontmatter are documented under [Using Skill frontmatter outside Claude Code](https://code.claude.com/docs/en/skills#using-skill-frontmatter-outside-claude-code). Codex's sidecar schema is documented under [Optional metadata](https://learn.chatgpt.com/docs/build-skills#optional-metadata).

## What can remain one source

One source tree can safely contain:

- the strict-standard `SKILL.md`;
- all canon/reference documents reached through relative pointers;
- cross-platform or compatibility-declared scripts and assets;
- optional client sidecars in additional directories, such as `agents/openai.yaml`, because the Agent Skills directory format permits additional files.

**Inference.** A generated client copy is justified only when client-specific behavior must live in `SKILL.md` itself — most notably Claude-only frontmatter or body substitutions. Codex's documented extension is already a sidecar, so it does not by itself justify a Codex-specific copy of the Skill.

Outer plugin manifests, marketplace metadata, and release workflows are distribution contracts rather than the Agent Skills contract. They can wrap the same `skills/` subtree and should be decided separately.

## Residual uncertainty

The official Codex Skill documentation does not state how Codex handles unknown `SKILL.md` frontmatter keys, whether it acts on standard `allowed-tools`, or whether it validates every optional standard field. The contract therefore relies only on what Codex documents plus the strict standard; it does not assume that Claude extensions will be ignored safely.

The sources also do not promise that Claude Code will ignore every possible unreferenced client sidecar. The narrower supported conclusion is that extra files are valid in an Agent Skills directory and that `agents/openai.yaml` is Codex's documented sidecar. Whether a final cross-client plugin package should include that sidecar unchanged belongs to plugin-package validation, not to this Skill-format decision.

Finally, documentation establishes the intended semantics of each client's invocation policy but not behavioral equivalence under every host version, sandbox, or plugin surface. Any selected non-standard behavior still needs an installation smoke test in both clients. No further uncertainty affects the strict shared `SKILL.md` contract.

## Decision-ready contract for this repository

1. Author each Next Move Theory Skill once, under one `skills/<name>/` tree.
2. Validate every source Skill against the strict Agent Skills specification.
3. Restrict shared frontmatter to `name`, `description`, `license`, `compatibility`, and string-valued `metadata`; treat `allowed-tools` as non-portable unless it is nonessential.
4. Put all activation triggers in `description`; support both implicit and explicit use by default.
5. Use only relative Markdown pointers and relative script references; resolve them from the Skill root at runtime.
6. Express runtime assumptions in `compatibility` and check them in the workflow or script.
7. Keep Codex-only UI/dependency metadata in `agents/openai.yaml`.
8. Generate or maintain a client adapter only for a consciously selected non-standard behavior, with a test that proves the portable source is insufficient.

This contract removes the current architectural reason for parallel hand-maintained Codex and Claude Skill directories while preserving a precise escape hatch for real client incompatibilities.
