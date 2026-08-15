# Migration boundary

The `1.0.0` distribution is a fresh user-global suite. It does not migrate an
existing project-local Legacy setup.

The supported install and update command is:

```bash
npx skills@latest add ztemerbekov/Next-Move-Theory-Canon-and-Skills --skill '*' -a codex -a claude-code -g -y
```

It changes Client user state only. It does not scan, copy, reconcile, rewrite,
or delete `AGENTS.md`, `CLAUDE.md`, `.agents/`, `.claude/`, a project-local
Canon, project-local Skills, or `.nmt-version` in a Consumer project.

There is no migration command, cleanup pass, compatibility merge, or promise
that two installations will be reconciled. Leave an existing Legacy layout in
place until its owner chooses a separate manual cleanup. The unchanged
`nmt-upgrade` workflow remains Legacy-only for that existing project-local
layout and is not a global suite updater.

For the package-level source tree and acceptance evidence, see the
[repository migration specification](repository-migration-specification.md)
and [migration checks](migration/).
