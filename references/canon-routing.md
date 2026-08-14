# Bundled Canon routing

The Plugin always carries one Canon at the exact root path
`Next-Move-Theory-Canon/`. Load the relevant Canon file before answering a
methodology question.

## Client anchors

| Client | Installed-Canon anchor |
| --- | --- |
| Claude Code | `${CLAUDE_PLUGIN_ROOT}/Next-Move-Theory-Canon/` |
| Codex | `../../Next-Move-Theory-Canon/` from a Skill under `skills/<name>/` |
| Legacy project-local setup | `Next-Move-Theory-Canon/` in the Consumer project |

Use the first two anchors for the Plugin. They survive user-global cache
relocation; checkout paths and literal cache-version paths do not. The Legacy
anchor belongs only to `nmt-upgrade` and the transition installers.

## Routing rule

Choose the Canon file from the routing table in the agent-facing source or the
relevant Skill, then read that file in the Client anchor above. The Canon is
progressively disclosed: load only the cluster needed for the current branch,
and return to `ajtbd-key-theses.md` or `nmt-key-theses.md` when the task spans
multiple pillars.
