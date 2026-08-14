# Source-tree consolidation report

Wayfinder ticket: [#13 — Consolidate the Canon, references, and one Skill source tree](https://github.com/ztemerbekov/Next-Move-Theory-Canon-and-Skills/issues/13)

Specification: [repository migration specification](../repository-migration-specification.md)

## Result

The repository now has one physical lower-case `skills/` directory containing
exactly the eight direct NMT Skill entry points. It is the only candidate
editable Skill source tree.

The Canon remains at the exact `Next-Move-Theory-Canon/` path and remains a
single root. The shared producer and readability contracts are now under
`references/` and are byte-preserved.

The old Claude and Codex trees were not deleted. Because this development
environment uses a case-insensitive filesystem, `Skills/` and `skills/` cannot
coexist as separate physical directories. The old trees were therefore moved
without content changes to:

```text
docs/migration/legacy-inputs/Skills/claude/
docs/migration/legacy-inputs/Skills/codex/
```

They are read-only migration evidence. Ticket #16 owns their final retirement
after parity and clean-environment acceptance; they are not part of the
authoritative `skills/` source tree.

## Mechanical transformations

Only the locked allowlist was applied to the new source:

- shared contract pointers now resolve through `../../references/`;
- non-Legacy Canon pointers now resolve through the Plugin-relative
  `../../Next-Move-Theory-Canon/` path;
- the one objectively broken baseline pointer to the absent internal
  `mechanics-catalog.md` is corrected to the bundled public
  `value-creation-mechanics.md` file;
- `user-invocable: true` was removed as a redundant Claude extension rejected by
  the current Codex validator;
- `nmt-upgrade` keeps its project-root Canon paths and Legacy workflow;
- no workflow step, question, mode, handoff, output contract, methodology rule,
  or completion gate was rewritten.

No generated Client-specific Skill tree was created. The preserved Codex tree is
only a comparison input until final parity closes it out.

## Verification

Command:

```bash
python3 scripts/verify-source-consolidation.py
```

Observed result:

```text
PASS: 8 Skills match the Claude baseline after the mechanical allowlist
PASS: shared contracts are byte-preserved in references/
PASS: Codex baseline is preserved as migration evidence
PASS: Canon has one root and the consolidated tree has eight Skill entries
```

The verifier is read-only. It compares every file in each migrated Skill with
the preserved Claude baseline after reversing only the allowlisted path and
frontmatter transformations. Any other content or inventory difference fails.

The official `quick_validate.py` run passes six Skills. Two existing Claude
baseline descriptions remain over the strict 1,024-character frontmatter limit:
`nmt-analyze-interviews` and `nmt-diagnose`. Their complete descriptions were
not truncated because that would alter model-facing routing semantics. This is
recorded as a proven frontmatter compatibility finding for the validation and
adapter slices; the source consolidation keeps the reviewed baseline intact.

## Scope boundary

This ticket does not claim manifest validation, adapter drift validation,
clean-environment runtime smoke, update behavior, or final removal of the
legacy evidence trees. Those are owned by #15, #18, #19, #14, #17, and #16.
