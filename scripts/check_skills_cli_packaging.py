#!/usr/bin/env python3
"""Smoke-test the eight-Skill payload through the skills CLI in isolated state."""

from __future__ import annotations

import argparse
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


def command(mode: str, home: Path) -> tuple[list[str], subprocess.CompletedProcess[str]]:
    cache = home / "npm-cache"
    env = os.environ.copy()
    env.update(
        {
            "HOME": str(home),
            "XDG_CONFIG_HOME": str(home / "config"),
            "npm_config_cache": str(cache),
        }
    )
    argv = [
        "npx",
        "--yes",
        "skills@latest",
        "add",
        str(ROOT),
        "--skill",
        "*",
        "-a",
        "codex",
        "-a",
        "claude-code",
        "-g",
        "-y",
    ]
    if mode == "copy":
        argv.append("--copy")
    result = subprocess.run(
        argv,
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        timeout=300,
        check=False,
    )
    return argv, result


def find_skill_roots(home: Path) -> list[Path]:
    roots: set[Path] = set()
    for skill in home.rglob("nmt-chat"):
        if not skill.is_dir():
            continue
        candidate = skill.parent
        actual = {
            child.name
            for child in candidate.iterdir()
            if child.name in SKILLS and child.is_dir()
        }
        if actual == SKILLS:
            roots.add(candidate)
    return sorted(roots)


def verify_install(mode: str, home: Path) -> list[str]:
    failures: list[str] = []
    roots = find_skill_roots(home)
    if len(roots) != 2:
        return [f"{mode}: expected separate Codex and Claude skill roots, found {roots}"]

    for root in roots:
        actual = {
            child.name
            for child in root.iterdir()
            if child.name.startswith("nmt-") and child.is_dir()
        }
        if actual != SKILLS:
            failures.append(f"{mode} {root}: expected eight Skills, found {sorted(actual)}")

        linked = [skill for skill in sorted(SKILLS) if (root / skill).is_symlink()]
        if mode == "copy" and linked:
            failures.append(f"{mode} {root}: copied Skill directories are symlinks: {linked}")

        nmt_chat_references = root / "nmt-chat" / "references"
        if {
            path.name for path in nmt_chat_references.iterdir() if path.is_file()
        } != SHARED_REFERENCES:
            failures.append(f"{mode} {root}: nmt-chat shared-reference payload is incomplete")
        canon = nmt_chat_references / "Next-Move-Theory-Canon"
        if not (canon / CANON_PROBE).is_file():
            failures.append(f"{mode} {root}: bundled Canon probe is unreadable")

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
                failures.append(f"{mode} {root}: {skill} Canon anchor does not resolve")
            if skill in PRODUCER_SKILLS:
                contract = skill_root / "../nmt-chat/references/producer-contract.md"
                if not contract.resolve().is_file():
                    failures.append(f"{mode} {root}: {skill} producer contract is unreadable")

    if mode == "symlink" and not any(
        (root / skill).is_symlink()
        for root in roots
        for skill in SKILLS
    ):
        failures.append(f"{mode}: CLI did not create any symlinked Client Skill payload")
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
    before = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=all"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    ).stdout
    failures: list[str] = []
    for mode in modes:
        with tempfile.TemporaryDirectory(prefix=f"nmt-skills-cli-{mode}-") as temporary:
            home = Path(temporary) / "home"
            home.mkdir()
            argv, result = command(mode, home)
            if result.returncode:
                output = (result.stdout + result.stderr).strip()[-2000:]
                failures.append(f"{mode}: skills CLI failed ({result.returncode}): {output}")
                continue
            failures.extend(verify_install(mode, home))

    after = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=all"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    ).stdout
    if before != after:
        failures.append("Consumer/source worktree status changed during isolated installation")

    if failures:
        print("SKILLS CLI PACKAGING FAILED")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("PASS: skills CLI installed all eight Skills for Codex and Claude Code")
    print("PASS: copy and symlink modes preserve the nmt-chat Canon/shared-reference payload")
    print("PASS: every installed Skill resolves its Canon anchor and producer contracts")
    print("PASS: source worktree status remained unchanged")
    return 0


if __name__ == "__main__":
    sys.exit(main())
