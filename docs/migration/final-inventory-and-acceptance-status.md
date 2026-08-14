# Final inventory and acceptance status

Wayfinder ticket: [#16 — Run acceptance matrix and retire the duplicate Skill source tree](https://github.com/ztemerbekov/Next-Move-Theory-Canon-and-Skills/issues/16)

This file records the implementation inventory and the evidence boundary. It
does not claim Destination until both Client runtime smoke tests have been
observed.

## Repository inventory

- `.codex-plugin/plugin.json` and `.claude-plugin/plugin.json` identify one
  `next-move-theory` Plugin at version `1.0.0`.
- `skills/` is the one editable, hand-maintained Skill source tree and contains
  the eight NMT Skill entry points.
- `Next-Move-Theory-Canon/` is the one bundled Canon root and is available from
  the installed Plugin package.
- `references/` contains the shared routing, methodology, adapter, producer,
  and readability contracts.
- `scripts/` and `docs/` contain static validation, adapter drift, acceptance,
  installation, update, and Legacy-installer instructions.
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
