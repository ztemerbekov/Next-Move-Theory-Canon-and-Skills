# Client adapter and source drift validation

This check implements Wayfinder ticket [#18](https://github.com/ztemerbekov/Next-Move-Theory-Canon-and-Skills/issues/18)
and the adapter contract in
[`docs/repository-migration-specification.md`](../repository-migration-specification.md).

## One adapter source

[`references/client-adapters.md`](../../references/client-adapters.md) is the
only hand-authored adapter registry. It contains exactly five proven
boundaries: invocation spelling/namespacing, interactive-question tooling,
executor lifecycle, installed-Canon anchors, and Codex frontmatter validator
compatibility. It explicitly rejects semantic Skill changes as adapters.

The shared Skill source remains one tree under `skills/`. The registry freezes
the reviewed source and shared-reference contents with SHA-256 fingerprints.
That makes a future host-specific wording change fail closed until the source
and its evidence are deliberately reviewed together.

## Check

Run from the repository root:

```bash
python3 scripts/check_adapter_drift.py
```

The check verifies the exact five registry entries and their required fields,
resolves every declared local evidence link, checks the eight-Skill inventory,
rejects a second Client-specific tree, rejects literal checkout/cache anchors,
rejects `user-invocable` metadata, and compares every shared Skill/reference
file with the registry fingerprint inventory.

It fails when a shared source file changes, even if the change appears small:
the registry must be reviewed and updated only with evidence. It also fails
when a declared adapter reference is missing or stale. No Claude account or
runtime is needed.
