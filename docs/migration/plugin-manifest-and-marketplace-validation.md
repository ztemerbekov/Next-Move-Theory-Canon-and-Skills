# Plugin manifests and marketplace catalogs

This package metadata implements the locked contract in
[`docs/repository-migration-specification.md`](../repository-migration-specification.md)
and Wayfinder ticket [#15](https://github.com/ztemerbekov/Next-Move-Theory-Canon-and-Skills/issues/15).

## Package metadata

- `.codex-plugin/plugin.json` identifies `next-move-theory` at `1.0.0`, exposes
  the single `./skills/` source tree, and contains only interface metadata.
- `.claude-plugin/plugin.json` identifies the same Plugin and version.
- `.claude-plugin/marketplace.json` points `source: "./"` at this repository
  root and enables strict validation.
- `.agents/plugins/marketplace.json` points at the repository Git URL on
  `main` and uses `AVAILABLE` / `ON_INSTALL` / `Productivity`.

Neither manifest declares Agents, Hooks, MCP servers, or Apps. The marketplace
catalogs do not create a second Skill or Canon tree.

## Focused static check

Run from the repository root:

```bash
python3 scripts/check_plugin_manifests.py
```

The check parses all four JSON files, verifies shared identity and version,
checks the exact eight-Skill inventory and entry points, validates both
marketplace sources and policy blocks, rejects prohibited runtime components,
and rejects a second bundled Canon root outside the `nmt-chat` payload.

## Client validators

The Codex validator is local and does not authenticate:

```bash
python3 /Users/ztemerbekov/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py .
```

Claude's strict validator is also a local manifest check and does not require
Claude account authentication:

```bash
claude plugin validate . --strict
```

Clean-environment installation, Skill invocation, update behavior, and the
runtime evidence boundary for an unavailable Claude session belong to the
later harness ticket; this ticket does not log in to either Client.
