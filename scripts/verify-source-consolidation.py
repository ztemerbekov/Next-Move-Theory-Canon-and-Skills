#!/usr/bin/env python3
"""Verify the mechanical Skill-source consolidation for Wayfinder #13.

The verifier is intentionally read-only.  It compares the new shared source
with the preserved Claude baseline after reversing only the migrations allowed
by docs/repository-migration-specification.md.
"""

from __future__ import annotations

import argparse
import difflib
import hashlib
import re
import sys
from pathlib import Path


SKILLS = (
    "nmt-analyze-interviews",
    "nmt-chat",
    "nmt-craft-go-to-market",
    "nmt-craft-value-proposition",
    "nmt-diagnose",
    "nmt-market-research",
    "nmt-product-requirements",
    "nmt-upgrade",
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalize_baseline(text: str) -> str:
    """Remove the old Claude-only visibility declaration."""

    return re.sub(r"^user-invocable: true\n", "", text, flags=re.MULTILINE)


def normalize_candidate(text: str, skill_name: str) -> str:
    """Reverse only the path and frontmatter transformations."""

    # The old public pointer named an internal-only file that is not bundled.
    # The migration fixes that objectively broken path to the bundled public
    # mechanics file; keep the correction in the explicit parity allowlist.
    if skill_name == "nmt-analyze-interviews":
        text = text.replace(
            "`../../Next-Move-Theory-Canon/Advanced-Jobs-To-Be-Done/"
            "value-creation-mechanics.md`; cited as provenance",
            "`Next-Move-Theory-Canon/Next-Move-Theory/mechanics-catalog.md`; "
            "cited as provenance",
        )

    text = text.replace(
        "../../references/producer-contract.md", "../PRODUCER-CONTRACT.md"
    )
    text = text.replace(
        "../../references/readability-contract.md", "../READABILITY-CONTRACT.md"
    )
    text = re.sub(r"^user-invocable: true\n", "", text, flags=re.MULTILINE)

    # nmt-upgrade is the Legacy workflow.  Its project-root Canon paths must
    # remain untouched; all other Skills use the Plugin-relative path.
    if skill_name != "nmt-upgrade":
        text = re.sub(
            r"(?<![A-Za-z0-9-])\.\./\.\./Next-Move-Theory-Canon/",
            "Next-Move-Theory-Canon/",
            text,
        )
    return text


def check_skill(repo: Path, name: str, failures: list[str]) -> None:
    baseline = repo / "docs/migration/legacy-inputs/Skills/claude" / name
    candidate = repo / "skills" / name

    if not baseline.is_dir():
        failures.append(f"missing Claude baseline: {baseline}")
        return
    if not candidate.is_dir():
        failures.append(f"missing consolidated Skill: {candidate}")
        return

    baseline_files = {p.relative_to(baseline) for p in baseline.rglob("*") if p.is_file()}
    candidate_files = {p.relative_to(candidate) for p in candidate.rglob("*") if p.is_file()}
    if baseline_files != candidate_files:
        failures.append(
            f"{name}: file inventory differs: baseline={sorted(baseline_files)} "
            f"candidate={sorted(candidate_files)}"
        )
        return

    for relative in sorted(baseline_files):
        old_path = baseline / relative
        new_path = candidate / relative
        old = old_path.read_text(encoding="utf-8")
        new = new_path.read_text(encoding="utf-8")
        if relative == Path("SKILL.md"):
            old = normalize_baseline(old)
            new = normalize_candidate(new, name)
        if old != new:
            old_lines = old.splitlines(keepends=True)
            new_lines = new.splitlines(keepends=True)
            diff = list(
                difflib.unified_diff(
                    old_lines,
                    new_lines,
                    fromfile=f"Claude baseline/{name}/{relative}",
                    tofile=f"shared source/{name}/{relative}",
                    n=3,
                )
            )
            if len(diff) > 80:
                diff = diff[:80] + ["... diff output truncated after 80 lines ...\n"]
            context = "".join(diff).rstrip()
            failures.append(
                f"{name}/{relative}: unexpected content diff\n{context}"
            )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="repository root (defaults to the parent of scripts/)",
    )
    args = parser.parse_args()
    repo = args.repo_root.resolve()
    failures: list[str] = []

    expected = set(SKILLS)
    source_root = repo / "skills"
    actual = {p.name for p in source_root.iterdir() if p.is_dir()} if source_root.is_dir() else set()
    if actual != expected:
        failures.append(f"skills/ directory inventory differs: expected={sorted(expected)} actual={sorted(actual)}")

    for name in SKILLS:
        check_skill(repo, name, failures)

    for name in ("producer-contract.md", "readability-contract.md"):
        reference = repo / "references" / name
        baseline = repo / "docs/migration/legacy-inputs/Skills/claude" / (
            "PRODUCER-CONTRACT.md" if name.startswith("producer") else "READABILITY-CONTRACT.md"
        )
        if not reference.is_file():
            failures.append(f"missing shared reference: {reference}")
        elif not baseline.is_file():
            failures.append(f"missing shared-reference baseline: {baseline}")
        elif reference.read_bytes() != baseline.read_bytes():
            failures.append(f"{name}: shared reference is not byte-preserved")

    if not (repo / "docs/migration/legacy-inputs/Skills/codex").is_dir():
        failures.append("missing preserved Codex migration evidence tree")
    if (repo / "Next-Move-Theory-Canon/Next-Move-Theory-Canon").exists():
        failures.append("nested Next-Move-Theory-Canon directory detected")

    for path in sorted((repo / "skills").glob("*/SKILL.md")):
        text = path.read_text(encoding="utf-8")
        if "user-invocable:" in text:
            failures.append(f"{path.relative_to(repo)}: non-portable user-invocable metadata remains")

        for relative in re.findall(
            r"(?<![A-Za-z0-9-])(\.\./\.\./Next-Move-Theory-Canon/"
            r"[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)*)",
            text,
        ):
            if "..." in relative:
                continue
            target = (path.parent / relative).resolve()
            if not target.is_file():
                failures.append(
                    f"{path.relative_to(repo)}: Canon pointer does not resolve: {relative}"
                )

        for relative in re.findall(
            r"(?<![A-Za-z0-9-])(\.\./\.\./references/"
            r"[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)*)",
            text,
        ):
            target = (path.parent / relative).resolve()
            if not target.is_file():
                failures.append(
                    f"{path.relative_to(repo)}: shared-reference pointer does not resolve: {relative}"
                )

    if failures:
        print("FAIL: source consolidation verification")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(f"PASS: {len(SKILLS)} Skills match the Claude baseline after the mechanical allowlist")
    print("PASS: shared contracts are byte-preserved in references/")
    print("PASS: Codex baseline is preserved as migration evidence")
    print("PASS: Canon has one root and the consolidated tree has eight Skill entries")
    return 0


if __name__ == "__main__":
    sys.exit(main())
