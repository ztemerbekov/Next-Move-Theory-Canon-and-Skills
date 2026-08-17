#!/usr/bin/env python3
"""Validate the current public installation, attribution, and documentation contract."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INSTALL_COMMAND = (
    "npx skills@latest add ztemerbekov/Next-Move-Theory-Canon-and-Skills "
    "--skill '*' -a codex -a claude-code -g -y"
)
PUBLIC_DOCS = (
    ROOT / "README.md",
    ROOT / "CHANGELOG.md",
    ROOT / "AGENTS.md",
    ROOT / "CLAUDE.md",
    ROOT / "NOTICE.md",
    *sorted((ROOT / "docs").glob("*.md")),
    *sorted((ROOT / "docs/migration").glob("*.md")),
)
LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
FORBIDDEN_COMMANDS = (
    "curl -fsSL https://nextmovetheory.com/install.sh | bash",
    "irm https://nextmovetheory.com/install.ps1 | iex",
    "bash install.sh --target",
    "powershell -ExecutionPolicy Bypass -File install.ps1",
)


def report(errors: list[str], path: Path, message: str) -> None:
    errors.append(f"{path.relative_to(ROOT).as_posix()}: {message}")


def check_required_files(errors: list[str]) -> None:
    for relative_path in ("install.sh", "install.ps1", "docs/legacy-installer.md"):
        path = ROOT / relative_path
        if path.exists():
            report(errors, path, "removed Legacy artifact is still present")


def check_notice(errors: list[str]) -> None:
    path = ROOT / "NOTICE.md"
    if not path.is_file():
        report(errors, path, "NOTICE.md is missing")
        return
    text = path.read_text(encoding="utf-8")
    required = (
        "Ivan Zamesin",
        "https://github.com/zamesin/Next-Move-Theory-Canon-and-Skills",
        "CC BY-NC-SA 4.0",
        "packaging",
        "path",
        "endorsement",
    )
    for phrase in required:
        if phrase.lower() not in text.lower():
            report(errors, path, f"required attribution phrase is missing: {phrase!r}")


def check_installation_docs(errors: list[str]) -> None:
    for relative_path in ("README.md", "docs/installation.md", "docs/updates.md", "docs/migration.md"):
        path = ROOT / relative_path
        if not path.is_file():
            report(errors, path, "required public documentation is missing")
            continue
        text = path.read_text(encoding="utf-8")
        if INSTALL_COMMAND not in text:
            report(errors, path, "exact supported skills CLI command is missing")

    installation = (ROOT / "docs/installation.md").read_text(encoding="utf-8")
    for phrase in ("partial", "unsupported", "nmt-upgrade", "Consumer project"):
        if phrase.lower() not in installation.lower():
            report(errors, ROOT / "docs/installation.md", f"installation boundary is missing: {phrase!r}")

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    if "npx install latest" in readme:
        report(errors, ROOT / "README.md", "obsolete unrelated npx command warning remains")
    if re.search(r"^#+\s+Windows(?:\s+installation)?\s*$", readme, re.IGNORECASE | re.MULTILINE):
        report(errors, ROOT / "README.md", "separate Windows installation section remains")


def check_live_docs_for_removed_commands(errors: list[str]) -> None:
    for path in PUBLIC_DOCS:
        if not path.is_file():
            report(errors, path, "public documentation file is missing")
            continue
        text = path.read_text(encoding="utf-8")
        for command in FORBIDDEN_COMMANDS:
            if command in text:
                report(errors, path, f"removed Legacy installer command is still documented: {command!r}")
        if "docs/legacy-installer.md" in text:
            report(errors, path, "removed Legacy installer documentation is still linked")


def check_local_links(errors: list[str]) -> None:
    for path in PUBLIC_DOCS:
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for match in LINK_RE.finditer(text):
            target = match.group(1).strip()
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = target.split("#", 1)[0].split("?", 1)[0].strip("<>")
            if not target:
                continue
            resolved = (path.parent / target).resolve()
            if not resolved.exists():
                line = text.count("\n", 0, match.start()) + 1
                report(errors, path, f"line {line}: local Markdown link does not resolve: {target}")


def validate() -> list[str]:
    errors: list[str] = []
    check_required_files(errors)
    check_notice(errors)
    check_installation_docs(errors)
    check_live_docs_for_removed_commands(errors)
    check_local_links(errors)
    return errors


def main() -> int:
    errors = validate()
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        print("PUBLIC DISTRIBUTION VALIDATION FAILED")
        return 1
    print("PASS: public installation, attribution, Legacy boundary, and local documentation links")
    return 0


if __name__ == "__main__":
    sys.exit(main())
