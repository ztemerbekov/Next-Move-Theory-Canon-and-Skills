# Plugin updates

Updates refresh the Client-managed Plugin snapshot. They do not edit a cache by
hand, use a package-manager updater, or write into a Consumer project.

## Claude Code

Refresh the marketplace, update the user-scoped Plugin, then start a new Claude
Code session or use the Client's plugin reload boundary:

```bash
claude plugin marketplace update next-move-theory
claude plugin update next-move-theory@next-move-theory --scope user
```

The current session may keep the old loaded snapshot until reload or restart.
The Skills resolve the current Canon through `${CLAUDE_PLUGIN_ROOT}`, so a cache
relocation does not require a path edit.

## Codex

Refresh the configured Git marketplace and reinstall the named Plugin snapshot:

```bash
codex plugin marketplace upgrade next-move-theory
codex plugin add next-move-theory@next-move-theory
```

Start a new Codex task after the reinstall. The current CLI has no separate
`codex plugin update` command; marketplace refresh plus the native `plugin add`
operation is the update path.

## Version rule

The bundle version is declared by the Client manifests and the changelog. A
future release must update the Plugin metadata and the documented validation
evidence together. Do not make a cache-directory edit or install a second
Client-specific Skill tree to work around a version change.

## Legacy boundary

`nmt-upgrade`, `install.sh`, and `install.ps1` refresh the old project-mutating
layout. They are not Plugin update commands. Their behavior and the explicit
no-migration boundary are documented in
[`legacy-installer.md`](legacy-installer.md) and [`migration.md`](migration.md).
