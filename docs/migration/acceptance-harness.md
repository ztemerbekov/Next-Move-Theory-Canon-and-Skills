# Clean-environment acceptance harness

The implementation for Wayfinder ticket [#14](https://github.com/ztemerbekov/Next-Move-Theory-Canon-and-Skills/issues/14)
is the repository-local `scripts/run_acceptance_harness.py` command. It tests
the installed package boundary; it does not inspect or rewrite the contents of
the eight Skills.

## What it isolates

Each run creates temporary state outside the repository:

- a disposable Codex home and marketplace source;
- a disposable unrelated Git Consumer with a baseline commit;
- a first package snapshot and a temporary `1.0.1` update snapshot;
- a JSON report containing command status, package fingerprints, file hashes,
  and before/after Consumer comparisons.

The temporary state is removed when the run ends. The harness never writes to
the Consumer or the checkout, never relies on a literal cache-version path,
and redacts credential-shaped output. The repository static suite runs before
any client operation.

## Commands

Run the static gates plus installation, discovery, bundled-Canon, update, and
Consumer-cleanliness checks for Codex without model credentials:

```bash
python3 scripts/run_acceptance_harness.py --client codex
```

Without an authenticated Codex runtime, the report still proves installation,
discovery, package refresh, and Consumer cleanliness. The model calls are
recorded as an `evidence_boundary` and the command exits non-zero.

To run the Codex model smoke using an already-existing local Codex credential,
copy it only into the disposable test state:

```bash
python3 scripts/run_acceptance_harness.py \
  --client codex \
  --codex-auth-source /path/to/existing/codex/auth.json \
  --report /tmp/nmt-acceptance-codex.json
```

The harness does not create, refresh, print, or persist credentials. The
source file is copied to temporary state for the duration of this process and
is not included in the report.

Claude Code is intentionally a no-auth evidence boundary in this harness:

```bash
python3 scripts/run_acceptance_harness.py --client claude
```

This records `claude --version` only. It does not run Claude Code prompts,
invoke `claude login`, repair an account, or modify Claude state. A functioning
Claude runtime can be tested later through the same black-box contract, but an
unavailable runtime is reported as evidence boundary rather than converted
into an authentication task.

`--client all` runs the Codex path and records the Claude version/boundary in
the same report. It is useful for a status snapshot, but it cannot claim a
full two-client runtime pass while Claude remains at that boundary.

## Checks recorded

For Codex, a successful authenticated run records:

1. version and isolated login status;
2. local user-global marketplace installation and Plugin discovery;
3. exactly eight installed Skills and one bundled Canon root carried by the
   `nmt-chat` payload;
4. one direct smoke call per Skill, installed-Canon access, the model-invoked
   `nmt-chat` router, and a negative unrelated route;
5. native local-fixture reinstall with a changed package fingerprint;
6. unchanged Consumer file hashes and Git status after the whole run.

The local update fixture is deliberate: the current Codex CLI supports native
Plugin reinstall for a local source, while marketplace upgrade is only
available for hosted Git sources. The harness marks local marketplace refresh
as `not_applicable` and still exercises the native reinstall/update boundary.

No command in this harness calls the Legacy installer. Legacy behavior remains
documented separately in the current [installation](../installation.md) and
[update](../updates.md) boundary documents.
