#!/usr/bin/env python3
"""Run the deterministic, read-only static validation suite for the Plugin."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = "next-move-theory"
VERSION = "1.0.0"
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
FRONTMATTER_KEYS = frozenset({"name", "description"})
PROHIBITED_COMPONENTS = frozenset({"agents", "hooks", "mcpServers", "apps"})
CANON_FILES = frozenset(
    {
        "ABCDX-Segmentation/abcdx-segmentation-key-theses.md",
        "Advanced-Jobs-To-Be-Done/ajtbd-key-theses.md",
        "Advanced-Jobs-To-Be-Done/b2b.md",
        "Advanced-Jobs-To-Be-Done/barrier-removal.md",
        "Advanced-Jobs-To-Be-Done/behaviour-change.md",
        "Advanced-Jobs-To-Be-Done/communication.md",
        "Advanced-Jobs-To-Be-Done/consideration-activators.md",
        "Advanced-Jobs-To-Be-Done/critical-chain.md",
        "Advanced-Jobs-To-Be-Done/customers-attention-management.md",
        "Advanced-Jobs-To-Be-Done/job-graph.md",
        "Advanced-Jobs-To-Be-Done/job-structure.md",
        "Advanced-Jobs-To-Be-Done/job-types-and-properties.md",
        "Advanced-Jobs-To-Be-Done/scientific-foundations.md",
        "Advanced-Jobs-To-Be-Done/segmentation.md",
        "Advanced-Jobs-To-Be-Done/value-creation-mechanics.md",
        "Advanced-Jobs-To-Be-Done/value-creation.md",
        "Algorithms/the-algorithm.md",
        "HowTos/basic-ajtbd-interview-guide-and-principles.md",
        "Next-Move-Theory/focus-as-company-attention-management.md",
        "Next-Move-Theory/local-vs-global-optimum.md",
        "Next-Move-Theory/nmt-key-theses.md",
        "Next-Move-Theory/subtraction.md",
        "Riskiest-Assumption-Test/rat-key-theses.md",
    }
)
CANON_ROOT = Path("skills/nmt-chat/references/Next-Move-Theory-Canon")
SHARED_REFERENCE_FILES = frozenset(
    {
        "canon-routing.md",
        "client-adapters.md",
        "methodology-guardrails.md",
        "producer-contract.md",
        "readability-contract.md",
        "skill-routing.md",
    }
)
CANON_PATH_RE = re.compile(
    r"(?<![A-Za-z0-9-])((?:references/|\.\./nmt-chat/references/)"
    r"Next-Move-Theory-Canon/[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)*)"
)
REFERENCE_PATH_RE = re.compile(
    r"(?<![A-Za-z0-9-])(\.\./nmt-chat/references/"
    r"[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)*)"
)
OLD_REFERENCE_RE = re.compile(r"\.\./(?:PRODUCER|READABILITY)-CONTRACT\.md")
FRONTMATTER_KEY_RE = re.compile(r"^([A-Za-z0-9_-]+):(?:\s*(.*))?$")


def relative(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def add_error(errors: list[str], root: Path, path: Path, line: int | None, message: str) -> None:
    location = relative(path, root)
    if line is not None:
        errors.append(f"{location}:{line}: {message}")
    else:
        errors.append(f"{location}: {message}")


def read_json(root: Path, relative_path: str, errors: list[str]) -> Any:
    path = root / relative_path
    if not path.is_file():
        add_error(errors, root, path, None, "missing JSON file")
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        add_error(errors, root, path, None, f"invalid JSON: {error}")
        return None


def require_mapping(value: Any, label: str, errors: list[str]) -> dict[str, Any] | None:
    if not isinstance(value, dict):
        errors.append(f"{label}: expected a JSON object")
        return None
    return value


def require_keys(value: dict[str, Any], keys: set[str], label: str, errors: list[str]) -> None:
    for key in sorted(keys - set(value)):
        errors.append(f"{label}: missing required key `{key}`")


def assert_value(
    value: dict[str, Any], key: str, expected: Any, label: str, errors: list[str]
) -> None:
    if value.get(key) != expected:
        errors.append(f"{label}.{key}: expected {expected!r}, got {value.get(key)!r}")


def assert_prohibited(value: Any, label: str, errors: list[str]) -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            if key in PROHIBITED_COMPONENTS:
                errors.append(f"{label}: prohibited component `{key}` is declared")
            assert_prohibited(child, f"{label}.{key}", errors)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            assert_prohibited(child, f"{label}[{index}]", errors)


def check_manifests(root: Path, errors: list[str]) -> None:
    codex = require_mapping(read_json(root, ".codex-plugin/plugin.json", errors), "Codex manifest", errors)
    claude = require_mapping(read_json(root, ".claude-plugin/plugin.json", errors), "Claude manifest", errors)
    claude_marketplace = require_mapping(
        read_json(root, ".claude-plugin/marketplace.json", errors),
        "Claude marketplace",
        errors,
    )
    codex_marketplace = require_mapping(
        read_json(root, ".agents/plugins/marketplace.json", errors),
        "Codex marketplace",
        errors,
    )

    if codex is not None:
        require_keys(
            codex,
            {"name", "version", "description", "author", "skills", "interface"},
            "Codex manifest",
            errors,
        )
        assert_value(codex, "name", PLUGIN, "Codex manifest", errors)
        assert_value(codex, "version", VERSION, "Codex manifest", errors)
        if not isinstance(codex.get("description"), str) or not codex["description"].strip():
            errors.append("Codex manifest.description: must be a non-empty string")
        author = require_mapping(codex.get("author"), "Codex manifest.author", errors)
        if author is not None and not isinstance(author.get("name"), str):
            errors.append("Codex manifest.author.name: must be a string")
        interface = require_mapping(codex.get("interface"), "Codex manifest.interface", errors)
        if interface is not None:
            require_keys(
                interface,
                {
                    "displayName",
                    "shortDescription",
                    "longDescription",
                    "developerName",
                    "category",
                    "capabilities",
                    "defaultPrompt",
                },
                "Codex manifest.interface",
                errors,
            )
            if not isinstance(interface.get("capabilities"), list):
                errors.append("Codex manifest.interface.capabilities: must be an array")
            if not isinstance(interface.get("defaultPrompt"), list):
                errors.append("Codex manifest.interface.defaultPrompt: must be an array")
        assert_value(codex, "skills", "./skills/", "Codex manifest", errors)
        skills_path = (root / "skills").resolve()
        if not skills_path.is_dir():
            errors.append("Codex manifest.skills: ./skills/ does not resolve to a directory")
        else:
            try:
                skills_path.relative_to(root.resolve())
            except ValueError:
                errors.append("Codex manifest.skills: path leaves the Plugin root")
        assert_prohibited(codex, "Codex manifest", errors)

    if claude is not None:
        require_keys(
            claude,
            {"name", "version", "description", "author"},
            "Claude manifest",
            errors,
        )
        assert_value(claude, "name", PLUGIN, "Claude manifest", errors)
        assert_value(claude, "version", VERSION, "Claude manifest", errors)
        if not isinstance(claude.get("description"), str) or not claude["description"].strip():
            errors.append("Claude manifest.description: must be a non-empty string")
        author = require_mapping(claude.get("author"), "Claude manifest.author", errors)
        if author is not None and not isinstance(author.get("name"), str):
            errors.append("Claude manifest.author.name: must be a string")
        assert_prohibited(claude, "Claude manifest", errors)

    if claude_marketplace is not None:
        require_keys(
            claude_marketplace,
            {"name", "owner", "plugins"},
            "Claude marketplace",
            errors,
        )
        assert_value(claude_marketplace, "name", PLUGIN, "Claude marketplace", errors)
        owner = require_mapping(claude_marketplace.get("owner"), "Claude marketplace.owner", errors)
        if owner is not None and not isinstance(owner.get("name"), str):
            errors.append("Claude marketplace.owner.name: must be a string")
        entries = claude_marketplace.get("plugins")
        if not isinstance(entries, list) or len(entries) != 1:
            errors.append("Claude marketplace.plugins: expected exactly one entry")
        elif isinstance(entries[0], dict):
            entry = entries[0]
            assert_value(entry, "name", PLUGIN, "Claude marketplace entry", errors)
            assert_value(entry, "source", "./", "Claude marketplace entry", errors)
            assert_value(entry, "strict", True, "Claude marketplace entry", errors)
        assert_prohibited(claude_marketplace, "Claude marketplace", errors)

    if codex_marketplace is not None:
        require_keys(
            codex_marketplace,
            {"name", "interface", "plugins"},
            "Codex marketplace",
            errors,
        )
        assert_value(codex_marketplace, "name", PLUGIN, "Codex marketplace", errors)
        interface = require_mapping(codex_marketplace.get("interface"), "Codex marketplace.interface", errors)
        if interface is not None and not isinstance(interface.get("displayName"), str):
            errors.append("Codex marketplace.interface.displayName: must be a string")
        entries = codex_marketplace.get("plugins")
        if not isinstance(entries, list) or len(entries) != 1:
            errors.append("Codex marketplace.plugins: expected exactly one entry")
        elif isinstance(entries[0], dict):
            entry = entries[0]
            assert_value(entry, "name", PLUGIN, "Codex marketplace entry", errors)
            source = require_mapping(entry.get("source"), "Codex marketplace entry.source", errors)
            if source is not None:
                assert_value(source, "source", "url", "Codex marketplace source", errors)
                assert_value(
                    source,
                    "url",
                    "https://github.com/ztemerbekov/Next-Move-Theory-Canon-and-Skills.git",
                    "Codex marketplace source",
                    errors,
                )
                assert_value(source, "ref", "main", "Codex marketplace source", errors)
            assert_value(
                entry,
                "policy",
                {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
                "Codex marketplace entry",
                errors,
            )
            assert_value(entry, "category", "Productivity", "Codex marketplace entry", errors)
        assert_prohibited(codex_marketplace, "Codex marketplace", errors)


def check_versions(root: Path, errors: list[str]) -> None:
    specification = root / "docs/repository-migration-specification.md"
    changelog = root / "CHANGELOG.md"
    if not specification.is_file():
        add_error(errors, root, specification, None, "missing locked migration specification")
    elif not re.search(r"^Release: `1\.0\.0`$", specification.read_text(encoding="utf-8"), re.MULTILINE):
        add_error(errors, root, specification, None, "locked specification does not declare Release: `1.0.0`")
    if not changelog.is_file():
        add_error(errors, root, changelog, None, "missing CHANGELOG.md")
    elif not re.search(r"^## 1\.0\.0(?:\s|$)", changelog.read_text(encoding="utf-8"), re.MULTILINE):
        add_error(errors, root, changelog, None, "CHANGELOG.md has no 1.0.0 release entry")


def check_inventory(root: Path, errors: list[str]) -> None:
    canon = root / CANON_ROOT
    if not canon.is_dir():
        errors.append(f"{CANON_ROOT}: bundled Canon root is missing")
    else:
        actual = {
            path.relative_to(canon).as_posix()
            for path in canon.rglob("*")
            if path.is_file()
        }
        if actual != CANON_FILES:
            errors.append(
                f"{CANON_ROOT}: exact inventory changed; "
                f"missing={sorted(CANON_FILES - actual)}, unexpected={sorted(actual - CANON_FILES)}"
            )

    canon_roots = sorted(
        path.relative_to(root).as_posix()
        for path in root.rglob("Next-Move-Theory-Canon")
        if path.is_dir() and ".git" not in path.parts
    )
    expected_canon_root = CANON_ROOT.as_posix()
    if canon_roots != [expected_canon_root]:
        errors.append(
            "Next-Move-Theory-Canon: expected exactly one physical payload root; "
            f"found={canon_roots}"
        )

    shared_root = root / "skills/nmt-chat/references"
    actual_shared = {
        path.name
        for path in shared_root.iterdir()
        if path.is_file()
    } if shared_root.is_dir() else set()
    if actual_shared & {"Next-Move-Theory-Canon"}:
        actual_shared.remove("Next-Move-Theory-Canon")
    if actual_shared != SHARED_REFERENCE_FILES:
        errors.append(
            "skills/nmt-chat/references/: shared-reference inventory changed; "
            f"expected={sorted(SHARED_REFERENCE_FILES)}, actual={sorted(actual_shared)}"
        )
    if (root / "references").exists():
        errors.append("references/: retired root shared-reference directory remains")

    skills_root = root / "skills"
    if not skills_root.is_dir():
        errors.append("skills/: shared Skill source tree is missing")
        return
    actual_skills = {
        path.name for path in skills_root.iterdir() if path.is_dir() and not path.name.startswith(".")
    }
    if actual_skills != SKILLS:
        errors.append(
            f"skills/: exact inventory changed; expected={sorted(SKILLS)}, actual={sorted(actual_skills)}"
        )
    for skill in sorted(SKILLS):
        entry = skills_root / skill / "SKILL.md"
        if not entry.is_file():
            errors.append(f"{relative(entry, root)}: Skill entry point is missing")


def parse_frontmatter(path: Path) -> tuple[dict[str, int], list[str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    keys: dict[str, int] = {}
    errors: list[str] = []
    if not lines or lines[0] != "---":
        errors.append("frontmatter must start with `---`")
        return keys, errors
    closing = next((index for index in range(1, len(lines)) if lines[index] == "---"), None)
    if closing is None:
        errors.append("frontmatter has no closing `---`")
        return keys, errors
    for index, line in enumerate(lines[1:closing], start=2):
        match = FRONTMATTER_KEY_RE.match(line)
        if match:
            keys[match.group(1)] = index
        elif line and not line[0].isspace():
            errors.append(f"frontmatter line {index} is not a key/value entry")
    return keys, errors


def check_frontmatter_and_paths(root: Path, errors: list[str]) -> None:
    skills_root = root / "skills"
    if not skills_root.is_dir():
        return
    for path in sorted(skills_root.rglob("*.md")):
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as error:
            add_error(errors, root, path, None, f"cannot read Skill source: {error}")
            continue
        if path.name == "SKILL.md":
            keys, frontmatter_errors = parse_frontmatter(path)
            for message in frontmatter_errors:
                add_error(errors, root, path, None, message)
            for key, line in sorted(keys.items()):
                if key not in FRONTMATTER_KEYS:
                    add_error(errors, root, path, line, f"non-portable frontmatter key `{key}`")
            if "user-invocable" in keys:
                add_error(errors, root, path, keys["user-invocable"], "Codex-incompatible `user-invocable` metadata")
            expected_name = path.parent.name
            if "name" not in keys:
                add_error(errors, root, path, 2, "frontmatter is missing `name`")
            elif not re.search(rf"^name:\s*{re.escape(expected_name)}\s*$", text, re.MULTILINE):
                add_error(errors, root, path, keys["name"], f"frontmatter name must be `{expected_name}`")
            if "description" not in keys:
                add_error(errors, root, path, 2, "frontmatter is missing `description`")

        for match in CANON_PATH_RE.finditer(text):
            target = match.group(1)
            if target.endswith("/..."):
                continue
            resolved = (path.parent / target).resolve()
            line = text.count("\n", 0, match.start()) + 1
            try:
                resolved.relative_to(root.resolve())
            except ValueError:
                add_error(errors, root, path, line, f"Canon path leaves the Plugin root: {target}")
                continue
            if not resolved.is_file():
                add_error(errors, root, path, line, f"Canon path does not resolve: {target}")

        for match in REFERENCE_PATH_RE.finditer(text):
            target = match.group(1)
            if "Next-Move-Theory-Canon" in target:
                continue
            resolved = (path.parent / target).resolve()
            line = text.count("\n", 0, match.start()) + 1
            try:
                resolved.relative_to(root.resolve())
            except ValueError:
                add_error(errors, root, path, line, f"reference path leaves the Plugin root: {target}")
                continue
            if not resolved.is_file():
                add_error(errors, root, path, line, f"reference path does not resolve: {target}")

        old_reference = OLD_REFERENCE_RE.search(text)
        if old_reference:
            line = text.count("\n", 0, old_reference.start()) + 1
            add_error(errors, root, path, line, "retired shared-contract path remains")


def check_required_anchors(root: Path, errors: list[str]) -> None:
    producer_skills = SKILLS - {"nmt-chat", "nmt-upgrade"}
    for skill in sorted(SKILLS):
        path = root / "skills" / skill / "SKILL.md"
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        anchor = (
            "references/Next-Move-Theory-Canon/"
            if skill == "nmt-chat"
            else "../nmt-chat/references/Next-Move-Theory-Canon/"
        )
        if anchor not in text:
            errors.append(f"{path.relative_to(root)}: required Canon anchor is not declared: {anchor}")
        elif not (path.parent / anchor).resolve().is_dir():
            errors.append(f"{path.relative_to(root)}: required Canon anchor does not resolve: {anchor}")

        if skill in producer_skills:
            contract = "../nmt-chat/references/producer-contract.md"
            if contract not in text:
                errors.append(
                    f"{path.relative_to(root)}: producer Skill does not declare shared contract: {contract}"
                )
            elif not (path.parent / contract).resolve().is_file():
                errors.append(f"{path.relative_to(root)}: shared producer contract does not resolve: {contract}")


def check_package_contract(root: Path) -> list[str]:
    errors: list[str] = []
    check_manifests(root, errors)
    check_versions(root, errors)
    check_inventory(root, errors)
    check_frontmatter_and_paths(root, errors)
    check_required_anchors(root, errors)
    return errors


def run_existing_checks() -> list[str]:
    failures: list[str] = []
    for script in (
        "scripts/check_plugin_manifests.py",
        "scripts/verify-source-consolidation.py",
        "scripts/check_adapter_drift.py",
    ):
        print(f"== {script} ==")
        result = subprocess.run(
            [sys.executable, str(ROOT / script)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        output = (result.stdout + result.stderr).strip()
        if output:
            print(output)
        if result.returncode:
            failures.append(f"{script} exited with status {result.returncode}")
    return failures


def copy_package_fixture(source: Path, destination: Path) -> None:
    for relative_path in (
        ".agents",
        ".claude-plugin",
        ".codex-plugin",
        "skills",
        "docs",
        "CHANGELOG.md",
    ):
        source_path = source / relative_path
        destination_path = destination / relative_path
        if source_path.is_dir():
            shutil.copytree(source_path, destination_path)
        else:
            destination_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_path, destination_path)


def run_negative_fixture_tests() -> list[str]:
    failures: list[str] = []
    with tempfile.TemporaryDirectory(prefix="nmt-static-validation-") as temporary:
        fixture_root = Path(temporary)

        nested_fixture = fixture_root / "nested-canon"
        copy_package_fixture(ROOT, nested_fixture)
        nested = nested_fixture / CANON_ROOT / "fixture" / "Next-Move-Theory-Canon"
        nested.mkdir(parents=True)
        (nested / "unexpected.md").write_text("fixture\n", encoding="utf-8")
        nested_errors = check_package_contract(nested_fixture)
        if not any("exactly one physical payload root" in error for error in nested_errors):
            failures.append("self-test: duplicate Canon fixture was not rejected")

        missing_anchor_fixture = fixture_root / "missing-anchor"
        copy_package_fixture(ROOT, missing_anchor_fixture)
        missing_probe = missing_anchor_fixture / CANON_ROOT / "Advanced-Jobs-To-Be-Done/ajtbd-key-theses.md"
        missing_probe.unlink()
        missing_errors = check_package_contract(missing_anchor_fixture)
        if not any("Canon path does not resolve" in error for error in missing_errors):
            failures.append("self-test: missing Canon anchor fixture was not rejected")

        metadata_fixture = fixture_root / "user-invocable"
        copy_package_fixture(ROOT, metadata_fixture)
        skill = metadata_fixture / "skills/nmt-chat/SKILL.md"
        lines = skill.read_text(encoding="utf-8").splitlines()
        closing = lines.index("---", 1)
        lines.insert(closing, "user-invocable: true")
        skill.write_text("\n".join(lines) + "\n", encoding="utf-8")
        metadata_errors = check_package_contract(metadata_fixture)
        if not any("user-invocable" in error for error in metadata_errors):
            failures.append("self-test: user-invocable fixture was not rejected")
    return failures


def main() -> int:
    failures = run_existing_checks()

    print("== package contract ==")
    package_errors = check_package_contract(ROOT)
    if package_errors:
        failures.extend(f"package contract: {error}" for error in package_errors)
        for error in package_errors:
            print(f"FAIL: {error}")
    else:
        print("PASS: manifests, version, Canon inventory, Skill frontmatter, and package paths")

    print("== negative fixture tests ==")
    fixture_errors = run_negative_fixture_tests()
    if fixture_errors:
        failures.extend(fixture_errors)
        for error in fixture_errors:
            print(f"FAIL: {error}")
    else:
        print("PASS: nested Canon and user-invocable incompatibility fixtures are rejected")

    if failures:
        print("STATIC VALIDATION FAILED")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("STATIC VALIDATION PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
