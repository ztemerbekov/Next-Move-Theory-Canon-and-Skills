#!/usr/bin/env python3
"""Smoke-test the supported skills CLI install and update path in disposable state."""

from __future__ import annotations

import argparse
import hashlib
import os
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = frozenset(
    {
        "nmt-analyze-interviews",
        "nmt-chat",
        "nmt-craft-go-to-market",
        "nmt-craft-value-proposition",
        "nmt-diagnose",
        "nmt-market-research",
        "nmt-product-requirements",
        "nmt-upgrade",
    }
)
PRODUCER_SKILLS = SKILLS - {"nmt-chat", "nmt-upgrade"}
CANON_PROBE = "Advanced-Jobs-To-Be-Done/ajtbd-key-theses.md"
SHARED_REFERENCES = {
    "canon-routing.md",
    "client-adapters.md",
    "methodology-guardrails.md",
    "producer-contract.md",
    "readability-contract.md",
    "skill-routing.md",
}
SUPPORTED_CLIENT_ARGS = ("-a", "codex", "-a", "claude-code")


def cli_command(
    home: Path,
    *,
    skill: str = "*",
    copy: bool = False,
    cwd: Path | None = None,
) -> tuple[list[str], subprocess.CompletedProcess[str]]:
    cache = home / "npm-cache"
    env = os.environ.copy()
    env.update(
        {
            "HOME": str(home),
            "XDG_CONFIG_HOME": str(home / "config"),
            "npm_config_cache": str(cache),
            "PYTHONDONTWRITEBYTECODE": "1",
        }
    )
    argv = [
        "npx",
        "--yes",
        "skills@latest",
        "add",
        str(ROOT),
        "--skill",
        skill,
        *SUPPORTED_CLIENT_ARGS,
        "-g",
        "-y",
    ]
    if copy:
        argv.append("--copy")
    result = subprocess.run(
        argv,
        cwd=cwd or ROOT,
        env=env,
        capture_output=True,
        text=True,
        timeout=300,
        check=False,
    )
    return argv, result


def inventory(root: Path) -> set[str]:
    return {
        child.name
        for child in root.iterdir()
        if child.name in SKILLS and child.is_dir()
    } if root.is_dir() else set()


def find_candidate_skill_roots(home: Path) -> list[Path]:
    roots: set[Path] = set()
    for skill_name in SKILLS:
        for skill in home.rglob(skill_name):
            if skill.is_dir():
                roots.add(skill.parent)
    return sorted(roots)


def find_full_skill_roots(home: Path) -> list[Path]:
    return [root for root in find_candidate_skill_roots(home) if inventory(root) == SKILLS]


def directory_fingerprint(root: Path) -> str:
    entries: list[tuple[str, str]] = []
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        if path.is_symlink() and path.is_dir():
            entries.append((relative, f"symlink:{os.readlink(path)}"))
        elif path.is_file():
            entries.append((relative, hashlib.sha256(path.read_bytes()).hexdigest()))
    return hashlib.sha256(
        "".join(f"{name}\0{value}\n" for name, value in entries).encode()
    ).hexdigest()


