#!/usr/bin/env python3
"""Validate the hand-authored Client adapter registry and source boundary."""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "skills" / "nmt-chat" / "references" / "client-adapters.md"
EXPECTED_ADAPTERS = {
    "Invocation spelling and namespacing",
    "Interactive-question tooling and limits",
    "Agent/subagent executor lifecycle",
    "Client discovery and installed-Canon path anchors",
    "Codex `user-invocable` validator compatibility",
}
EXPECTED_SKILLS = {
    "nmt-analyze-interviews",
    "nmt-chat",
    "nmt-craft-go-to-market",
    "nmt-craft-value-proposition",
    "nmt-diagnose",
    "nmt-market-research",
    "nmt-product-requirements",
    "nmt-upgrade",
}
EXPECTED_SHARED_REFERENCES = {
    "skills/nmt-chat/references/producer-contract.md",
    "skills/nmt-chat/references/readability-contract.md",
    "skills/nmt-chat/references/canon-routing.md",
    "skills/nmt-chat/references/skill-routing.md",
    "skills/nmt-chat/references/methodology-guardrails.md",
}
INVENTORY_RE = re.compile(r"^\| `([^`]+)` \| `([0-9a-f]{64})` \|$", re.MULTILINE)
HEADING_RE = re.compile(r"^### \d+\. (.+)$", re.MULTILINE)
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
FORBIDDEN_CACHE_RE = re.compile(
    r"(?:~/(?:\.claude|\.codex)|/plugins/cache|file://|/Users/|/private/tmp/)"
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def source_files() -> set[str]:
    skills = {
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "skills").rglob("*.md")
        if "Next-Move-Theory-Canon" not in path.parts and path != REGISTRY
    }
    return skills | EXPECTED_SHARED_REFERENCES


def validate_registry(errors: list[str]) -> str:
    if not REGISTRY.is_file():
        errors.append("missing references/client-adapters.md")
        return ""
    text = REGISTRY.read_text(encoding="utf-8")
    headings = set(HEADING_RE.findall(text))
    if headings != EXPECTED_ADAPTERS:
        errors.append(
            "adapter headings differ from the five proven boundaries: "
            f"expected {sorted(EXPECTED_ADAPTERS)}, got {sorted(headings)}"
        )
    for heading in EXPECTED_ADAPTERS:
        match = re.search(
            rf"^### \d+\. {re.escape(heading)}$(.*?)(?=^### \d+\. |^## )",
            text,
            re.MULTILINE | re.DOTALL,
        )
        if match is None:
            errors.append(f"missing adapter entry: {heading}")
            continue
        entry = match.group(1)
        for field in (
            "**Client:**",
            "**Proven incompatibility:**",
            "**Evidence:**",
            "**Portable boundary:**",
            "**Drift check:**",
        ):
            if field not in entry:
                errors.append(f"adapter `{heading}` is missing {field}")
    inventory = dict(INVENTORY_RE.findall(text))
    expected = source_files()
    if set(inventory) != expected:
        errors.append(
            "shared-source fingerprint inventory differs from the package: "
            f"missing={sorted(expected - set(inventory))}, "
            f"unexpected={sorted(set(inventory) - expected)}"
        )
    for path_string, expected_hash in inventory.items():
        path = ROOT / path_string
        if not path.is_file():
            errors.append(f"declared shared-source path is missing: {path_string}")
            continue
        actual_hash = sha256(path)
        if actual_hash != expected_hash:
            errors.append(
                f"shared-source fingerprint changed: {path_string} "
                f"(expected {expected_hash}, got {actual_hash})"
            )
    return text


def validate_links(text: str, errors: list[str]) -> None:
    for raw_target in LINK_RE.findall(text):
        if raw_target.startswith(("https://", "http://", "#")):
            continue
        target = raw_target.split("#", 1)[0]
        path = (REGISTRY.parent / target).resolve()
        try:
            path.relative_to(ROOT)
        except ValueError:
            errors.append(f"registry link leaves the Plugin root: {raw_target}")
            continue
        if not path.exists():
            errors.append(f"registry link does not resolve: {raw_target}")


def validate_source_boundary(errors: list[str]) -> None:
    skills_root = ROOT / "skills"
    if not skills_root.is_dir():
        errors.append("missing shared skills/ source tree")
        return
    skill_dirs = {
        child.name
        for child in skills_root.iterdir()
        if child.is_dir() and not child.name.startswith(".")
    }
    if skill_dirs != EXPECTED_SKILLS:
        errors.append(
            f"Skill inventory drift: expected {sorted(EXPECTED_SKILLS)}, "
            f"got {sorted(skill_dirs)}"
        )
    for skill in EXPECTED_SKILLS:
        if not (skills_root / skill / "SKILL.md").is_file():
            errors.append(f"missing Skill entry point: skills/{skill}/SKILL.md")
    if any(
        child.is_dir() and child.name in {"claude", "codex"}
        for child in skills_root.iterdir()
    ):
        errors.append("a second Client-specific Skill tree exists under skills/")
    if any(child.name == "Skills" for child in ROOT.iterdir()):
        errors.append("retired root Skills/ tree exists beside the shared source")
    canon_roots = [
        path for path in ROOT.rglob("Next-Move-Theory-Canon")
        if path.is_dir() and ".git" not in path.parts
    ]
    expected_canon = ROOT / "skills/nmt-chat/references/Next-Move-Theory-Canon"
    if canon_roots != [expected_canon]:
        relative = [path.relative_to(ROOT).as_posix() for path in canon_roots]
        errors.append(f"Canon payload inventory differs: expected={[expected_canon.relative_to(ROOT).as_posix()]}, got={relative}")
    if (ROOT / "references").exists():
        errors.append("retired root references/ directory exists")

    for path_string in source_files():
        path = ROOT / path_string
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        match = FORBIDDEN_CACHE_RE.search(text)
        if match:
            line = text.count("\n", 0, match.start()) + 1
            errors.append(
                f"literal checkout/cache anchor in shared source: "
                f"{path_string}:{line}"
            )
        if "user-invocable" in text:
            errors.append(f"Codex-incompatible user-invocable metadata remains: {path_string}")


def main() -> int:
    errors: list[str] = []
    text = validate_registry(errors)
    if text:
        validate_links(text, errors)
    validate_source_boundary(errors)
    if errors:
        print("Adapter drift validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("PASS: five proven Client adapter entries are complete")
    print("PASS: registry links, source fingerprints, and Skill inventory are stable")
    print("PASS: no second Client Skill tree, literal cache anchor, or user-invocable metadata")
    return 0


if __name__ == "__main__":
    sys.exit(main())
