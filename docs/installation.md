# Global Plugin installation

The primary distribution is one user-global `next-move-theory` Plugin, version
`1.0.0`. The repository root is both the Plugin root and its marketplace root.
The Plugin bundles the exact `Next-Move-Theory-Canon/` directory and one
`skills/` tree containing all eight Skills.

## Install

Use the installer command for your platform:

macOS, Linux, and other Unix-like systems:

```bash
npx install latest
```

Windows PowerShell:

```powershell
irm https://nextmovetheory.com/install.ps1 | iex
```

## After installation

Start with `nmt-chat`. It is the model-invoked router: describe the product
question in ordinary language and let it route to the appropriate Skill. Direct
Skill invocation is still available through each Client's Plugin surface, with
the Client's own namespace or invocation marker if it displays one.

The user-global Plugin install changes Client user state only. It does not add
or modify `AGENTS.md`, `CLAUDE.md`, `.agents/`, `.claude/`,
`Next-Move-Theory-Canon/`, or a Skill directory in the Consumer project. A
Consumer project may be changed later when a user explicitly asks a Skill to
perform work; that is runtime work, not installation residue.

## Verify the package before distribution

From a repository checkout, maintainers can run the local checks without
authenticating Claude Code:

```bash
python3 scripts/check_plugin_manifests.py
python3 /Users/ztemerbekov/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py .
claude plugin validate . --strict
```

Clean-environment installation, Skill invocation, update, and Consumer
cleanliness checks are maintained by the acceptance harness. They run in an
isolated user state and do not use Consumer-project files as installation
inputs.

## Migration boundary

There is no automatic migration in this release. Existing project-local Legacy
files are neither scanned nor reconciled by the Plugin install. See
[`migration.md`](migration.md) before moving an existing setup.
