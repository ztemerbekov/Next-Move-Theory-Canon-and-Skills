# Final inventory and acceptance status

Wayfinder ticket: [#16 — Run acceptance matrix and retire the duplicate Skill source tree](https://github.com/ztemerbekov/Next-Move-Theory-Canon-and-Skills/issues/16)

This file records the implementation inventory and the evidence boundary. It
does not claim Destination until the exact public owner/repository command has
been tested against the remotely available implementation and the remaining
runtime boundary is cleared.

## Repository inventory

- `.codex-plugin/plugin.json` and `.claude-plugin/plugin.json` identify one
  `next-move-theory` Plugin at version `1.0.0`.
- `skills/` is the one editable, hand-maintained Skill source tree and contains
  the eight NMT Skill entry points.
- `skills/nmt-chat/references/Next-Move-Theory-Canon/` is the one bundled Canon
  root, carried by the `nmt-chat` payload in the installed suite.
- `skills/nmt-chat/references/` contains the shared routing, methodology,
  adapter, producer, and readability contracts.
- `scripts/` and `docs/` contain static validation, adapter drift, acceptance,
  installation, update, and migration-boundary instructions. The active tree
  does not ship the old shell or PowerShell installers.
- `docs/migration/legacy-inputs/Skills/` contains immutable Claude and Codex
  baseline evidence for semantic parity. It is not a runtime Skill tree.
- Repository-level `Skills/claude/` and `Skills/codex/` are retired. No
  Client-specific replacement tree was generated.

## Evidence recorded on 2026-08-14

The following checks passed:

```text
python3 scripts/check_static_validation.py       PASS
python3 scripts/check_adapter_drift.py           PASS
claude plugin validate . --strict                PASS
Codex authenticated clean-environment harness   PASS
```

The authenticated Codex run covered installation, discovery, the eight direct
Skill probes, bundled Canon access, the model-invoked router, the negative
unrelated route, reinstall/update, and unchanged Consumer files. Temporary
state was cleaned and credentials were not printed or persisted.

Claude Code was intentionally not authenticated or invoked for model smoke.
The available evidence is version/static validation only. Therefore this file
does not claim a Claude runtime pass, and the overall Destination remains open
until an authorized Claude clean-environment smoke run is available.

## Final local acceptance evidence — 2026-08-15

The local implementation commits for the final slices are:

```text
0b8d880  feat: repackage suite around nmt-chat payload       (#22)
d0b8dbd  docs: replace legacy installer with skills CLI      (#23)
a15dd22  test: prove isolated skills CLI acceptance flow     (#24)
```

They are local commits only. No push, pull request, or marketplace release was
performed. The checkout intentionally retains the unrelated untracked research
file `docs/research/skills-cli-installers-license-audit.md`.

### Commands and results

| Command | Result | Evidence boundary |
| --- | --- | --- |
| `python3 -B scripts/check_static_validation.py` | PASS | Manifests, version, nested Canon inventory, frontmatter/path checks, parity, adapter drift, public docs, links, and negative fixtures. |
| `python3 -B scripts/check_skills_cli_packaging.py --mode both` | PASS | `skills@latest` `1.5.22`; temporary HOME/XDG/npm state; two Client targets; eight Skills; Canon/shared references; copy/symlink modes; idempotent reinstall; partial-install rejection; unchanged Consumer fixture. |
| `python3 -B scripts/run_acceptance_harness.py --client all --report /private/tmp/nmt-acceptance-24-all.json` | Evidence boundary | Codex `0.147.0`: local installation, discovery, Canon read, reinstall/update, and Consumer cleanliness passed; model prompts were not authenticated. Claude Code `2.1.153`: version only, no authentication or model prompt. |
| Official Plugin validator with temporary PyYAML dependency | PASS | Validator passed without changing repository or user state. |

The package inventory in the passing runs is exactly eight Skills, one physical
Canon at `skills/nmt-chat/references/Next-Move-Theory-Canon/`, six shared
references under `skills/nmt-chat/references/`, and the `1.0.0` manifests. The
Consumer fixture remained byte-for-byte unchanged. The authenticated Codex
direct-probe evidence recorded above on 2026-08-14 remains the evidence for the
eight direct Skills, nmt-chat routing, and the unrelated negative route; the
current no-auth run deliberately records those model probes as an evidence
boundary.

### Remote smoke still required

The exact public command from [`docs/installation.md`](../installation.md)
has been tested against the local checkout with the same flags and isolated
state. It has not been claimed against
`ztemerbekov/Next-Move-Theory-Canon-and-Skills` at a remote commit because the
implementation commits were not pushed. Issue #25 and the parent Wayfinder
map therefore remain open until the owner separately authorizes publication
and the remote command passes the same acceptance matrix.
