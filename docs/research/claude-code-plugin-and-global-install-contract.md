# Claude Code plugin and global-install contract

Research date: 2026-08-14

Question: what do current first-party Claude Code sources require or recommend for a self-contained plugin that bundles multiple Skills and the Next Move Theory canon, installs for one user across local projects, and leaves the consumer repository untouched?

Labels used below:

- **Requirement** — stated directly by current Anthropic documentation or enforced by Claude Code's documented schema/loader behavior.
- **Official recommendation** — Anthropic documents this as the preferred approach, but the runtime permits alternatives.
- **Inference for this repository** — a design conclusion derived from the documented behavior, not a rule stated by Anthropic.

## Conclusion

Claude Code can support the requested installation contract without writing anything into a consumer repository. The repository can be both the plugin and its marketplace: put `plugin.json` and `marketplace.json` in the root `.claude-plugin/` directory, keep all Skills in one root `skills/` tree, keep the whole canon inside the same plugin root, and list the plugin in the marketplace with `"source": "./"`. A user then adds the GitHub repository as a marketplace and installs the plugin at explicit `user` scope. User-scope plugin configuration lives in `~/.claude/settings.json`, marketplace state lives under `~/.claude/plugins`, and the installed plugin is copied to `~/.claude/plugins/cache`; project-scope files are not part of this path. This conclusion follows from Claude Code's documented [configuration scopes](https://code.claude.com/docs/en/settings), [plugin installation scopes and cache behavior](https://code.claude.com/docs/en/plugins-reference), and [marketplace source rules](https://code.claude.com/docs/en/plugin-marketplaces).

Two boundaries matter:

