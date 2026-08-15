# Static package validation

Wayfinder ticket [#19 — Add static package, path, version, and semantic-parity validation](https://github.com/ztemerbekov/Next-Move-Theory-Canon-and-Skills/issues/19)
is implemented by one read-only command:

```bash
python3 scripts/check_static_validation.py
```

The command uses only the Python 3 standard library and the checked-in
repository scripts. It returns `0` only when every gate passes and returns
`1` when any gate fails. It does not authenticate either Client, edit the
checkout, write a Consumer project, touch user state, or modify a cache.

## What the command checks

It runs the focused validators and public-distribution checks in a fixed order,
then checks the package contract directly:

1. JSON manifest and marketplace shape, shared Plugin identity, and the
   `1.0.0` agreement across both manifests, the locked specification, and the
   changelog;
2. the exact bundled Canon inventory under
   `skills/nmt-chat/references/Next-Move-Theory-Canon/`, no duplicate Canon
   root, exactly eight Skill directories, and every `SKILL.md` entry point;
3. portable Skill frontmatter, including rejection of `user-invocable`, and
   resolution of every Plugin-relative Canon/reference pointer;
4. the adapter/source/package drift gate; and
5. semantic parity against the preserved Claude baseline after only the
   explicit mechanical allowlist. Unexpected Skill content is reported with
   a unified diff containing file and line context.
6. the exact user-global `skills` CLI command, NOTICE attribution, removed
   Legacy artifacts, removed installer commands, and resolving local links in
   the active public documentation.

The command also runs two isolated, temporary negative fixtures. One adds a
nested `Next-Move-Theory-Canon/` directory; the other adds
`user-invocable: true` to a Skill frontmatter block. The suite passes only when
both known failures are rejected. The fixtures are removed automatically and
never touch the repository source.

The existing focused commands remain useful when diagnosing one gate:

```bash
python3 scripts/check_plugin_manifests.py
python3 scripts/verify-source-consolidation.py
python3 scripts/check_adapter_drift.py
```