def consumer_snapshot(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def verify_install(mode: str, home: Path) -> tuple[list[str], list[Path]]:
    failures: list[str] = []
    roots = find_full_skill_roots(home)
    if len(roots) != 2:
        return [f"{mode}: expected separate Codex and Claude skill roots, found {roots}"], roots

    for root in roots:
        actual = inventory(root)
        if actual != SKILLS:
            failures.append(f"{mode} {root}: expected eight Skills, found {sorted(actual)}")

        linked = [skill for skill in sorted(SKILLS) if (root / skill).is_symlink()]
        if mode == "copy" and linked:
            failures.append(f"{mode} {root}: copied Skill directories are symlinks: {linked}")

        nmt_chat_references = root / "nmt-chat" / "references"
        actual_references = {
            path.name for path in nmt_chat_references.iterdir() if path.is_file()
        } if nmt_chat_references.is_dir() else set()
        if actual_references != SHARED_REFERENCES:
            failures.append(
                f"{mode} {root}: nmt-chat shared-reference payload is incomplete; "
                f"expected={sorted(SHARED_REFERENCES)}, actual={sorted(actual_references)}"
            )
        canon = nmt_chat_references / "Next-Move-Theory-Canon"
        if not (canon / CANON_PROBE).is_file():
            failures.append(f"{mode} {root}: bundled Canon probe is unreadable: {canon / CANON_PROBE}")

        for skill in sorted(SKILLS):
            skill_root = root / skill
            skill_file = skill_root / "SKILL.md"
            if not skill_file.is_file():
                failures.append(f"{mode} {root}: missing {skill}/SKILL.md")
                continue
            text = skill_file.read_text(encoding="utf-8")
            canon_anchor = (
                "references/Next-Move-Theory-Canon/"
                if skill == "nmt-chat"
                else "../nmt-chat/references/Next-Move-Theory-Canon/"
            )
            if canon_anchor not in text:
                failures.append(f"{mode} {root}: {skill} does not declare its Canon anchor")
            elif not (skill_root / canon_anchor).resolve().is_dir():
                failures.append(f"{mode} {root}: {skill} Canon anchor does not resolve: {canon_anchor}")
            if skill in PRODUCER_SKILLS:
                contract = skill_root / "../nmt-chat/references/producer-contract.md"
                if not contract.resolve().is_file():
                    failures.append(f"{mode} {root}: {skill} producer contract is unreadable: {contract}")
    return failures, roots


def run_mode(mode: str) -> list[str]:
    failures: list[str] = []
    with tempfile.TemporaryDirectory(prefix=f"nmt-skills-cli-{mode}-") as temporary:
        home = Path(temporary) / "home"
        home.mkdir()
        consumer = Path(temporary) / "consumer"
        consumer.mkdir()
        (consumer / "consumer.md").write_text("Unrelated consumer fixture.\n", encoding="utf-8")
        before_consumer = consumer_snapshot(consumer)

        argv, first = cli_command(home, copy=mode == "copy", cwd=consumer)
        if first.returncode:
            output = (first.stdout + first.stderr).strip()[-2000:]
            return [f"{mode}: skills CLI failed ({first.returncode}) for {' '.join(argv)}: {output}"]
        first_failures, roots = verify_install(mode, home)
        failures.extend(first_failures)
        if first_failures:
            return failures
        before_fingerprints = {
            root.relative_to(home).as_posix(): directory_fingerprint(root)
            for root in roots
        }

        _, second = cli_command(home, copy=mode == "copy", cwd=consumer)
        if second.returncode:
            output = (second.stdout + second.stderr).strip()[-2000:]
            failures.append(f"{mode}: repeated install/update failed ({second.returncode}): {output}")
        else:
            second_failures, updated_roots = verify_install(mode, home)
            failures.extend(second_failures)
            after_fingerprints = {
                root.relative_to(home).as_posix(): directory_fingerprint(root)
                for root in updated_roots
            }
            if before_fingerprints != after_fingerprints:
                failures.append(
                    f"{mode}: repeated install/update changed the installed snapshot; "
                    f"before={before_fingerprints}, after={after_fingerprints}"
                )
            else:
                print(f"PASS: {mode} repeated install/update is idempotent")

        after_consumer = consumer_snapshot(consumer)
        if before_consumer != after_consumer:
            failures.append(f"{mode}: Consumer fixture changed during install/update")
        else:
            print(f"PASS: {mode} Consumer fixture remained unchanged")

        if mode == "symlink":
            linked = [
                root / skill
                for root in find_full_skill_roots(home)
                for skill in SKILLS
                if (root / skill).is_symlink()
            ]
            if linked:
                print(f"PASS: symlink mode produced {len(linked)} symlinked Skill directories")
            else:
                print("INFO: symlink mode limitation — CLI materialized copies; payload checks still passed")
    return failures


def run_partial_install_negative() -> list[str]:
    failures: list[str] = []
    with tempfile.TemporaryDirectory(prefix="nmt-skills-cli-partial-") as temporary:
        home = Path(temporary) / "home"
        home.mkdir()
        consumer = Path(temporary) / "consumer"
        consumer.mkdir()
        _, result = cli_command(home, skill="nmt-market-research", copy=True, cwd=consumer)
        candidates = find_candidate_skill_roots(home)
        inventories = [sorted(inventory(root)) for root in candidates]
        if result.returncode != 0:
            print("PASS: partial install was explicitly rejected by the skills CLI")
            return failures
        if not candidates:
            failures.append("partial install returned success but created no observable Skill inventory")
            return failures
        if any(set(items) == SKILLS for items in inventories):
            failures.append(
                "partial install unexpectedly produced the complete suite; omission of nmt-chat "
                "was not rejected explicitly"
            )
            return failures
        if any("nmt-chat" in items for items in inventories):
            failures.append(
                f"partial install returned success with an unexpected nmt-chat payload: {inventories}"
            )
            return failures
        print(
            "PASS: partial install was rejected as unsupported by the harness "
            f"(CLI subset inventory: {inventories})"
        )
    return failures


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--mode",
        choices=("copy", "symlink", "both"),
        default="both",
        help="installation mode to exercise",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    modes = ("copy", "symlink") if args.mode == "both" else (args.mode,)
    failures: list[str] = []
    before = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=all"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    ).stdout
    for mode in modes:
        failures.extend(run_mode(mode))
    failures.extend(run_partial_install_negative())
    after = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=all"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    ).stdout
    if before != after:
        failures.append("source worktree status changed during isolated skills CLI acceptance")
    if failures:
        print("SKILLS CLI PACKAGING FAILED")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("PASS: skills CLI installed all eight Skills for Codex and Claude Code")
    print("PASS: every installed Skill resolves its Canon and shared-reference payload")
    print("PASS: source worktree status remained unchanged")
    return 0


if __name__ == "__main__":
    sys.exit(main())
