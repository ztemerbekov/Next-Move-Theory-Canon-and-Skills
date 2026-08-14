# Clean-environment acceptance contract

Date: 2026-08-14

Wayfinder ticket: [#10 — Define the clean-environment acceptance contract](https://github.com/ztemerbekov/Next-Move-Theory-Canon-and-Skills/issues/10)

## Decision

The Plugin is accepted only after black-box checks pass in clean Codex and Claude Code environments. The checks prove installation, discovery, invocation, bundled-Canon access, model-invoked routing, native updates, adapter/source/package integrity, and zero changes to an unrelated Consumer project.

The acceptance suite does not inspect, rewrite, or semantically judge the inside of a Skill. Existing Skill behavior remains outside this ticket's scope. The suite checks the installed Plugin through its public client behavior and checks only the packaging and adapter contracts needed to detect drift.

## Clean-environment definition

Each client run starts with:

1. a temporary user-level client state directory with no existing Next Move Theory installation, cache, settings, or project-local NMT files;
2. only the credentials needed for the client to run, supplied by the test harness and never committed or printed;
3. a new unrelated temporary Git Consumer project containing a baseline commit and no NMT files;
4. the Plugin installed through the supported user-global path for that client;
5. test logs and fingerprints stored outside the Consumer project.

The test harness must not rely on the repository checkout path, current working directory, a literal installed-cache version, or files injected into the Consumer project.

## Static gates

Before runtime smoke tests, the validation suite must pass all of these checks:

- the repository-root Plugin manifests identify `next-move-theory` and release `1.0.0`;
- the required `Next-Move-Theory-Canon/`, top-level `skills/`, `references/`, `scripts/`, `tests/`, and installation/documentation entries exist;
- all eight Skill entry points have valid portable frontmatter and the expected relative references;
- every bundled Canon pointer resolves from the Plugin package boundary;
- the hand-authored `references/client-adapters.md` registry exists, every declared adapter reference resolves, and no per-Client Skill copy is introduced;
- generated adapter output, when present, is reproducible from the shared source and registry; a changed source, registry, or package copy without the corresponding generated-output update fails the check;
- Claude's strict Plugin validation passes;
- Codex's Plugin preflight and each Skill's static validation pass using the repository-provided validation runtime;
- the semantic-parity gate rejects unexpected changes outside the explicit mechanical adapter/path allowlist.

These gates validate packaging and drift. They do not require edits to any `SKILL.md` file as part of this acceptance ticket.

## Runtime matrix

Run the following against both clients, for sixteen direct Skill smoke calls in total:

| Check | Required observation |
| --- | --- |
| Direct discovery | Each of the eight bundled Skills is discoverable from the user-global installation. |
| Direct invocation | A minimal representative request reaches the named Skill and returns its existing smallest useful output contract. |
| Canon access | At least one required Canon lookup completes from the installed Plugin copy, not from the checkout or Consumer project. |
| Model-invoked router | A product/methodology request without an explicit Skill name reaches the existing `nmt-chat` front door and follows the existing route/handoff behavior. No ninth Skill or second router is introduced. |
| Negative route | A clearly unrelated request does not invoke an NMT Skill and does not write NMT files into the Consumer project. |

The direct requests are short smoke probes, not full workflow evaluations. They prove presence, reachability, and the existing public output shape; they do not grade methodology quality.

The eight direct routes are:

`nmt-analyze-interviews`, `nmt-chat`, `nmt-craft-go-to-market`, `nmt-craft-value-proposition`, `nmt-diagnose`, `nmt-market-research`, `nmt-product-requirements`, and `nmt-upgrade`.

The router and negative-route observations must be captured from client-visible execution evidence (for example, the client trace/session output or an equivalent deterministic test harness record), not inferred only from the final prose answer.

## Consumer-project cleanliness gate

Capture the Consumer project's file list, tracked-file hashes, and Git status before installation. Repeat the capture after:

- Plugin installation;
- Skill discovery;
- all direct smoke calls;
- the router and negative-route probes;
- the client-native update flow.

The result must be byte-for-byte and status-for-status unchanged. In particular, the default global path must not add or modify `AGENTS.md`, `CLAUDE.md`, `.nmt-version`, Skill files, Canon files, settings, or any other Consumer-project file.

## Update gate

The harness installs a first temporary package snapshot, records the installed package fingerprint and client cache/state location, then replaces it with a second package snapshot through the native update surface of each client:

- Claude Code: the documented marketplace/plugin update flow;
- Codex: the documented marketplace refresh and Plugin reinstall flow.

After the update, the harness must observe a changed installed package fingerprint or cache snapshot, successful discovery of all eight Skills, a successful read from the bundled Canon, and the unchanged Consumer-project baseline. The check does not introduce a migration, cleanup, alias, or project-file reconciliation step. It treats the Plugin as a fresh user-global installation, consistent with the `1.0.0` Legacy transition decision.

## Platform boundary

The full runtime smoke matrix is required on the current macOS environment where both supported clients are available. Static checks and portable shell/PowerShell contract checks may run on other platforms. The project must not claim a full Windows clean-environment smoke result unless the same matrix has actually run on Windows.

## Pass/fail evidence

The implementation is accepted only when the test run records:

- client versions and Plugin package fingerprint;
- the clean temporary state locations, without credentials;
- static-gate results;
- sixteen direct smoke results plus the router and negative-route result for each client;
- Canon-read evidence from the installed copy for each client;
- update evidence for each client;
- before/after Consumer file, hash, and Git-status comparison;
- adapter/source/package drift results.

Any failed check blocks acceptance. A passing static suite without both installed-copy client runs is insufficient.

## Scope consequence

This closes the acceptance-contract decision for #10. The remaining implementation work is to turn these black-box checks into repository scripts, fixtures, and documentation after the repository migration specification is locked. No new decision or Fog is created here.
