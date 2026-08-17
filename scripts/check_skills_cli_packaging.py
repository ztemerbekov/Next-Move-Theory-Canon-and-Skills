#!/usr/bin/env python3
"""Smoke-test installation and update through the supported skills CLI path."""

from __future__ import annotations

import hashlib
import os
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = {
    "nmt-analyze-interviews",
    "nmt-chat",
    "nmt-craft-go-to-market",
    "nmt-craft-value-proposition",
    "nmt-diagnose",
    "nmt-market-research",
    "nmt-product-requirements",
    "nmt-upgrade",
}
CANON_PROBE = "Advanced-Jobs-To-Be-Done/ajtbd-key-theses.md"
SHARED_CONTRACTS = {"producer-contract.md", "readability-contract.md"}


def run_cli(home: Path, consumer: Path) -> tuple[list[str], subprocess.CompletedProcess[str]]:
    env = os.environ.copy()
    env.update(
        {
            "HOME": str(home),
            "XDG_CONFIG_HOME": str(home / "config"),
            "XDG_DATA_HOME": str(home / "data"),
            "npm_config_cache": str(home / "npm-cache"),
            "PYTHONDONTWRITEBYTECODE": "1",
        }
    )
    command = [
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
    result = subprocess.run(
        command,
        cwd=consumer,
        env=env,
        capture_output=True,
        text=True,
        timeout=300,
        check=False,
    )
    return command, result


def tree_snapshot(root: Path) -> dict[str, str]:
    snapshot: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        if path.is_symlink():
            snapshot[relative] = f"symlink:{os.readlink(path)}"
        elif path.is_file():
            snapshot[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
        elif path.is_dir():
            snapshot[relative] = "directory"
    return snapshot


def source_status() -> str:
    result = subprocess.run(
        ["git", "status", "--porcelain=v1", "--untracked-files=all"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout


def inventory(root: Path) -> set[str]:
    if not root.is_dir():
        return set()
    return {path.name for path in root.iterdir() if path.name in SKILLS and path.is_dir()}


def find_installed_roots(home: Path) -> list[Path]:
    candidates: set[Path] = set()
    for name in SKILLS:
        for path in home.rglob(name):
            if path.is_dir():
                candidates.add(path.parent)
    return sorted(root for root in candidates if inventory(root) == SKILLS)


def installed_snapshot(roots: list[Path]) -> dict[str, str]:
    snapshot: dict[str, str] = {}
    for root in roots:
        for skill in sorted(SKILLS):
            skill_root = root / skill
            skill_file = skill_root / "SKILL.md"
            snapshot[f"{root}/{skill}/SKILL.md"] = hashlib.sha256(skill_file.read_bytes()).hexdigest()
        probe = root / "nmt-chat/references/Next-Move-Theory-Canon" / CANON_PROBE
        snapshot[f"{root}/canon-probe"] = hashlib.sha256(probe.read_bytes()).hexdigest()
    return snapshot


def verify_install(home: Path) -> tuple[list[str], list[Path]]:
    errors: list[str] = []
    roots = find_installed_roots(home)
    if len(roots) != 2:
        return [f"expected separate Codex and Claude Code Skill roots, found {roots}"], roots

    for root in roots:
        references = root / "nmt-chat/references"
        actual_contracts = {path.name for path in references.iterdir() if path.is_file()}
        if actual_contracts != SHARED_CONTRACTS:
            errors.append(
                f"{root}: expected shared contracts {sorted(SHARED_CONTRACTS)}, "
                f"found {sorted(actual_contracts)}"
            )
        canon = references / "Next-Move-Theory-Canon"
        if not (canon / CANON_PROBE).is_file():
            errors.append(f"{root}: bundled Canon probe is unreadable")

        for skill in sorted(SKILLS):
            skill_root = root / skill
            skill_file = skill_root / "SKILL.md"
            if not skill_file.is_file():
                errors.append(f"{root}: missing {skill}/SKILL.md")
                continue
            text = skill_file.read_text(encoding="utf-8")
            anchor = (
                "references/Next-Move-Theory-Canon/"
                if skill == "nmt-chat"
                else "../nmt-chat/references/Next-Move-Theory-Canon/"
            )
            if anchor not in text or not (skill_root / anchor).resolve().is_dir():
                errors.append(f"{root}: {skill} cannot resolve the bundled Canon")
    return errors, roots


def main() -> int:
    errors: list[str] = []
    before_source = source_status()
    with tempfile.TemporaryDirectory(prefix="nmt-skills-cli-") as temporary:
        temporary_root = Path(temporary)
        home = temporary_root / "home"
        consumer = temporary_root / "consumer"
        home.mkdir()
        consumer.mkdir()
        (consumer / "consumer.md").write_text("Unrelated consumer fixture.\n", encoding="utf-8")
        before_consumer = tree_snapshot(consumer)

        command, first = run_cli(home, consumer)
        if first.returncode:
            output = (first.stdout + first.stderr).strip()[-3000:]
            print(f"FAIL: skills CLI install failed ({first.returncode}): {' '.join(command)}\n{output}")
            return 1
        first_errors, roots = verify_install(home)
        errors.extend(first_errors)
        if not first_errors:
            before_install = installed_snapshot(roots)
            _, second = run_cli(home, consumer)
            if second.returncode:
                output = (second.stdout + second.stderr).strip()[-3000:]
                errors.append(f"repeated install/update failed ({second.returncode}): {output}")
            else:
                second_errors, updated_roots = verify_install(home)
                errors.extend(second_errors)
                if not second_errors and before_install != installed_snapshot(updated_roots):
                    errors.append("repeated install/update changed the installed package snapshot")

        if before_consumer != tree_snapshot(consumer):
            errors.append("installation changed the Consumer project")

    if before_source != source_status():
        errors.append("installation changed the source checkout")
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print("PASS: skills CLI installed all eight Skills for Codex and Claude Code")
    print("PASS: bundled Canon and contracts resolve after install and repeated update")
    print("PASS: Consumer project and source checkout remained unchanged")
    return 0


if __name__ == "__main__":
    sys.exit(main())
