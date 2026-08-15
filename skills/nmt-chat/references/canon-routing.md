# Bundled Canon routing

The suite always carries one Canon at the exact path
`skills/nmt-chat/references/Next-Move-Theory-Canon/`. Load the relevant Canon
file before answering a methodology question.

## Installed suite anchors

| Skill location | Canon anchor |
| --- | --- |
| `nmt-chat/SKILL.md` | `references/Next-Move-Theory-Canon/` |
| Any other installed `nmt-*` Skill | `../nmt-chat/references/Next-Move-Theory-Canon/` |

These sibling-relative anchors survive user-global copy and symlink
installation, as well as Plugin cache relocation. Checkout paths and literal
cache-version paths do not. The Consumer-project
`Next-Move-Theory-Canon/` anchor belongs only to the historical `nmt-upgrade`
workflow and is not part of the supported suite installation.

## Routing rule

Choose the Canon file from the routing table in the agent-facing source or the
relevant Skill, then read that file in the Client anchor above. The Canon is
progressively disclosed: load only the cluster needed for the current branch,
and return to `ajtbd-key-theses.md` or `nmt-key-theses.md` when the task spans
multiple pillars.
