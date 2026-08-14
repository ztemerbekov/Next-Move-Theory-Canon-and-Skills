# Codex plugin and global-install contract

Research date: 2026-08-14

Question: what do current first-party Codex sources require or recommend for a self-contained plugin that bundles multiple Skills and the Next Move Theory canon, installs for one user across projects, and leaves the consumer repository untouched?

Labels used below:

- **Official requirement** — stated by current OpenAI documentation or enforced by the published package/submission contract.
- **Bundled tooling convention** — behavior prescribed by the OpenAI-bundled `plugin-creator` / `skill-creator` skills or by the installed Codex CLI, but not stated as the only valid public package shape.
- **Inference for this repository** — a design conclusion derived from those sources and requiring an installed-copy test where noted.

## Conclusion

Codex supports the requested contract. A plugin can live at this repository's root, contain one shared `skills/` tree and the full canon, and expose itself through a repo marketplace. A user can add the Git repository as a marketplace and install the plugin into Codex's user-level state. Installed plugin files are copied under `~/.codex/plugins/cache/...`, enablement is stored under `~/.codex/config.toml`, and no install step needs to write to the consumer repository. OpenAI explicitly positions plugins, rather than repo-local Skill folders, as the distribution mechanism for reusable Skills beyond one repository. Sources: [package a plugin](https://developers.openai.com/plugins/build/plugins), [build Skills](https://learn.chatgpt.com/docs/build-skills), and [use plugins](https://learn.chatgpt.com/docs/plugins).

The practical install path is:

```bash
codex plugin marketplace add <owner>/<repository> --ref main
codex plugin add next-move-theory@next-move-theory
```

The second command is confirmed by the installed `codex-cli 0.144.5` help and by the bundled `plugin-creator` update guide. The interactive equivalent is to run `/plugins`, install `next-move-theory` from its marketplace, and then start a new session. OpenAI documents that newly installed plugin Skills and tools are picked up by a new Codex session. [Plugins in Codex CLI](https://learn.chatgpt.com/docs/plugins#plugin-browser-in-codex-cli)

One boundary remains deliberately explicit: public OpenAI docs require authors to verify that bundled files and references resolve after installation, but do not define a general Markdown-link resolution rule for a Skill that reaches from `skills/<name>/SKILL.md` into a shared top-level canon directory. Keeping the Canon in the same plugin archive and referring to it with relocation-safe paths is a strong inference, not a quoted public guarantee; it must be proven against the installed cache copy. [Complete-plugin test checklist](https://developers.openai.com/plugins/deploy/connect-chatgpt#test-the-complete-plugin)

## Source hierarchy and an important discrepancy

This report uses three first-party source layers:

1. Current public OpenAI documentation on `developers.openai.com` and `learn.chatgpt.com` — authoritative for the package, marketplace, install, and submission contracts.
2. Current local Codex CLI help (`codex-cli 0.144.5`) — authoritative for the commands available in this environment.
3. OpenAI-bundled local skills and scripts under `$CODEX_HOME/skills/.system/plugin-creator/` and `$CODEX_HOME/skills/.system/skill-creator/` — useful implementation conventions and preflight tooling.

They are not perfectly identical:

- Public docs show a minimal local manifest with `name`, `version`, `description`, and `skills`, while the public package/submission checks also require `author.name` and the core `interface` listing fields for a submission-grade archive. [Minimal local plugin](https://developers.openai.com/plugins/build/plugins#create-a-plugin-manually) and [plugin manifest errors](https://developers.openai.com/plugins/deploy/submission-errors#plugin-manifest-errors)
- Public docs support a `hooks` manifest field. The bundled `plugin-creator/scripts/validate_plugin.py` snapshot rejects `hooks` as an unsupported top-level field, and the bundled creator tells authors to omit it. [Public path and hook rules](https://developers.openai.com/plugins/build/plugins#path-rules)
- Public docs say a local plugin can be refreshed by updating the source directory and restarting the desktop app. The bundled creator prescribes a deterministic cachebuster plus `codex plugin add` reinstall loop. [Local update note](https://developers.openai.com/plugins/build/plugins#install-a-local-plugin-manually) and `$CODEX_HOME/skills/.system/plugin-creator/references/installing-and-updating.md`.

**Inference for this repository:** target the intersection of the public submission checks and the bundled validator for this skills-only plugin. Include full author/interface metadata, omit MCP/app/hook fields because NMT does not need those components, and run both structural and installed-behavior validation. This avoids depending on which ingestion surface is more permissive.

## Repository layout

### Direct contract

- **Official requirement:** every plugin has `.codex-plugin/plugin.json`. Only `plugin.json` belongs in `.codex-plugin/`; `skills/`, optional `hooks/`, `.app.json`, `.mcp.json`, and presentation assets live at the plugin root. [Plugin structure](https://developers.openai.com/plugins/build/plugins#plugin-structure)
- **Official requirement for bundled Skills:** each Skill is an immediate child of `skills/` and contains a readable UTF-8 `SKILL.md`. Hidden Skill directories and nested Skill manifests are rejected by public package checks. [Skill archive errors](https://developers.openai.com/plugins/deploy/submission-errors#skill-errors)
- **Official requirement for a repo marketplace:** use `$REPO_ROOT/.agents/plugins/marketplace.json`. Git-backed entries support `source: "url"` when the plugin is at repository root and `source: "git-subdir"` when it is in a subdirectory. [Marketplace metadata and Git sources](https://developers.openai.com/plugins/build/plugins#marketplace-metadata)
- **Official requirement for uploaded archives:** the archive has exactly one plugin root, paths remain relative, and members are regular files or directories. `..` archive entries and unsupported member types are rejected. [ZIP structure errors](https://developers.openai.com/plugins/deploy/submission-errors#zip-structure-and-limit-errors)

### Recommended shape for this repository

**Inference for this repository:** make the existing repository root the plugin root and marketplace root. This is the least-duplicative cross-client shape: one Canon, one shared Skill source, and client metadata only in their prescribed hidden directories.

```text
Next-Move-Theory-Canon-and-Skills/
├── .codex-plugin/
│   └── plugin.json
├── .agents/
│   └── plugins/
│       └── marketplace.json
├── skills/
│   ├── nmt-analyze-interviews/
│   │   └── SKILL.md
│   ├── nmt-chat/
│   │   └── SKILL.md
│   └── ...
├── Next-Move-Theory-Canon/
│   ├── Advanced-Jobs-To-Be-Done/
│   ├── ABCDX-Segmentation/
│   ├── Algorithms/
│   ├── HowTos/
│   ├── Next-Move-Theory/
│   └── Riskiest-Assumption-Test/
├── README.md
└── LICENSE
```

Codex imposes no special directory name for the Canon. Keeping the current `Next-Move-Theory-Canon/` name avoids a purely mechanical migration. The important condition is that every runtime dependency stays inside the plugin root and therefore inside the installed copy.

This layout eliminates the current `Skills/codex/` versus `Skills/claude/` split. Codex expects one plugin-level `skills/` directory; its public Skill contract is already intended for workflows shared between ChatGPT and Codex. [Build Skills](https://learn.chatgpt.com/docs/build-skills)

## `.codex-plugin/plugin.json`

### Required package identity

The public package checks establish these required fields for a submission-grade package:

- `name`: required, at most 64 characters, begins with an ASCII letter or digit, and uses only ASCII letters, digits, `_`, or `-`.
- `version`: required SemVer, at most 64 characters.
- `description`: required, non-empty, at most 1,024 characters.
- `author.name`: required.
- `interface.displayName`, `interface.shortDescription`, `interface.longDescription`, and `interface.developerName`: required by package/listing validation.
- Final public-directory limits are stricter: display name and short description are each at most 30 characters; developer name is at most 80; long description is at most 4,000. [Submission field limits](https://developers.openai.com/plugins/deploy/submission-errors#final-directory-submission) and [listing/interface errors](https://developers.openai.com/plugins/deploy/submission-errors#listing-and-interface-errors)

For a skills-only NMT plugin, use a complete manifest in this shape:

```json
{
  "name": "next-move-theory",
  "version": "0.1.0",
  "description": "Advanced Jobs To Be Done and Next Move Theory canon and workflows.",
  "author": {
    "name": "Next Move Theory"
  },
  "homepage": "https://nextmovetheory.com/",
  "repository": "https://github.com/<owner>/<repository>",
  "license": "<repository-license-identifier>",
  "keywords": ["ajtbd", "jobs-to-be-done", "product-strategy"],
  "skills": "./skills/",
  "interface": {
    "displayName": "Next Move Theory",
    "shortDescription": "Apply Next Move Theory",
    "longDescription": "Use the bundled Next Move Theory canon and workflows for product strategy, research, segmentation, value, positioning, and validation.",
    "developerName": "Next Move Theory",
    "category": "Productivity",
    "capabilities": ["Read", "Write"],
    "defaultPrompt": [
      "Diagnose my product with Next Move Theory"
    ]
  }
}
```

The exact publisher, repository URL, license identifier, copy, category, and prompts are product decisions, not resolved by this research.

Additional rules relevant here:

- **Official requirement:** manifest component and asset paths resolve from the plugin root, start with `./`, and stay inside the plugin. Use `skills` for the root `skills/` directory. [Manifest path rules](https://developers.openai.com/plugins/build/plugins#path-rules)
- **Official requirement:** each bundled Skill has a unique `name`; the combined `plugin-name:skill-name` identity is at most 64 characters. [Skill errors](https://developers.openai.com/plugins/deploy/submission-errors#skill-errors)
- **Official requirement:** `apps` and `mcpServers` do not belong in a skills-only ZIP. [Skills-only ZIP checks](https://developers.openai.com/plugins/deploy/submission-errors#skills-only-zip-upload-errors-and-warnings)
- **Bundled tooling convention:** include `interface.category`, an array-valued `interface.capabilities`, and `interface.defaultPrompt`; use real values rather than `[TODO: ...]`. The bundled validator requires these even where the public docs describe some as optional.
- **Inference for this repository:** omit `hooks`, `apps`, and `mcpServers` entirely. No NMT requirement identified in this ticket needs them, and omission passes both the public skills-only contract and the stricter bundled validator.

## Marketplace shape and workflow

OpenAI defines a marketplace as a JSON catalog. A marketplace can list one plugin or many. The file contains:

- top-level `name`;
- optional top-level `interface.displayName`;
- ordered `plugins[]` entries;
- for each entry, `name`, `source`, `policy.installation`, `policy.authentication`, and `category`. [Marketplace metadata](https://developers.openai.com/plugins/build/plugins#marketplace-metadata)

A repository-root plugin can use a Git-backed `url` source:

```json
{
  "name": "next-move-theory",
  "interface": {
    "displayName": "Next Move Theory"
  },
  "plugins": [
    {
      "name": "next-move-theory",
      "source": {
        "source": "url",
        "url": "https://github.com/<owner>/<repository>.git",
        "ref": "main"
      },
      "policy": {
        "installation": "AVAILABLE",
        "authentication": "ON_INSTALL"
      },
      "category": "Productivity"
    }
  ]
}
```

- **Official requirement:** local `source.path` values are relative to the marketplace root, begin with `./`, and remain inside that root. The marketplace root is not the `.agents/plugins/` directory itself. [Local path resolution](https://developers.openai.com/plugins/build/plugins#install-a-local-plugin-manually)
- **Official requirement:** supported installation policies include `AVAILABLE`, `INSTALLED_BY_DEFAULT`, and `NOT_AVAILABLE`; authentication policy controls install-time versus first-use auth. [Marketplace metadata](https://developers.openai.com/plugins/build/plugins#marketplace-metadata)
- **Bundled tooling convention:** default a new entry to `AVAILABLE`, `ON_INSTALL`, and `Productivity`; append entries rather than reorder them; keep the plugin entry name aligned with the plugin folder and manifest name.
- **Inference for this repository:** use the same `next-move-theory` identifier for the marketplace and plugin. Different names are possible, but make install selectors and support instructions harder to read.

For local development, the public docs allow a personal marketplace at `~/.agents/plugins/marketplace.json` or a repo marketplace. The official public example stores personal plugin sources under `~/.codex/plugins/`; the bundled creator defaults to `~/plugins/<plugin-name>`. These are examples, not fixed source locations: the marketplace path controls the source, and the actual installed copy still goes into the Codex cache. [Personal marketplace example and path note](https://developers.openai.com/plugins/build/plugins#install-a-local-plugin-manually)

## User-global installation and consumer-repository cleanliness

### Git marketplace installation

The current public and CLI contract supports these marketplace sources: GitHub shorthand, Git URLs over HTTPS or SSH, and local marketplace roots. `--ref` pins a Git ref; `--sparse` is available for Git sources. [Add a marketplace from the CLI](https://developers.openai.com/plugins/build/plugins#add-a-marketplace-from-the-cli)

```bash
codex plugin marketplace add <owner>/<repository> --ref main
codex plugin marketplace list
codex plugin add next-move-theory@next-move-theory
codex plugin list
```

Installed `codex-cli 0.144.5` additionally exposes JSON modes:

```bash
codex plugin marketplace list --json
codex plugin list --available --json
codex plugin add next-move-theory@next-move-theory --json
```

The interactive install flow is:

```text
/plugins
```

Choose the marketplace, install the plugin, and start a new session. [Codex CLI plugin browser](https://learn.chatgpt.com/docs/plugins#plugin-browser-in-codex-cli)

### Where state goes

| State | Location | Source level |
| --- | --- | --- |
| Personal marketplace file | `~/.agents/plugins/marketplace.json` | Official public path for a local personal marketplace. |
| Installed plugin copy | `~/.codex/plugins/cache/$MARKETPLACE_NAME/$PLUGIN_NAME/$VERSION/` | Official public cache contract; local plugins use version directory `local`. |
| Plugin enable/disable state | `~/.codex/config.toml` | Official public state contract. |
| Git marketplace snapshot | User-level configured marketplace state; inspect its resolved root with `codex plugin marketplace list` | Official CLI behavior; public docs do not promise a stable internal snapshot path. |
| Consumer repository | no file required | Inference from the documented user-level destinations and marketplace install flow. |

Source: [How local marketplaces work](https://developers.openai.com/plugins/build/plugins#how-local-marketplaces-work).

**Inference for this repository:** installation can leave a consumer repository byte-for-byte untouched if the user adds the Git marketplace globally and installs from it, rather than copying Skills to `$REPO_ROOT/.agents/skills` or creating a repo marketplace in the consumer. The plugin's later runtime actions may still edit a project when the user asks it to do product work; that is normal Skill behavior, not installation residue.

The current installers' practice of copying the Canon, Skills, version files, README material, and agent instructions into every consumer repository is not required by Codex's plugin contract.

## Skill discovery

- **Official requirement:** a Skill is a directory with `SKILL.md`; `name` and `description` are required frontmatter fields, and the body must be non-empty. Each Skill directory is an immediate child of the plugin's `skills/` directory. [Build Skills](https://learn.chatgpt.com/docs/build-skills) and [Skill validation errors](https://developers.openai.com/plugins/deploy/submission-errors#skill-errors)
- **Official behavior:** Codex initially loads Skill name, description, and path, then loads the full `SKILL.md` after selection. A Skill can activate explicitly through `$skill-name` / `/skills` or implicitly when its description matches the request. [How Codex uses Skills](https://learn.chatgpt.com/docs/build-skills#how-chatgpt-and-codex-use-skills)
- **Official recommendation:** write concise, front-loaded descriptions because descriptions are the invocation router and may be shortened in large Skill sets. [Build Skills](https://learn.chatgpt.com/docs/build-skills)
- **Official distribution boundary:** `$HOME/.agents/skills` and repository `.agents/skills` are direct-authoring/local-discovery locations. Plugins are the recommended route when distributing reusable Skills or multiple related Skills. [Where Codex loads local Skills](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills)
- **Official behavior:** installed plugin Skills become available in new chats/sessions. [Plugins overview](https://learn.chatgpt.com/docs/plugins)

**Inference for this repository:** maintain exactly one `skills/<nmt-skill>/SKILL.md` source per Skill. Do not generate parallel `claude/` and `codex/` trees unless a later client-contract ticket proves an irreducible behavioral incompatibility.

## Canon and relative references

### What is explicit

- **Official requirement:** manifest paths are plugin-root relative and stay inside the plugin root. [Path rules](https://developers.openai.com/plugins/build/plugins#path-rules)
- **Official Skill shape:** supporting `references/`, `scripts/`, and `assets/` can live inside a Skill directory and are loaded as needed. [Build Skills](https://learn.chatgpt.com/docs/build-skills)
- **Bundled tooling convention:** OpenAI's bundled `skill-creator` says reference documents belong in `references/`, should be linked directly from `SKILL.md`, and should be loaded progressively. `$CODEX_HOME/skills/.system/skill-creator/SKILL.md`.
- **Observed first-party package convention:** the installed OpenAI-bundled `sites` plugin uses Skill-local links such as `references/persistence-and-storage.md` from `skills/sites-building/SKILL.md`. Its complete plugin, Skills, references, and root scripts are installed together under `~/.codex/plugins/cache/openai-bundled/sites/<version>/`.
- **Official test requirement:** before submission, verify that bundled files and references resolve after installation. [Complete-plugin checklist](https://developers.openai.com/plugins/deploy/connect-chatgpt#test-the-complete-plugin)

### What is not explicit

Public OpenAI docs do not currently state that a Markdown link such as `../../Next-Move-Theory-Canon/...` is resolved automatically from the containing `SKILL.md`, nor do they expose a general Skill-content `${PLUGIN_ROOT}` substitution contract. The documented `PLUGIN_ROOT` environment variable is explicitly described for plugin hook commands, not ordinary prose in a Skill. [Plugin hook environment](https://developers.openai.com/plugins/build/plugins#bundled-mcp-servers-and-lifecycle-hooks)

### Relocation-safe design for NMT

**Inference for this repository:** keep one Canon tree at the plugin root and make every Skill pointer explicitly relative to its own `SKILL.md`, for example:

```markdown
When the task concerns segmentation, resolve this path from the directory
containing this `SKILL.md`, then read:

`../../Next-Move-Theory-Canon/Advanced-Jobs-To-Be-Done/segmentation.md`
```

This path remains inside the plugin archive and preserves one source of truth. It does not depend on the consumer's current working directory or on a hard-coded `~/.codex/plugins/cache/...` version path.

Treat this as a hypothesis until the installed-copy test passes. The acceptance test must invoke every Skill from an unrelated clean repository and confirm it reads at least one required Canon file from the actual cache root reported by the Skill path. OpenAI's own test checklist explicitly requires this verification.

Do not use symlinks to share the Canon across Skill directories. Public ZIP checks accept regular files and directories and reject unsupported archive member types; a single real Canon directory plus tested in-archive pointers is the safer package. [ZIP member checks](https://developers.openai.com/plugins/deploy/submission-errors#zip-structure-and-limit-errors)

## Updates and cache behavior

### Marketplace updates

Current public docs and CLI expose:

```bash
codex plugin marketplace upgrade
codex plugin marketplace upgrade next-move-theory
```

These commands refresh configured Git marketplace snapshots. They do not, by their documented description, promise to replace an already installed plugin cache entry. [Marketplace CLI](https://developers.openai.com/plugins/build/plugins#add-a-marketplace-from-the-cli)

### Plugin updates

- **Official public behavior for local sources:** update the directory referenced by the local marketplace and restart the ChatGPT desktop app so it picks up the changed files. Local installed copies use the cache version directory `local`. [Local update behavior](https://developers.openai.com/plugins/build/plugins#install-a-local-plugin-manually)
- **Official release requirement:** a new published release uses a different manifest version; reusing the published version produces a submission warning/confirmation path. [Skills-only ZIP update checks](https://developers.openai.com/plugins/deploy/submission-errors#skills-only-zip-upload-errors-and-warnings)
- **Bundled tooling convention for deterministic local iteration:** preserve the base SemVer, replace its build metadata with `+codex.<timestamp>`, reinstall with `codex plugin add <plugin>@<marketplace>`, and start a new thread. `$CODEX_HOME/skills/.system/plugin-creator/references/installing-and-updating.md` and `scripts/update_plugin_cachebuster.py`.

Recommended policies:

1. **Git-distributed releases:** bump `.codex-plugin/plugin.json` SemVer for every installable release, refresh the marketplace snapshot, reinstall the plugin, then start a new session.

   ```bash
   codex plugin marketplace upgrade next-move-theory
   codex plugin add next-move-theory@next-move-theory
   ```

2. **Local worktree iteration:** either follow the public source-update + restart path or use the bundled cachebuster + reinstall flow when deterministic cache replacement matters.

3. **Never reference the cache directory by literal version:** the version is part of the installed path and changes across releases.

The bundled helper's cachebuster is a development convention, not the release version policy. A public release should use an intentional SemVer rather than a timestamped local build token.

## Validation contract

There is no single public `codex plugin validate` command in the current CLI. Validation has three layers.

### 1. Static Skill checks

For every Skill:

```bash
python3 "$CODEX_HOME/skills/.system/skill-creator/scripts/quick_validate.py" \
  skills/<skill-name>
```

The OpenAI-bundled `skill-creator` says this validates YAML frontmatter, required fields, and naming rules.

### 2. Bundled plugin preflight

```bash
python3 "$CODEX_HOME/skills/.system/plugin-creator/scripts/validate_plugin.py" .
```

The validator checks `.codex-plugin/plugin.json`, strict SemVer, required author/interface metadata, component paths, bundled Skill frontmatter, optional `agents/openai.yaml`, assets, and leftover `[TODO: ...]` placeholders. This is a **bundled tooling convention**, not a complete substitute for public submission validation.

Environment note: in the current shell, plain system `python3` could not run this helper because `PyYAML` was not installed (`ModuleNotFoundError: yaml`). The implementation/CI ticket must provide a Python environment with PyYAML or use the bundled workspace runtime; do not claim the validator passes until the command actually runs.

### 3. Installed-copy validation

OpenAI's public test contract requires installing from a local marketplace, starting a new conversation, and testing:

- direct requests that should activate each Skill;
- indirect requests expressing the same goal;
- negative requests that should not activate the plugin;
- boundary cases the plugin intentionally does not support;
- every required bundled file/reference after installation;
- starter prompts against workflows the plugin can actually complete. [Test the complete plugin](https://developers.openai.com/plugins/deploy/connect-chatgpt#test-the-complete-plugin)

For this repository, add two concrete acceptance checks:

1. **Canon relocation:** from a clean unrelated repository, invoke every NMT Skill and confirm its required Canon path resolves inside `~/.codex/plugins/cache/<marketplace>/next-move-theory/<version>/...`.
2. **Consumer cleanliness:** record `git status --short` and the directory listing of a disposable consumer repository before marketplace registration and plugin install; repeat after install and first invocation. Installation passes only if there is no consumer-repo delta.

Useful read-only/install checks from the current CLI:

```bash
codex plugin marketplace list --json
codex plugin list --available --json
codex plugin add next-move-theory@next-move-theory --json
codex plugin list --json
```

Uninstall and marketplace cleanup are also user-level:

```bash
codex plugin remove next-move-theory@next-move-theory
codex plugin marketplace remove next-move-theory
```

## Decision-ready contract

The Codex side of the larger repository redesign can proceed with these constraints:

1. Use one repository-root plugin with `.codex-plugin/plugin.json`, one shared root `skills/` tree, and the complete Canon inside the plugin root.
2. Add a repo marketplace at `.agents/plugins/marketplace.json`; use a Git `url` source for a repository-root plugin.
3. Install by configuring the Git marketplace and installing the named plugin; user state and the installed copy remain under the user's home directory.
4. Treat `name`, SemVer `version`, `description`, `author.name`, the main `interface` copy, and `skills: "./skills/"` as the publish-ready manifest baseline.
5. Keep `apps`, `mcpServers`, and hooks out of this skills-only package unless a later requirement adds the corresponding component.
6. Use one Skill source per workflow. Codex discovers immediate-child Skills from the plugin's `skills/` directory and routes them by frontmatter description.
7. Keep one Canon source at plugin root; replace project-root lookups with Skill-relative, in-archive pointers and make installed-copy resolution a blocking acceptance test.
8. Bump SemVer for installable Git releases; refresh the Git marketplace, reinstall, and use a new session. Use the bundled cachebuster only for local iteration.
9. Validate Skills, run the bundled plugin preflight in a Python environment with PyYAML, install from a marketplace, test routing and references, and prove the consumer repository remains unchanged.

## First-party sources consulted

Public OpenAI sources:

- [Package your plugin](https://developers.openai.com/plugins/build/plugins)
- [Build plugins](https://learn.chatgpt.com/docs/build-plugins)
- [Build Skills](https://learn.chatgpt.com/docs/build-skills)
- [Plugins](https://learn.chatgpt.com/docs/plugins)
- [Plugin architecture](https://developers.openai.com/plugins/concepts/plugins)
- [Connect and test your plugin](https://developers.openai.com/plugins/deploy/connect-chatgpt)
- [Plugin submission errors](https://developers.openai.com/plugins/deploy/submission-errors)

Local first-party snapshot:

- `$CODEX_HOME/skills/.system/plugin-creator/SKILL.md`
- `$CODEX_HOME/skills/.system/plugin-creator/references/plugin-json-spec.md`
- `$CODEX_HOME/skills/.system/plugin-creator/references/installing-and-updating.md`
- `$CODEX_HOME/skills/.system/plugin-creator/scripts/create_basic_plugin.py`
- `$CODEX_HOME/skills/.system/plugin-creator/scripts/update_plugin_cachebuster.py`
- `$CODEX_HOME/skills/.system/plugin-creator/scripts/validate_plugin.py`
- `$CODEX_HOME/skills/.system/skill-creator/SKILL.md`
- Installed OpenAI-bundled plugin manifests and Skills under `~/.codex/plugins/cache/openai-bundled/`
- `codex --version`, `codex plugin --help`, `codex plugin add --help`, `codex plugin list --help`, and `codex plugin marketplace {add,list,upgrade} --help` from `codex-cli 0.144.5`
