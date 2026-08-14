# Versioning, updates, and Legacy installer contract

Date: 2026-08-14

Wayfinder ticket: [#9 — Choose versioning, updates, and Legacy installer migration](https://github.com/ztemerbekov/Next-Move-Theory-Canon-and-Skills/issues/9)

## Decision

Release the self-contained Plugin as `1.0.0`.

One release version identifies the complete installed distribution:

- both Client manifests;
- all eight unchanged NMT Skill workflows;
- the bundled `Next-Move-Theory-Canon/` snapshot;
- shared references and Client adapters;
- validation and installation documentation.

The Canon does not have an independently installable package version. Its existing methodology maturity labels remain Canon content, not a second updater or release stream. The exact Canon tree bundled in Plugin `1.0.0` is the Canon for that release.

Every cache-bearing manifest and release record must say `1.0.0`. Static validation fails if the Codex manifest, Claude manifest, or top `CHANGELOG.md` release disagree. A packaged-file inventory or tree digest proves that the installed Canon is the one shipped by that Plugin release; users do not maintain a second Canon version.

## Strict Skill boundary

This decision does not authorize changing the behavior or naming of any Skill.

- Keep the name `nmt-upgrade`.
- Do not rewrite its workflow, commands, inputs, outputs, or completion behavior.
- Do not introduce `nmt-update`, an npm package, an `npx` command, or a replacement update Skill.
- Do not use this ticket to justify changes inside any other Skill.

The only later Skill-file edits permitted by already closed decisions are the previously allowlisted mechanical packaging changes needed for relocation-safe paths, portable frontmatter, and Client adapter pointers. They may not alter workflow semantics.

Because the existing `nmt-upgrade` workflow invokes the project-mutating installers, it remains part of the Legacy path in `1.0.0`. It is not redefined as the updater for a globally installed Plugin.

## Global Plugin installation and updates

Treat the global Plugin as a fresh installation. There is no conversion from an existing project-local NMT setup.

The primary installation and update documentation uses each Client's own Plugin management surface, outside the NMT Skills:

### Claude Code

```bash
claude plugin marketplace update next-move-theory
claude plugin update next-move-theory@next-move-theory --scope user
```

The updated Plugin becomes active after `/reload-plugins` or a new Claude Code session. Claude Code keys installed cache copies by the resolved Plugin version and exposes an explicit `plugin update` operation. [Claude Code Plugin reference](https://code.claude.com/docs/en/plugins-reference) and [Plugin discovery and updates](https://code.claude.com/docs/en/discover-plugins).

### Codex

```bash
codex plugin marketplace upgrade next-move-theory
codex plugin add next-move-theory@next-move-theory
```

The refreshed Plugin is used from a new Codex task. The current Codex CLI exposes marketplace refresh and Plugin installation, but no separate `plugin update` subcommand. The installed cache is replaced through the host workflow; documentation must never tell users to edit cache directories directly. [OpenAI Plugin packaging and marketplace documentation](https://developers.openai.com/plugins/build/plugins).

No Plugin update command may write to the Consumer project.

## Update discovery without Skill changes

Do not modify the existing per-Skill update checks.

- A Legacy project-local installation continues to receive `.nmt-version` from `install.sh` or `install.ps1`, exactly as it does now.
- A fresh global Plugin installation writes no `.nmt-version` into the Consumer project.
- The unchanged Skill check is already silent when `.nmt-version` is absent, so it remains silent in the global path.
- Global update discovery therefore belongs to the Client marketplace/Plugin UI, release documentation, and the explicit host-native commands above.

This preserves current Skill behavior while removing Consumer-project mutation from the primary installation model.

## Legacy installer contract for `1.0.0`

`install.sh` and `install.ps1` remain available for the `1.0.0` transition release with their existing project-mutating behavior.

- They are labeled Legacy and are not the primary installation path.
- They may continue copying Canon, Skills, `.nmt-version`, the renamed README, and marked instruction blocks into a project.
- They do not install the global Plugin.
- They do not detect, migrate, reconcile, clean, or delete an existing project-local installation.
- They do not remove user files or remove NMT residue from a Consumer project.
- The global Plugin documentation treats every global install as new, even when unrelated Legacy files happen to exist in a project.

No migration utility, cleanup command, compatibility alias, or migration ticket is created. Post-`1.0.0` handling of old project-local installations is outside this Destination.

## Validation consequences

The repository migration and acceptance contracts must prove:

1. all release-version declarations equal `1.0.0`;
2. the bundled Canon inventory is present in the installed `1.0.0` Plugin;
3. host-native update/reinstall commands refresh the installed cache without a Consumer-project delta;
4. a new task/session loads the refreshed Plugin version;
5. `nmt-upgrade` keeps its existing name and workflow;
6. Legacy installers remain isolated from the primary global installation documentation;
7. no migration or cleanup behavior is implemented.

## Remaining scope

No new in-scope Fog emerges from this decision. Ticket #10 defines clean-environment acceptance details, and ticket #12 turns all closed contracts into the exact repository migration specification.
