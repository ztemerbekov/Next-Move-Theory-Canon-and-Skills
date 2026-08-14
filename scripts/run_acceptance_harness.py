#!/usr/bin/env python3
"""Run clean-environment Plugin installation, smoke, update, and hygiene checks."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import signal
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = "next-move-theory"
MARKETPLACE = "next-move-theory"
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
CANON_PROBE = "Next-Move-Theory-Canon/Advanced-Jobs-To-Be-Done/ajtbd-key-theses.md"
AUTH_FAILURE_RE = re.compile(
    r"(?:not logged in|login required|authentication required|unauthorized|api key)",
    re.IGNORECASE,
)
SECRET_RE = re.compile(
    r"(?i)(?:bearer\s+|\b)(?:sk-[A-Za-z0-9_-]+|gh[opurs]_[A-Za-z0-9_-]+|eyJ[A-Za-z0-9_-]+)"
)


def redact(text: str) -> str:
    return SECRET_RE.sub("[REDACTED]", text)


def digest_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def digest_file(path: Path) -> str:
    return digest_bytes(path.read_bytes())


def tree_snapshot(root: Path) -> dict[str, Any]:
    files: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        if not path.is_file() or ".git" in path.parts:
            continue
        files[path.relative_to(root).as_posix()] = digest_file(path)
    status = subprocess.run(
        ["git", "-C", str(root), "status", "--porcelain", "--untracked-files=all"],
        capture_output=True,
        text=True,
        check=False,
    )
    return {
        "files": files,
        "file_count": len(files),
        "tree_fingerprint": digest_bytes(
            "".join(f"{name}\0{value}\n" for name, value in files.items()).encode()
        ),
        "git_status": status.stdout,
        "git_status_exit": status.returncode,
    }


def command(
    name: str,
    argv: list[str],
    *,
    cwd: Path | None = None,
    env: dict[str, str] | None = None,
    timeout: int = 180,
) -> tuple[dict[str, Any], str, str]:
    safe_argv = [redact(str(value)) for value in argv]
    process: subprocess.Popen[str] | None = None
    try:
        process = subprocess.Popen(
            argv,
            cwd=cwd,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            start_new_session=os.name != "nt",
        )
        stdout, stderr = process.communicate(timeout=timeout)
        stdout = stdout or ""
        stderr = stderr or ""
        combined = stdout + stderr
        record = {
            "name": name,
            "command": safe_argv,
            "cwd": str(cwd) if cwd else None,
            "exit_code": process.returncode,
            "status": "pass" if process.returncode == 0 else "fail",
            "stdout_sha256": digest_bytes(stdout.encode()),
            "stderr_sha256": digest_bytes(stderr.encode()),
            "output_excerpt": redact(combined[-1800:]),
            "auth_failure": bool(AUTH_FAILURE_RE.search(combined)),
        }
        return record, stdout, stderr
    except subprocess.TimeoutExpired as error:
        if process is not None:
            if os.name == "nt":
                process.kill()
            else:
                os.killpg(process.pid, signal.SIGKILL)
            stdout_after_kill, stderr_after_kill = process.communicate()
        else:
            stdout_after_kill, stderr_after_kill = "", ""
        stdout = stdout_after_kill or (error.stdout or "")
        stderr = stderr_after_kill or (error.stderr or "")
        if not isinstance(stdout, str):
            stdout = stdout.decode(errors="replace")
        if not isinstance(stderr, str):
            stderr = stderr.decode(errors="replace")
        record = {
            "name": name,
            "command": safe_argv,
            "cwd": str(cwd) if cwd else None,
            "exit_code": process.returncode if process is not None else None,
            "status": "timeout",
            "stdout_sha256": digest_bytes(stdout.encode()),
            "stderr_sha256": digest_bytes(stderr.encode()),
            "output_excerpt": redact((stdout + stderr)[-1800:]),
            "auth_failure": bool(AUTH_FAILURE_RE.search(stdout + stderr)),
        }
        return record, stdout, stderr
    except OSError as error:
        record = {
            "name": name,
            "command": safe_argv,
            "cwd": str(cwd) if cwd else None,
            "exit_code": None,
            "status": "unavailable",
            "error": str(error),
            "stdout_sha256": digest_bytes(b""),
            "stderr_sha256": digest_bytes(b""),
            "output_excerpt": "",
            "auth_failure": False,
        }
        return record, "", str(error)


def add_command(report: dict[str, Any], record: dict[str, Any]) -> None:
    report.setdefault("commands", []).append(record)
    print(f"  {record['name']}: {record['status']}")


def add_check(report: dict[str, Any], name: str, status: str, detail: str = "") -> None:
    report.setdefault("checks", []).append(
        {"name": name, "status": status, "detail": redact(detail)}
    )
    print(f"  {name}: {status}" + (f" — {detail}" if detail else ""))


def ignore_git(_path: str, names: list[str]) -> set[str]:
    return {".git"} if ".git" in names else set()


def make_snapshot(source: Path, destination: Path) -> None:
    shutil.copytree(source, destination, ignore=ignore_git)


def make_local_marketplace(snapshot: Path) -> None:
    """Point only the disposable Codex catalog at its local package copy."""

    path = snapshot / ".agents/plugins/marketplace.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["plugins"][0]["source"] = {"source": "local", "path": "./"}
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def make_update_snapshot(first: Path, second: Path) -> None:
    shutil.copytree(first, second, ignore=ignore_git)
    for relative_path in (".codex-plugin/plugin.json", ".claude-plugin/plugin.json"):
        path = second / relative_path
        data = json.loads(path.read_text(encoding="utf-8"))
        data["version"] = "1.0.1"
        path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    changelog = second / "CHANGELOG.md"
    changelog.write_text(
        "## 1.0.1 — temporary harness update snapshot\n\n"
        "This marker exists only in the disposable update fixture.\n\n"
        + changelog.read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    marker = second / "docs/migration/harness-update-marker.md"
    marker.write_text("Temporary update fixture; never committed.\n", encoding="utf-8")


def replace_directory_contents(destination: Path, source: Path) -> None:
    for child in destination.iterdir():
        if child.is_dir() and not child.is_symlink():
            shutil.rmtree(child)
        else:
            child.unlink()
    for child in source.iterdir():
        target = destination / child.name
        if child.is_dir():
            shutil.copytree(child, target, ignore=ignore_git)
        else:
            shutil.copy2(child, target)


def make_consumer(root: Path) -> None:
    root.mkdir(parents=True, exist_ok=True)
    command("consumer-git-init", ["git", "init", "-q", str(root)])
    command("consumer-git-name", ["git", "-C", str(root), "config", "user.name", "Harness"])
    command(
        "consumer-git-email",
        ["git", "-C", str(root), "config", "user.email", "harness@example.invalid"],
    )
    (root / "consumer.md").write_text(
        "Unrelated consumer fixture.\n", encoding="utf-8"
    )
    command("consumer-git-commit", ["git", "-C", str(root), "add", "consumer.md"])
    command(
        "consumer-git-commit-created",
        ["git", "-C", str(root), "commit", "-qm", "baseline"],
    )


def copy_auth(source: Path | None, destination: Path) -> str | None:
    if source is None:
        return None
    if not source.is_file():
        raise RuntimeError(f"Codex auth source does not exist: {source}")
    destination.mkdir(parents=True, exist_ok=True)
    target = destination / "auth.json"
    shutil.copy2(source, target)
    target.chmod(0o600)
    return "copied-in-memory-test-credential"


def find_installed_plugin(state_root: Path, manifest_directory: str) -> Path | None:
    candidates: list[tuple[tuple[int, int, int], float, Path]] = []
    for manifest in state_root.rglob(f"{manifest_directory}/plugin.json"):
        try:
            data = json.loads(manifest.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if data.get("name") != PLUGIN:
            continue
        version = str(data.get("version", "0.0.0")).split("+", 1)[0]
        try:
            version_key = tuple(int(part) for part in version.split("."))
            if len(version_key) != 3:
                version_key = (0, 0, 0)
        except ValueError:
            version_key = (0, 0, 0)
        candidates.append((version_key, manifest.stat().st_mtime, manifest.parent.parent))
    if not candidates:
        return None
    return max(candidates, key=lambda value: (value[0], value[1]))[2]


def installed_fingerprint(plugin_root: Path) -> str:
    files: list[tuple[str, str]] = []
    for path in sorted(plugin_root.rglob("*")):
        if path.is_file():
            files.append((path.relative_to(plugin_root).as_posix(), digest_file(path)))
    return digest_bytes("".join(f"{name}\0{digest}\n" for name, digest in files).encode())


def installed_contract(plugin_root: Path) -> tuple[bool, str]:
    if plugin_root is None or not plugin_root.is_dir():
        return False, "installed Plugin root was not discovered"
    skills_root = plugin_root / "skills"
    actual = {
        path.name for path in skills_root.iterdir() if path.is_dir()
    } if skills_root.is_dir() else set()
    expected = set(SKILLS)
    if actual != expected:
        return False, f"Skill inventory differs: expected={sorted(expected)}, actual={sorted(actual)}"
    canon = plugin_root / "Next-Move-Theory-Canon"
    if not canon.is_dir():
        return False, "installed bundled Canon root is missing"
    nested = [path for path in canon.rglob("*") if path.is_dir() and path.name == canon.name]
    if nested:
        return False, f"nested Canon root found at {nested[0]}"
    probe = plugin_root / CANON_PROBE
    if not probe.is_file():
        return False, f"Canon probe is missing: {CANON_PROBE}"
    return True, str(probe)


def prompt_command(client: str, binary: str, prompt: str, consumer: Path, env: dict[str, str]) -> list[str]:
    if client == "codex":
        return [
            binary,
            "--ask-for-approval",
            "never",
            "exec",
            "--json",
            "--ephemeral",
            "--ignore-rules",
            "--sandbox",
            "read-only",
            "--cd",
            str(consumer),
            prompt,
        ]
    return [
        binary,
        "--print",
        "--no-session-persistence",
        "--setting-sources",
        "user",
        "--plugin-dir",
        str(env["NMT_INSTALLED_PLUGIN_ROOT"]),
        prompt,
    ]


def run_prompt(
    report: dict[str, Any],
    *,
    client: str,
    binary: str,
    name: str,
    prompt: str,
    consumer: Path,
    env: dict[str, str],
    timeout: int,
    required_markers: tuple[str, ...],
    forbidden_markers: tuple[str, ...] = (),
) -> tuple[bool, bool]:
    record, stdout, stderr = command(
        name,
        prompt_command(client, binary, prompt, consumer, env),
        cwd=consumer,
        env=env,
        timeout=timeout,
    )
    add_command(report, record)
    combined = stdout + stderr
    if record["auth_failure"]:
        add_check(report, name, "evidence_boundary", "client runtime requires credentials; no login attempted")
        return False, True
    if record["status"] in {"timeout", "unavailable"}:
        add_check(report, name, "evidence_boundary", "client runtime did not return within the harness timeout")
        return False, True
    combined_lower = combined.lower()
    markers_ok = all(marker.lower() in combined_lower for marker in required_markers)
    forbidden_ok = all(marker.lower() not in combined_lower for marker in forbidden_markers)
    passed = record["status"] == "pass" and markers_ok and forbidden_ok
    detail = "markers observed" if passed else "required client-visible smoke evidence was not observed"
    add_check(report, name, "pass" if passed else "fail", detail)
    return passed, False


def run_static_gate(report: dict[str, Any]) -> bool:
    record, stdout, stderr = command(
        "static-validation",
        [sys.executable, str(ROOT / "scripts/check_static_validation.py")],
        cwd=ROOT,
        timeout=180,
    )
    add_command(report, record)
    passed = record["status"] == "pass"
    add_check(report, "static-validation", "pass" if passed else "fail", redact((stdout + stderr)[-800:]))
    return passed


def run_codex_update(
    report: dict[str, Any],
    *,
    binary: str,
    env: dict[str, str],
    source_root: Path,
    update_source: Path,
    state_root: Path,
    before_fingerprint: str,
    timeout: int,
    client: dict[str, Any],
) -> bool:
    replace_directory_contents(source_root, update_source)
    # A local fixture is intentionally used for an offline, reproducible run;
    # the current CLI has no marketplace-upgrade operation for local sources.
    add_check(report, "codex-marketplace-refresh", "not_applicable", "local fixture source")
    record, stdout, stderr = command(
        "codex-plugin-reinstall-update",
        [binary, "plugin", "add", f"{PLUGIN}@{MARKETPLACE}", "--json"],
        env=env,
        timeout=timeout,
    )
    add_command(report, record)
    if record["status"] != "pass":
        client["status"] = "fail"
        add_check(report, "codex-plugin-reinstall-update", "fail", redact((stdout + stderr)[-800:]))
        return False
    add_check(report, "codex-plugin-reinstall-update", "pass")
    updated = find_installed_plugin(state_root, ".codex-plugin")
    updated_valid, updated_detail = installed_contract(updated) if updated else (False, "updated Plugin was not discovered")
    after_fingerprint = installed_fingerprint(updated) if updated else ""
    client["installed_plugin_root_after_update"] = str(updated) if updated else None
    client["installed_fingerprint_after"] = after_fingerprint
    changed = after_fingerprint != before_fingerprint
    update_passed = updated_valid and changed
    add_check(report, "codex-update-refresh", "pass" if update_passed else "fail", updated_detail)
    return update_passed


def run_codex(
    report: dict[str, Any],
    *,
    binary: str,
    state_root: Path,
    source_root: Path,
    update_source: Path,
    consumer: Path,
    auth_source: Path | None,
    timeout: int,
    skills: tuple[str, ...] = SKILLS,
) -> bool:
    print("== Codex clean environment ==")
    client: dict[str, Any] = {"status": "running", "state_root": str(state_root)}
    report.setdefault("clients", {})["codex"] = client
    env = os.environ.copy()
    env["HOME"] = str(state_root.parent / "home")
    env["CODEX_HOME"] = str(state_root)
    Path(env["HOME"]).mkdir(parents=True, exist_ok=True)
    state_root.mkdir(parents=True, exist_ok=True)
    try:
        copy_auth(auth_source, state_root)
    except RuntimeError as error:
        client["status"] = "evidence_boundary"
        client["boundary"] = str(error)
        add_check(report, "codex-auth-source", "evidence_boundary", str(error))
        return False

    record, stdout, stderr = command("codex-version", [binary, "--version"], env=env)
    add_command(report, record)
    client["version"] = redact((stdout + stderr).strip())
    if record["status"] != "pass":
        client["status"] = "evidence_boundary"
        add_check(report, "codex-version", "evidence_boundary", "Codex CLI is unavailable")
        return False

    record, stdout, stderr = command("codex-login-status", [binary, "login", "status"], env=env)
    add_command(report, record)
    runtime_boundary = False
    if record["status"] != "pass" or not re.search(r"logged in", stdout + stderr, re.IGNORECASE):
        client["status"] = "evidence_boundary"
        client["boundary"] = "Codex model runtime is not authenticated; no login was attempted"
        add_check(report, "codex-model-runtime", "evidence_boundary", client["boundary"])
        runtime_boundary = True
    else:
        add_check(report, "codex-model-runtime", "pass", "isolated login status is authenticated")

    for name, argv in (
        (
            "codex-marketplace-add",
            [binary, "plugin", "marketplace", "add", str(source_root), "--json"],
        ),
        (
            "codex-plugin-add",
            [binary, "plugin", "add", f"{PLUGIN}@{MARKETPLACE}", "--json"],
        ),
    ):
        record, stdout, stderr = command(name, argv, env=env, timeout=timeout)
        add_command(report, record)
        if record["status"] != "pass":
            client["status"] = "evidence_boundary" if record["auth_failure"] else "fail"
            add_check(report, name, client["status"], redact((stdout + stderr)[-800:]))
            return False
        add_check(report, name, "pass")

    record, stdout, stderr = command(
        "codex-plugin-list-installed",
        [binary, "plugin", "list", "--json"],
        env=env,
        timeout=timeout,
    )
    add_command(report, record)
    add_check(report, "codex-discovery", "pass" if record["status"] == "pass" else "fail")
    installed = find_installed_plugin(state_root, ".codex-plugin")
    valid, detail = installed_contract(installed) if installed else (False, "installed Plugin was not discovered")
    if not valid:
        client["status"] = "fail"
        add_check(report, "codex-installed-contract", "fail", detail)
        return False
    client["installed_plugin_root"] = str(installed)
    client["installed_fingerprint_before"] = installed_fingerprint(installed)
    add_check(report, "codex-installed-contract", "pass", detail)
    add_check(report, "codex-canon-installed-read", "pass", detail)

    for skill in skills:
        if runtime_boundary:
            add_check(
                report,
                f"codex-direct-{skill}",
                "evidence_boundary",
                "skipped after the first unavailable model smoke",
            )
            continue
        passed, boundary = run_prompt(
            report,
            client="codex",
            binary=binary,
            name=f"codex-direct-{skill}",
            prompt=(
                f"Invoke exactly the ${skill} Skill for a read-only installation smoke probe. "
                f"Do not ask questions, call external tools, run installers, or write files. "
                f"Reply exactly `SMOKE_READY {skill}` and one short sentence."
            ),
            consumer=consumer,
            env=env,
            timeout=timeout,
            required_markers=(f"SMOKE_READY {skill}",),
            forbidden_markers=(
                "requested skill is unavailable",
                "skill is unavailable in this session",
            ),
        )
        runtime_boundary = runtime_boundary or boundary
        if not passed and not boundary:
            client["status"] = "fail"
    if runtime_boundary:
        client["status"] = "evidence_boundary"
        client["boundary"] = "Codex model smoke did not return; no retry loop was started"

    if not runtime_boundary:
        passed, boundary = run_prompt(
            report,
            client="codex",
            binary=binary,
            name="codex-canon-read",
            prompt=(
                "Use the installed Next Move Theory Plugin, not the checkout or Consumer project. "
                f"Read `{CANON_PROBE}` from the bundled Canon and reply exactly `CANON_READY` "
                "followed by the first Markdown heading in that file. Do not write files."
            ),
            consumer=consumer,
            env=env,
            timeout=timeout,
            required_markers=("CANON_READY",),
        )
        runtime_boundary = runtime_boundary or boundary
        if not passed and not boundary:
            client["status"] = "fail"

    if not runtime_boundary:
        passed, boundary = run_prompt(
            report,
            client="codex",
            binary=binary,
            name="codex-model-router",
            prompt=(
                "This is a read-only router smoke probe. A product team is deciding whether to "
                "build a new product move and wants help thinking through the next step. Do not "
                "name or invoke a Skill explicitly. Let the installed model-invoked router choose "
                "the existing nmt-chat front door and any documented handoff; do not write files, "
                "and include `ROUTER_READY`, `nmt-chat`, and the selected route in your reply."
            ),
            consumer=consumer,
            env=env,
            timeout=timeout,
            required_markers=("ROUTER_READY", "nmt-chat"),
        )
        runtime_boundary = runtime_boundary or boundary
        if not passed and not boundary:
            client["status"] = "fail"

    if not runtime_boundary:
        passed, boundary = run_prompt(
            report,
            client="codex",
            binary=binary,
            name="codex-negative-route",
            prompt=(
                "This is an unrelated read-only smoke probe. What is 2 + 2? Reply exactly "
                "`NEGATIVE_READY 4`; do not mention Next Move Theory, invoke any NMT Skill, "
                "or write files."
            ),
            consumer=consumer,
            env=env,
            timeout=timeout,
            required_markers=("NEGATIVE_READY 4",),
            forbidden_markers=("nmt-", "Next Move Theory"),
        )
        runtime_boundary = runtime_boundary or boundary
        if not passed and not boundary:
            client["status"] = "fail"

    update_passed = run_codex_update(
        report,
        binary=binary,
        env=env,
        source_root=source_root,
        update_source=update_source,
        state_root=state_root,
        before_fingerprint=client["installed_fingerprint_before"],
        timeout=timeout,
        client=client,
    )
    if not update_passed:
        client["status"] = "fail"
        return False

    if runtime_boundary:
        client["status"] = "evidence_boundary"
        return False
    client["status"] = "pass" if client.get("status") != "fail" else "fail"
    return client["status"] == "pass"


def run_claude_boundary(report: dict[str, Any], binary: str) -> None:
    print("== Claude Code clean environment ==")
    client = {"status": "evidence_boundary", "reason": "runtime smoke is opt-in; no authentication attempted"}
    report.setdefault("clients", {})["claude"] = client
    record, stdout, stderr = command("claude-version", [binary, "--version"])
    add_command(report, record)
    client["version"] = redact((stdout + stderr).strip())
    if record["status"] != "pass":
        client["reason"] = "Claude Code CLI is unavailable"
    add_check(report, "claude-runtime", "evidence_boundary", client["reason"])


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--client", choices=("codex", "claude", "all"), default="all")
    parser.add_argument("--codex", default="codex", help="Codex executable")
    parser.add_argument("--claude", default="claude", help="Claude Code executable")
    parser.add_argument(
        "--only-skill",
        choices=SKILLS,
        action="append",
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "--codex-auth-source",
        type=Path,
        help="Optional existing Codex auth.json copied into temporary state; never printed or persisted",
    )
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument("--report", type=Path, help="JSON report path (defaults to the system temporary directory)")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report: dict[str, Any] = {
        "schema": "next-move-theory.acceptance-harness.v1",
        "started_at_epoch": time.time(),
        "repository": str(ROOT),
        "clients_requested": args.client,
        "credentials": "never printed; optional Codex auth is copied only into temporary state",
        "temporary_state_cleaned": True,
    }
    if not run_static_gate(report):
        report["status"] = "fail"
        return write_report(report, args.report)

    with tempfile.TemporaryDirectory(prefix="nmt-acceptance-") as temporary:
        temp_root = Path(temporary)
        source_root = temp_root / "marketplace-source"
        update_source = temp_root / "marketplace-update-source"
        make_snapshot(ROOT, source_root)
        make_local_marketplace(source_root)
        make_update_snapshot(source_root, update_source)
        consumer = temp_root / "consumer"
        make_consumer(consumer)
        baseline = tree_snapshot(consumer)
        report["consumer"] = {"root": str(consumer), "before": baseline}
        state_root = temp_root / "codex-home"

        if args.client in ("codex", "all"):
            run_codex(
                report,
                binary=args.codex,
                state_root=state_root,
                source_root=source_root,
                update_source=update_source,
                consumer=consumer,
                auth_source=args.codex_auth_source,
                timeout=args.timeout,
                skills=tuple(args.only_skill or SKILLS),
            )
        if args.client in ("claude", "all"):
            run_claude_boundary(report, args.claude)
        after = tree_snapshot(consumer)
        report["consumer"]["after"] = after
        clean = baseline == after
        add_check(report, "consumer-cleanliness", "pass" if clean else "fail")
        report["consumer"]["unchanged"] = clean
        report["temporary_state_cleaned"] = True
        requested_clients = (
            ("codex",) if args.client == "codex" else
            ("claude",) if args.client == "claude" else
            ("codex", "claude")
        )
        statuses = [report.get("clients", {}).get(name, {}).get("status") for name in requested_clients]
        if not clean or any(status == "fail" for status in statuses):
            report["status"] = "fail"
        elif any(status == "evidence_boundary" for status in statuses):
            report["status"] = "evidence_boundary"
        else:
            report["status"] = "pass"
    return write_report(report, args.report)


def write_report(report: dict[str, Any], requested: Path | None) -> int:
    report["finished_at_epoch"] = time.time()
    path = requested or Path(tempfile.gettempdir()) / f"nmt-acceptance-{int(report['started_at_epoch'])}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Report: {path}")
    print(f"Harness: {report['status']}")
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
