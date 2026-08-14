# Migration boundary

The `1.0.0` Plugin is a fresh user-global installation. It does not migrate an
existing project-local Legacy setup.

## What is intentionally not automated

The Plugin does not scan, copy, reconcile, rewrite, or delete any of these in a
Consumer project:

- `AGENTS.md` or `CLAUDE.md`;
- `.agents/` or `.claude/`;
- `Next-Move-Theory-Canon/`;
- project-local Skills; or
- `.nmt-version` and other Legacy state.

There is no migration command, cleanup pass, compatibility merge, or promise
that two installations will be reconciled. This keeps the fresh Plugin
installation independent of project history and preserves user changes.

## Adopting the Plugin beside a Legacy setup

1. Record the Consumer project's current Git status and any local Legacy files.
2. Install `next-move-theory` at user scope using
   [`installation.md`](installation.md).
3. Start a new Client session and verify that `nmt-chat` routes to the bundled
   Skills and Canon.
4. Leave the Legacy files in place until the owner chooses a separate manual
   cleanup. The Plugin does not remove or reconcile them.

If the Legacy layout and the Plugin produce different results, treat that as a
separate compatibility decision; do not modify a Skill or a Client cache as an
implicit migration fix.
