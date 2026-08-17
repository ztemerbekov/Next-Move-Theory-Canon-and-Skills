#!/usr/bin/env python3
"""Validate the current eight-Skill package without encoding migration history."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote


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
CANON_ROOT = ROOT / "skills/nmt-chat/references/Next-Move-Theory-Canon"
INSTALL_COMMAND = (
    "npx skills@latest add ztemerbekov/Next-Move-Theory-Canon-and-Skills "
    "--skill '*' -a codex -a claude-code -g -y"
)
LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
NAME = re.compile(r"(?m)^name:\s*([^\s]+)\s*$")
DESCRIPTION = re.compile(r"(?m)^description:\s*(?:>\-|>\+|>|\|\-|\|\+|\||\S)")
FRONTMATTER_KEY = re.compile(r"(?m)^([A-Za-z0-9_-]+):")
ALLOWED_FRONTMATTER = {"name", "description", "license", "allowed-tools", "metadata"}


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def check_skill_inventory(errors: list[str]) -> None:
    skills_root = ROOT / "skills"
    actual = {
        path.name
        for path in skills_root.iterdir()
        if path.is_dir() and not path.name.startswith(".")
    }
    if actual != SKILLS:
        fail(errors, f"Skill inventory differs: expected={sorted(SKILLS)}, actual={sorted(actual)}")

    for skill in sorted(SKILLS):
        skill_root = skills_root / skill
        skill_file = skill_root / "SKILL.md"
        if not skill_file.is_file():
            fail(errors, f"missing skills/{skill}/SKILL.md")
            continue
        text = skill_file.read_text(encoding="utf-8")
        if not text.startswith("---\n") or "\n---\n" not in text[4:]:
            fail(errors, f"skills/{skill}/SKILL.md: malformed YAML frontmatter")
            continue
        frontmatter = text[4:text.index("\n---\n", 4)]
        unexpected = set(FRONTMATTER_KEY.findall(frontmatter)) - ALLOWED_FRONTMATTER
        if unexpected:
            fail(errors, f"skills/{skill}/SKILL.md: unexpected frontmatter keys {sorted(unexpected)}")
        match = NAME.search(text)
        if not match or match.group(1) != skill:
            fail(errors, f"skills/{skill}/SKILL.md: frontmatter name must equal directory name")
        if not DESCRIPTION.search(text):
            fail(errors, f"skills/{skill}/SKILL.md: non-empty description is required")

        anchor = (
            "references/Next-Move-Theory-Canon/"
            if skill == "nmt-chat"
            else "../nmt-chat/references/Next-Move-Theory-Canon/"
        )
        if anchor not in text:
            fail(errors, f"skills/{skill}/SKILL.md: missing bundled Canon anchor {anchor}")
        elif not (skill_root / anchor).resolve().is_dir():
            fail(errors, f"skills/{skill}/SKILL.md: Canon anchor does not resolve")

def check_shared_payload(errors: list[str]) -> None:
    if not CANON_ROOT.is_dir():
        fail(errors, "bundled Canon payload is missing")
    canon_roots = sorted(
        path
        for path in ROOT.rglob("Next-Move-Theory-Canon")
        if path.is_dir() and ".git" not in path.parts
    )
    if canon_roots != [CANON_ROOT]:
        found = [path.relative_to(ROOT).as_posix() for path in canon_roots]
        fail(errors, f"expected one bundled Canon root, found {found}")

    shared_root = ROOT / "skills/nmt-chat/references"
    expected = {"producer-contract.md", "readability-contract.md"}
    actual = {path.name for path in shared_root.iterdir() if path.is_file()}
    if actual != expected:
        fail(errors, f"shared contracts differ: expected={sorted(expected)}, actual={sorted(actual)}")


def markdown_files() -> list[Path]:
    top_level = [ROOT / name for name in ("README.md", "AGENTS.md", "CLAUDE.md", "CHANGELOG.md", "NOTICE.md")]
    docs = [ROOT / "docs/installation.md"]
    skills = [
        path
        for path in (ROOT / "skills").rglob("*.md")
        if CANON_ROOT not in path.parents
    ]
    return top_level + docs + skills


def link_target(raw: str) -> str:
    target = raw.strip()
    if target.startswith("<") and ">" in target:
        return target[1:target.index(">")]
    return target.split(maxsplit=1)[0]


def check_local_links(errors: list[str]) -> None:
    for source in markdown_files():
        if not source.is_file():
            fail(errors, f"missing maintained Markdown file: {source.relative_to(ROOT)}")
            continue
        text = source.read_text(encoding="utf-8")
        for raw in LINK.findall(text):
            target = link_target(raw)
            if (
                not target
                or target in {"url", "…"}
                or target.startswith(("#", "http://", "https://", "mailto:"))
            ):
                continue
            relative = unquote(target.split("#", 1)[0])
            resolved = (source.parent / relative).resolve()
            if not resolved.exists():
                fail(errors, f"{source.relative_to(ROOT)}: broken local link {target}")


def check_documented_install(errors: list[str]) -> None:
    for relative in ("README.md", "docs/installation.md"):
        text = (ROOT / relative).read_text(encoding="utf-8")
        if INSTALL_COMMAND not in text:
            fail(errors, f"{relative}: supported installation command is missing or changed")


def check_manifests(errors: list[str]) -> None:
    result = subprocess.run(
        [sys.executable, "-B", str(ROOT / "scripts/check_plugin_manifests.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode:
        fail(errors, (result.stdout + result.stderr).strip())


def main() -> int:
    errors: list[str] = []
    check_skill_inventory(errors)
    check_shared_payload(errors)
    check_local_links(errors)
    check_documented_install(errors)
    check_manifests(errors)
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print("PASS: eight Skills, shared contracts, and one bundled Canon are internally consistent")
    print("PASS: maintained Markdown links, installation command, and Plugin manifests are valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
