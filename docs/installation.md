# Global installation

The supported distribution is a user-global `next-move-theory` Skill suite
installed with the `skills` CLI into Codex and Claude Code. It contains all
seven Skills and the bundled Canon/shared contracts carried by the `nmt-chat`
payload. This command installs the Skills directly; it does not consume the
repository's native Plugin manifests.

## Install

Run this command from any directory:

```bash
npx skills@latest add ztemerbekov/Next-Move-Theory-Canon-and-Skills --skill '*' -a codex -a claude-code -g -y
```

The command is cross-platform: use it from macOS, Linux, or Windows. The
intentional `--skill '*'` installs the complete suite; partial Skill selection
is unsupported because the shared Canon and contracts are packaged with
`nmt-chat`.

## After installation

Start with `nmt-chat`. It is the model-invoked router and conversational front
door to the methodology. The `skills` CLI may materialize the installed suite
as a copy or a symlink in each Client's user-global state; follow the CLI's
reported destinations rather than copying files into a project.

The install changes Client user state only. It does not add or modify
`AGENTS.md`, `CLAUDE.md`, `.agents/`, `.claude/`, a Canon directory, or a Skill
directory in the Consumer project. Within each Client target, the bundled Canon
and shared contracts resolve from the installed `nmt-chat` payload.

## Update

Repeat the same command to refresh both supported Client targets:

```bash
npx skills@latest add ztemerbekov/Next-Move-Theory-Canon-and-Skills --skill '*' -a codex -a claude-code -g -y
```

Do not edit a Client cache by hand or install a partial selection.

After the command completes, start a new Codex task or Claude Code session so
the Client loads the refreshed snapshot. Verify that `nmt-chat` can reach the
bundled Canon and route to the other Skills.

Installation and update never scan, rewrite, or delete files in the Consumer
project. Any project changes made later by an explicitly invoked Skill are
separate runtime work, not installation residue.
