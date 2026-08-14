# Legacy installer

`install.sh`, `install.ps1`, and the bundled `nmt-upgrade` Skill are retained for
one transition release. They are the old project-local path, not the
user-global `next-move-theory` Plugin installer.

## What the Legacy path does

When explicitly run from the Legacy transition source for a Consumer project,
the shell and PowerShell scripts:

1. clone or use a checkout of this repository;
2. replace the Consumer's `Next-Move-Theory-Canon/` directory;
3. copy the Legacy Claude and Codex Skill inputs into
   `.claude/skills/` and `.agents/skills/`;
4. inject the repository's `CLAUDE.md` and `AGENTS.md` between the existing
   `Next-Move-Theory-Rules` markers; and
5. copy the README as `NextMoveTheory-README.md` and record `.nmt-version`.

The scripts preserve unrelated Skills, but they are intentionally
project-mutating and can replace the existing Canon. Review the target and
record a backup before running them.

They retain the old `Skills/claude/` and `Skills/codex/` input contract. They
are documented here for the transition release and must not be treated as an
installer for the consolidated repository-root Plugin.

## Commands

macOS / Linux:

```bash
curl -fsSL https://nextmovetheory.com/install.sh | bash
```

Or, from a Legacy checkout:

```bash
bash install.sh --target /path/to/consumer-project
```

Windows / PowerShell:

```powershell
irm https://nextmovetheory.com/install.ps1 | iex
```

Or:

```powershell
powershell -ExecutionPolicy Bypass -File install.ps1 -Target C:\path\to\consumer-project
```

`nmt-upgrade` re-runs the same official installer from a project root. It is
not a Plugin marketplace update and does not update a user-global Plugin.

## Transition and no-migration boundary

Use this path only when the project-local Legacy layout is intentionally being
refreshed. It is retained for one transition release and is not the default
installation described in [`installation.md`](installation.md). It does not
perform migration, cleanup, reconciliation, or automatic removal of old
Consumer files. For the explicit boundary and a fresh Plugin adoption path,
read [`migration.md`](migration.md).