1. Claude Code calls this **user scope**, not “global installation.” It is global across this user's local Claude Code projects, but user-scoped plugins do not automatically transfer to Claude Code cloud or Cowork sessions. Anthropic documents that boundary in [Skills in Cowork and cloud sessions](https://code.claude.com/docs/en/skills#skills-in-cowork-and-cloud-sessions).
2. Bundling canon files does not make them context automatically. A plugin-root `CLAUDE.md` is explicitly not loaded. The Skills must route Claude to the relevant bundled canon files; the documented relocation-safe anchor is `${CLAUDE_PLUGIN_ROOT}`. See the [plugin directory structure and environment-variable rules](https://code.claude.com/docs/en/plugins-reference#plugin-directory-structure).

## Repository layout

### Direct contract

- **Requirement:** plugin components use directories at the plugin root. New Skills use `skills/<skill-name>/SKILL.md`. `skills/`, `commands/`, `agents/`, and `hooks/` do not belong inside `.claude-plugin/`; only plugin metadata belongs there. Claude Code auto-discovers the default `skills/` location. [Plugins reference: directory structure](https://code.claude.com/docs/en/plugins-reference#plugin-directory-structure)
- **Requirement:** a marketplace hosted as a repository has `.claude-plugin/marketplace.json` at the marketplace root. Its top-level required fields are `name`, `owner`, and `plugins`; each plugin entry requires `name` and `source`. [Marketplace schema](https://code.claude.com/docs/en/plugin-marketplaces#marketplace-schema)
- **Requirement:** a relative marketplace plugin source starts with `./` and resolves from the marketplace root, not from `.claude-plugin/`. The current docs explicitly support a marketplace-root plugin using `"source": "./"`. [Relative plugin sources](https://code.claude.com/docs/en/plugin-marketplaces#relative-paths) and [marketplace-root source behavior](https://code.claude.com/docs/en/plugin-marketplaces#advanced-plugin-entries)
- **Requirement:** every file needed at runtime must be inside the copied plugin directory. Marketplace-installed plugins are copied to the user's cache; paths such as `../shared-utils` outside that directory are unavailable after installation. Symlinks outside the marketplace are skipped. [Plugin caching and file resolution](https://code.claude.com/docs/en/plugins-reference#plugin-caching-and-file-resolution)
- **Official recommendation:** host the marketplace in GitHub and distribute it with the `owner/repo` shorthand. [Host on GitHub](https://code.claude.com/docs/en/plugin-marketplaces#host-on-github-recommended)

### Recommended repository shape

**Inference for this repository:** make the existing repository root the plugin root as well as the marketplace root. That keeps one copy of every Skill and every canon file and requires no generated Claude-specific tree.

```text
Next-Move-Theory-Canon-and-Skills/
├── .claude-plugin/
│   ├── plugin.json
│   └── marketplace.json
├── skills/
│   ├── <skill-a>/
│   │   ├── SKILL.md
│   │   └── ... optional supporting files
│   └── <skill-b>/
│       └── SKILL.md
├── Advanced-Jobs-To-Be-Done/      # bundled canon; existing names may stay
├── ABCDX-Segmentation/
├── Next-Move-Theory/
├── Riskiest-Assumption-Test/
├── Algorithms/
├── HowTos/
├── README.md
└── LICENSE
```

Claude Code imposes no special name such as `canon/`; it only requires the referenced files to remain inside the plugin root. Keeping the canon's existing directories avoids a needless path migration.

## Plugin manifest

Claude Code can technically auto-discover a manifestless plugin in default component locations. If a manifest is present, `name` is its only required field. The official plugin tutorial nevertheless creates `.claude-plugin/plugin.json` for a distributable plugin, and a marketplace's default `strict: true` mode treats `plugin.json` as the component authority. See the [plugin manifest schema](https://code.claude.com/docs/en/plugins-reference#plugin-manifest-schema) and [marketplace strict mode](https://code.claude.com/docs/en/plugin-marketplaces#strict-mode).

**Inference for this repository:** require a manifest even though the bare loader does not. It gives the plugin a stable identity, namespace, metadata source, and explicit version policy.

Suggested shape:

```json
{
  "$schema": "https://json.schemastore.org/claude-code-plugin-manifest.json",
  "name": "next-move-theory",
  "displayName": "Next Move Theory",
  "description": "Advanced Jobs To Be Done and Next Move Theory canon and agent skills",
  "repository": "https://github.com/<owner>/Next-Move-Theory-Canon-and-Skills",
  "license": "CC-BY-NC-SA-4.0",
  "keywords": ["ajtbd", "jobs-to-be-done", "product-strategy"]
}
```

Manifest rules relevant here:

- **Requirement:** `name` is a kebab-case identifier and becomes the plugin namespace. A plugin named `next-move-theory` exposes Skills as `/next-move-theory:<skill-name>`. [Plugin manifest required fields](https://code.claude.com/docs/en/plugins-reference#required-fields) and [Skill locations/namespacing](https://code.claude.com/docs/en/skills#where-skills-live)
- **Requirement:** if custom component paths are ever added, manifest paths are relative to the plugin root and normally begin with `./`. The default `skills/` directory is scanned automatically, so this repository does not need a `skills` field merely to point at `./skills`. [Component path fields](https://code.claude.com/docs/en/plugins-reference#component-path-fields)
- **Official recommendation:** include discoverability metadata and use `skills/` rather than the legacy flat `commands/` form for new plugins. [Create plugins](https://code.claude.com/docs/en/plugins)
- **Inference for this repository:** use the same stable `name` in `plugin.json` and the marketplace entry. Claude Code permits a different marketplace entry name, but then the marketplace name wins in user settings and `/plugin`, creating an unnecessary second identity.

## Marketplace manifest

Suggested root `.claude-plugin/marketplace.json`:

```json
{
  "$schema": "https://json.schemastore.org/claude-code-marketplace.json",
  "name": "next-move-theory",
  "description": "Next Move Theory plugins",
  "owner": {
    "name": "Next Move Theory"
  },
  "plugins": [
    {
      "name": "next-move-theory",
      "source": "./",
      "description": "Advanced Jobs To Be Done and Next Move Theory canon and agent skills",
      "strict": true
    }
  ]
}
```

- **Requirement:** the marketplace name must not collide with Anthropic's reserved marketplace names. `next-move-theory` is not in the current reserved list. [Marketplace required fields and reserved names](https://code.claude.com/docs/en/plugin-marketplaces#required-fields)
- **Requirement:** `source: "./"` means the repository root is copied as the plugin. The Skills and canon therefore travel together into the versioned cache. [Plugin sources](https://code.claude.com/docs/en/plugin-marketplaces#plugin-sources)
- **Inference for this repository:** keep component definitions in `plugin.json` and let the marketplace entry contain source plus catalog metadata. Explicit `strict: true` documents the single authority; it is also the default. Do not repeat `skills`, hooks, or other component paths in both files.
- **Inference for this repository:** do not use a direct-URL marketplace for this layout. Claude Code downloads only `marketplace.json` for a direct URL, so relative plugin sources cannot resolve; the GitHub repository marketplace does fetch the repository. [Relative path limitation](https://code.claude.com/docs/en/plugin-marketplaces#relative-paths)

## User-scoped installation and filesystem effects

Use the non-interactive CLI so the scope is explicit:

```bash
claude plugin marketplace add <owner>/Next-Move-Theory-Canon-and-Skills --scope user
claude plugin install next-move-theory@next-move-theory --scope user
```

The equivalent in-session forms are:

```text
/plugin marketplace add <owner>/Next-Move-Theory-Canon-and-Skills
/plugin install next-move-theory@next-move-theory
```

The shell commands default to `user` scope, but an explicit flag makes the clean-install contract auditable. The documented state locations are:

| State | User-scope location | Status |
| --- | --- | --- |
| Plugin enablement | `~/.claude/settings.json` | **Requirement**; this is the plugin settings file for user scope. |
| Marketplace registry | `~/.claude/plugins/known_marketplaces.json` | **Requirement**; marketplace state is stored once per user. |
| Installed plugin files | `~/.claude/plugins/cache/<marketplace>/<plugin>/<resolved-version>/...` | **Requirement**; marketplace plugins are copied into the versioned user cache. |
| Consumer repository | no install file | **Inference** from the three documented user-scope destinations. |

Sources: [configuration scopes](https://code.claude.com/docs/en/settings#configuration-scopes), [plugin installation scopes](https://code.claude.com/docs/en/plugins-reference#plugin-installation-scopes), and [plugin caching](https://code.claude.com/docs/en/plugins-reference#plugin-caching-and-file-resolution).

**Inference for this repository:** installation can leave a consumer repository byte-for-byte untouched if both marketplace registration and plugin installation use `--scope user`, and the plugin itself has no install hook or command that writes to `${CLAUDE_PROJECT_DIR}`. By contrast, `--scope project` intentionally writes `.claude/settings.json`, and `--scope local` writes `.claude/settings.local.json`; neither belongs in the desired path.

This guarantee covers installation and enablement. A Skill may still edit a project later when the user asks it to perform product work; that is normal runtime behavior, not installation residue.

## Skill discovery and canon references

- **Requirement:** multiple plugin Skills live at `<plugin-root>/skills/<skill-name>/SKILL.md` and are auto-discovered when the plugin is installed. They are namespaced by the plugin name. [Plugin Skills](https://code.claude.com/docs/en/plugins-reference#skills)
- **Requirement:** `SKILL.md` is the entry point. Claude Code says all frontmatter fields are technically optional, while `description` is recommended because it controls model invocation; `name` defaults to the directory name. [Skill frontmatter](https://code.claude.com/docs/en/skills#frontmatter-reference)
- **Requirement:** a plugin-root `CLAUDE.md` is not loaded. Plugin context must arrive through Skills, agents, or hooks. Simply moving the currently injected methodology block to a root `CLAUDE.md` would not work. [Plugin directory structure](https://code.claude.com/docs/en/plugins-reference#plugin-directory-structure)
- **Requirement:** `${CLAUDE_PLUGIN_ROOT}` expands anywhere in Skill content to the current absolute installed plugin directory. That directory changes when a plugin updates and must be treated as ephemeral. [Plugin environment variables](https://code.claude.com/docs/en/plugins-reference#environment-variables)
- **Official recommendation:** keep detailed references outside the main `SKILL.md` and link them with a description of when to load them. Anthropic's Skill guide shows relative Markdown links for supporting files in the Skill directory and recommends keeping `SKILL.md` below 500 lines. [Add supporting files](https://code.claude.com/docs/en/skills#add-supporting-files)

**Inference for this repository:** references to canon files outside an individual Skill directory should use the documented plugin-root variable, for example:

```markdown
When the task concerns segmentation, read
`${CLAUDE_PLUGIN_ROOT}/Advanced-Jobs-To-Be-Done/segmentation.md`
before answering.
```

This is safer than hard-coded checkout paths or paths into `~/.claude/plugins/cache`, both of which break when another user installs the plugin or the resolved version changes. Relative Markdown links are documented for files beside `SKILL.md`; the official docs do not explicitly promise a general resolution contract for `../../...` links from a Skill into arbitrary sibling canon trees. `${CLAUDE_PLUGIN_ROOT}` is the explicit cross-plugin-root contract.

## Versioning, updates, and relocation

Claude Code uses the resolved plugin version as both an update signal and a cache key. The resolution order is: `plugin.json` version, marketplace-entry version, git commit SHA for git and git-hosted relative sources, archive digest, then `unknown` for sources without another version. [Version management](https://code.claude.com/docs/en/plugins-reference#version-management)

There are two valid policies:

1. **Published releases:** put one SemVer value in `plugin.json`, omit it from `marketplace.json`, and bump it for every release. If commits change without a bump, installed users stay on the old cached version. Anthropic recommends semantic versioning for this mode.
2. **Active development:** omit `version` from both manifests. For this git-hosted relative source, the resolved commit SHA becomes the version, so every new source commit can be installed as an update.

**Inference for this repository:** use commit-SHA versioning while the fork is being reorganized; introduce an explicit `plugin.json` SemVer when a stable installable release is intentionally cut. Never duplicate version in both manifests.

Manual update flow:

```bash
claude plugin marketplace update next-move-theory
claude plugin update next-move-theory@next-move-theory --scope user
```

Third-party marketplaces have background auto-update disabled by default; users can enable it in `/plugin` under Marketplaces. When auto-update is enabled, Claude Code updates files on disk after session startup, while the current session keeps the version it loaded until `/reload-plugins` or the next launch. [Configure auto-updates](https://code.claude.com/docs/en/discover-plugins#configure-auto-updates)

Old cached versions remain temporarily so concurrent sessions continue working and are later swept. Consequently, Skills must resolve canon through the current `${CLAUDE_PLUGIN_ROOT}` and must not write state into the plugin directory. [Plugin caching](https://code.claude.com/docs/en/plugins-reference#plugin-caching-and-file-resolution)

## Validation and clean-install proof

### Static and local validation

```bash
claude --version
claude plugin validate . --strict
claude --plugin-dir .
```

- **Requirement:** `claude plugin validate .` checks the marketplace schema. For local-path entries it also validates the plugin manifest; validating the plugin directory checks Skill frontmatter and component files. `--strict` turns warnings into errors and is recommended for CI. [Marketplace validation](https://code.claude.com/docs/en/plugin-marketplaces#validation-and-testing) and [strict plugin validation](https://code.claude.com/docs/en/plugins-reference#unrecognized-fields)
- **Official recommendation:** use `claude --plugin-dir .` for direct development testing, then invoke the namespaced Skills and inspect component loading. [Test plugins locally](https://code.claude.com/docs/en/plugins#test-your-plugins-locally)
- **Requirement:** `claude --debug` exposes plugin load errors and Skill registration. `claude plugin details next-move-theory@next-move-theory` lists the component inventory and context cost. [Debugging](https://code.claude.com/docs/en/plugins-reference#debugging-and-development-tools) and [plugin details](https://code.claude.com/docs/en/plugins-reference#plugin-details)

### Acceptance checks for the desired contract

**Inference for this repository:** a clean-environment test is complete only when all of these hold:

1. Start in a disposable initialized Git repository with no `.claude/`, `CLAUDE.md`, copied canon, or installer residue.
2. Record its file tree and `git status --porcelain`.
3. Add the hosted marketplace and install the plugin with explicit `--scope user`.
4. Confirm `claude plugin list` and `claude plugin details next-move-theory@next-move-theory` show the plugin and every expected Skill.
5. Start Claude Code in the disposable repository, invoke at least one namespaced Skill, and make it read a canon file through `${CLAUDE_PLUGIN_ROOT}`.
6. Confirm the disposable repository's file tree and `git status --porcelain` are unchanged.
7. Update to a changed commit/version, reload plugins, and repeat the canon-read check to prove references survive cache relocation.
8. Run the same test on every supported operating system. On Windows, `~/.claude` resolves to `%USERPROFILE%\.claude`. [Claude Code settings](https://code.claude.com/docs/en/settings#configuration-scopes)

## Residual uncertainty to prove rather than assume

- Anthropic explicitly documents relative Markdown links for supporting files inside a Skill directory, but does not explicitly specify how arbitrary `../../...` Markdown links from `SKILL.md` into sibling canon trees are resolved. The contract therefore uses `${CLAUDE_PLUGIN_ROOT}` and the clean-install test must exercise an actual canon read after installation and after an update.
- The docs place every user-scope installation artifact under `~/.claude`, so “no consumer-repository write” is a strong inference, not a quoted blanket guarantee from Anthropic. The before/after repository snapshot is the acceptance proof.
- User-scope plugins apply to local Claude Code sessions. Cloud and Cowork availability has a different distribution mechanism and is outside this installation contract.

## Decisions this evidence supports

- One repository can legally be one self-contained Claude Code plugin and one marketplace; it does not need a separate Claude-specific copy of the Skills.
- The canon must be inside the plugin root copied by `source: "./"`.
- The stable runtime path from Skills to canon is `${CLAUDE_PLUGIN_ROOT}/...`.
- User-scoped installation can leave the consumer repository untouched.
- A project-local bootstrap may remain a separate opt-in workflow, but it is not needed for normal Claude Code installation.
- The plugin's Skill namespace is necessarily `next-move-theory:` under the proposed name; unnamespaced commands belong to standalone personal/project Skills, not marketplace plugins.
- “Global” should be documented as “user scope across local projects,” with the cloud/Cowork limitation stated explicitly.

## First-party sources consulted

- Anthropic, [Create plugins](https://code.claude.com/docs/en/plugins)
- Anthropic, [Plugins reference](https://code.claude.com/docs/en/plugins-reference)
- Anthropic, [Create and distribute a plugin marketplace](https://code.claude.com/docs/en/plugin-marketplaces)
- Anthropic, [Discover and install prebuilt plugins](https://code.claude.com/docs/en/discover-plugins)
- Anthropic, [Extend Claude with Skills](https://code.claude.com/docs/en/skills)
- Anthropic, [Claude Code settings](https://code.claude.com/docs/en/settings)
- Anthropic, [official Claude Code demo marketplace manifest](https://github.com/anthropics/claude-code/blob/main/.claude-plugin/marketplace.json)
