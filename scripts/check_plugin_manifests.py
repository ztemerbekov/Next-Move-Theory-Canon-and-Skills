#!/usr/bin/env python3
"""Check the repository-root Plugin manifests and marketplace catalogs."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
VERSION = "1.0.0"
PLUGIN = "next-move-theory"
SKILLS = {
    "nmt-analyze-interviews",
    "nmt-chat",
    "nmt-craft-go-to-market",
    "nmt-craft-value-proposition",
    "nmt-diagnose",
    "nmt-market-research",
    "nmt-product-requirements",
}
PROHIBITED = {"agents", "hooks", "mcpServers", "apps"}
CANON_ROOT = ROOT / "skills/nmt-chat/references/Next-Move-Theory-Canon"


def read_json(relative: str) -> dict[str, Any]:
    path = ROOT / relative
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise AssertionError(f"{relative}: invalid JSON ({error})") from error
    if not isinstance(value, dict):
        raise AssertionError(f"{relative}: top-level value must be an object")
    return value


def assert_equal(actual: Any, expected: Any, label: str) -> None:
    if actual != expected:
        raise AssertionError(f"{label}: expected {expected!r}, got {actual!r}")


def assert_no_prohibited(value: Any, label: str) -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            if key in PROHIBITED:
                raise AssertionError(f"{label}: prohibited component `{key}` is declared")
            assert_no_prohibited(child, f"{label}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            assert_no_prohibited(child, f"{label}[{index}]")


def check() -> None:
    codex = read_json(".codex-plugin/plugin.json")
    claude = read_json(".claude-plugin/plugin.json")
    claude_marketplace = read_json(".claude-plugin/marketplace.json")
    codex_marketplace = read_json(".agents/plugins/marketplace.json")

    for label, manifest in (("Codex plugin", codex), ("Claude plugin", claude)):
        assert_equal(manifest.get("name"), PLUGIN, f"{label} name")
        assert_equal(manifest.get("version"), VERSION, f"{label} version")
        assert_no_prohibited(manifest, label)

    assert_equal(codex.get("skills"), "./skills/", "Codex skills path")
    assert_equal(codex.get("interface", {}).get("category"), "Productivity", "Codex category")
    skill_dirs = {
        child.name
        for child in (ROOT / "skills").iterdir()
        if child.is_dir() and not child.name.startswith(".")
    }
    assert_equal(skill_dirs, SKILLS, "root Skill inventory")
    for skill in SKILLS:
        if not (ROOT / "skills" / skill / "SKILL.md").is_file():
            raise AssertionError(f"missing Skill entry point: skills/{skill}/SKILL.md")

    assert_equal(claude_marketplace.get("name"), PLUGIN, "Claude marketplace name")
    claude_entries = claude_marketplace.get("plugins")
    if not isinstance(claude_entries, list) or len(claude_entries) != 1:
        raise AssertionError("Claude marketplace must contain exactly one plugin entry")
    claude_entry = claude_entries[0]
    assert_equal(claude_entry.get("name"), PLUGIN, "Claude marketplace plugin name")
    assert_equal(claude_entry.get("source"), "./", "Claude marketplace source")
    assert_equal(claude_entry.get("strict"), True, "Claude marketplace strict mode")
    assert_no_prohibited(claude_marketplace, "Claude marketplace")

    assert_equal(codex_marketplace.get("name"), PLUGIN, "Codex marketplace name")
    codex_entries = codex_marketplace.get("plugins")
    if not isinstance(codex_entries, list) or len(codex_entries) != 1:
        raise AssertionError("Codex marketplace must contain exactly one plugin entry")
    codex_entry = codex_entries[0]
    assert_equal(codex_entry.get("name"), PLUGIN, "Codex marketplace plugin name")
    source = codex_entry.get("source")
    if not isinstance(source, dict):
        raise AssertionError("Codex marketplace source must be an object")
    assert_equal(source.get("source"), "url", "Codex marketplace source type")
    assert_equal(
        source.get("url"),
        "https://github.com/ztemerbekov/Next-Move-Theory-Canon-and-Skills.git",
        "Codex marketplace source URL",
    )
    assert_equal(source.get("ref"), "main", "Codex marketplace source ref")
    assert_equal(
        codex_entry.get("policy"),
        {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
        "Codex marketplace policy",
    )
    assert_equal(codex_entry.get("category"), "Productivity", "Codex marketplace category")
    assert_no_prohibited(codex_marketplace, "Codex marketplace")

    canon = CANON_ROOT
    if not canon.is_dir():
        raise AssertionError("bundled Canon payload is missing")
    canon_roots = [
        path for path in ROOT.rglob("Next-Move-Theory-Canon")
        if path.is_dir() and ".git" not in path.parts
    ]
    if canon_roots != [CANON_ROOT]:
        relative = [path.relative_to(ROOT).as_posix() for path in canon_roots]
        raise AssertionError(f"expected exactly one Canon payload root, found: {relative}")

    shared_root = ROOT / "skills/nmt-chat/references"
    expected_shared = {
        "producer-contract.md",
        "readability-contract.md",
    }
    actual_shared = {path.name for path in shared_root.iterdir() if path.is_file()}
    if actual_shared != expected_shared:
        raise AssertionError(
            f"shared-reference inventory differs: expected={sorted(expected_shared)}, "
            f"actual={sorted(actual_shared)}"
        )
    if (ROOT / "references").exists():
        raise AssertionError("retired root references/ directory remains")


def main() -> int:
    try:
        check()
    except AssertionError as error:
        print(f"FAIL: {error}")
        return 1
    print("PASS: repository-root Plugin manifests and marketplace catalogs agree")
    print("PASS: seven Skills, one Canon root, and no extra runtime components")
    return 0


if __name__ == "__main__":
    sys.exit(main())
