# Global installation

The supported distribution is one user-global `next-move-theory` suite
installed with the `skills` CLI. It contains all eight Skills and the bundled
Canon/shared references carried by the `nmt-chat` payload.

## Install

Run this command from any directory:

```bash
npx skills@latest add ztemerbekov/Next-Move-Theory-Canon-and-Skills --skill '*' -a codex -a claude-code -g -y
```

The command is cross-platform: use it from macOS, Linux, or Windows. The
intentional `--skill '*'` installs the complete suite; partial Skill selection
is unsupported because the shared Canon and routing references are packaged
with `nmt-chat`.

## After installation

Start with `nmt-chat`. It is the model-invoked router and conversational front
door to the methodology. The `skills` CLI may materialize the installed suite
as a copy or a symlink in each Client's user-global state; follow the CLI's
reported destination rather than copying files into a project.

The install changes Client user state only. It does not add or modify
`AGENTS.md`, `CLAUDE.md`, `.agents/`, `.claude/`, a Canon directory, or a Skill
directory in the Consumer project. The one physical bundled Canon and shared
reference set are resolved from the installed `nmt-chat` payload.

## Update

Repeat the same command to refresh both supported Client targets:

```bash
npx skills@latest add ztemerbekov/Next-Move-Theory-Canon-and-Skills --skill '*' -a codex -a claude-code -g -y
```

Do not edit a Client cache by hand, install a partial selection, or use an
`nmt-upgrade` command as the global suite updater. `nmt-upgrade` retains its
unchanged Legacy-only behavior for existing project-local setups; it is not
part of the supported global installation or update path.

## Legacy boundary

This release does not ship `install.sh` or `install.ps1`, and it does not
promise migration, cleanup, reconciliation, or removal of an existing
project-local Legacy setup. The supported installation never injects files
into a Consumer project. Any project changes made later by an explicitly
invoked Skill are separate runtime work, not installation residue.

## Verify the package before distribution

From a repository checkout, maintainers can run the local checks without
authenticating either Client:

```bash
python3 scripts/check_plugin_manifests.py
python3 scripts/check_static_validation.py
python3 /Users/ztemerbekov/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py .
```

The clean-environment acceptance harness covers installation, discovery,
Canon access, update behavior, and Consumer cleanliness in isolated state.
