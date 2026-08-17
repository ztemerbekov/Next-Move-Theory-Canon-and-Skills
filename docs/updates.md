# Suite updates

The supported update path is to repeat the same `skills` CLI command used for
installation. It refreshes the complete eight-Skill suite for Codex and Claude
Code and preserves the user-global boundary:

```bash
npx skills@latest add ztemerbekov/Next-Move-Theory-Canon-and-Skills --skill '*' -a codex -a claude-code -g -y
```

The `--skill '*'` selection is intentional. Partial updates are unsupported
because the shared Canon and routing references are carried by the `nmt-chat`
payload. The CLI may use a copy or symlink in Client user state; do not edit a
cache directory by hand and do not copy the suite into a Consumer project.

After the command completes, start a new Codex task or Claude Code session so
the Client loads the refreshed snapshot. Verify that `nmt-chat` can reach the
bundled Canon and route to the other Skills.

## Legacy boundary

`nmt-upgrade` is unchanged Legacy-only behavior for existing project-local
setups. It is not the supported global updater, and this repository no longer
ships the old `install.sh` or `install.ps1` scripts. No migration, cleanup, or
reconciliation is performed by a suite update.

## Version requests and telemetry

Founder-hosted version requests and any separate telemetry collected by the
`skills` CLI are unchanged by this repository packaging work. The Skills do
not gain new telemetry or behavior as part of installation or update.
