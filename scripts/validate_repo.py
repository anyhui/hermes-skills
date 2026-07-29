#!/usr/bin/env python3
"""Run dependency-free static validation for the skills repository."""

from __future__ import annotations

import argparse
import json
import posixpath
import re
import subprocess
import sys
import tokenize
import urllib.parse
from dataclasses import dataclass
from pathlib import Path

try:
    from scripts import generate_catalog
except ModuleNotFoundError:
    import generate_catalog  # type: ignore[no-redef]


ROOT = Path(__file__).resolve().parents[1]
NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK_PATTERN = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
CODE_PATTERN = re.compile(r"```.*?```|`[^`\n]*`", re.DOTALL)
MAX_FILE_SIZE = 256 * 1024
OVERSIZED_ALLOWLIST = {
    "mlops/training/pytorch-fsdp/references/other.md": "upstream reference material",
}
SECRET_SCAN_EXCLUSIONS = {"scripts/validate_repo.py"}


def _secret_patterns() -> tuple[tuple[str, re.Pattern[str]], ...]:
    # Split signatures keep the validator's own source from looking like a credential.
    return (
        ("GitHub token", re.compile("gh" + r"[pousr]_[A-Za-z0-9]{30,}")),
        ("AWS access key", re.compile("AK" + r"IA[0-9A-Z]{16}")),
        ("private key", re.compile("-----BEGIN " + r"(?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
        (
            "assigned credential",
            re.compile(
                r"(?i)(?:api[_-]?key|access[_-]?token|client[_-]?secret|password)\s*[:=]\s*['\"]?[A-Za-z0-9_./+=-]{20,}"
            ),
        ),
    )


@dataclass(frozen=True)
class Issue:
    severity: str
    code: str
    path: str
    message: str


def issue(code: str, path: str, message: str, severity: str = "error") -> Issue:
    return Issue(severity, code, path, message)


def tracked_files(root: Path) -> list[str]:
    return generate_catalog.tracked_files(root)


def gitlinks(root: Path) -> set[str]:
    result = subprocess.run(
        ["git", "ls-files", "--stage", "-z"],
        cwd=root,
        check=True,
        stdout=subprocess.PIPE,
    )
    links = set()
    for entry in filter(None, result.stdout.decode().split("\0")):
        metadata, path = entry.split("\t", 1)
        if metadata.split()[0] == "160000":
            links.add(path)
    return links


def _text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return None


def _link_target(raw_target: str) -> str:
    target = raw_target.strip()
    if target.startswith("<") and ">" in target:
        return target[1 : target.index(">")]
    return target.split(maxsplit=1)[0]


def validate(root: Path = ROOT, check_catalog: bool = True) -> list[Issue]:
    findings: list[Issue] = []
    files = tracked_files(root)
    tracked = set(files)
    link_paths = gitlinks(root)
    names: dict[str, str] = {}

    for relative_path in files:
        path = root / relative_path
        if relative_path in link_paths or not path.is_file():
            continue
        size = path.stat().st_size
        if size > MAX_FILE_SIZE:
            if relative_path in OVERSIZED_ALLOWLIST:
                findings.append(issue("oversized-allowlisted", relative_path, f"oversized tracked file is allowlisted ({size} bytes)", "warning"))
            else:
                findings.append(issue("oversized", relative_path, f"tracked file exceeds {MAX_FILE_SIZE} bytes ({size} bytes)"))

        if relative_path.endswith("SKILL.md"):
            try:
                metadata = generate_catalog.parse_frontmatter(path)
            except (UnicodeDecodeError, ValueError) as error:
                findings.append(issue("frontmatter", relative_path, f"invalid frontmatter: {error}"))
            else:
                name = metadata.get("name", "")
                description = metadata.get("description", "")
                if not NAME_PATTERN.fullmatch(name):
                    findings.append(issue("skill-name", relative_path, "skill name must be lowercase kebab-case"))
                if not description.strip():
                    findings.append(issue("skill-description", relative_path, "skill description is required"))
                if name in names:
                    findings.append(issue("duplicate-name", relative_path, f"duplicate skill name also used by {names[name]}"))
                elif name:
                    names[name] = relative_path

        if relative_path.endswith(".json"):
            try:
                json.loads(path.read_text(encoding="utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError) as error:
                findings.append(issue("json", relative_path, f"invalid JSON: {error}"))

        if relative_path.endswith(".py"):
            try:
                with tokenize.open(path) as source:
                    compile(source.read(), relative_path, "exec")
            except (SyntaxError, UnicodeError) as error:
                findings.append(issue("python", relative_path, f"Python compile failed: {error}"))

        text = _text(path)
        if text is None:
            continue
        if relative_path not in SECRET_SCAN_EXCLUSIONS:
            for label, pattern in _secret_patterns():
                if pattern.search(text):
                    findings.append(issue("secret", relative_path, f"possible secret: {label}"))
                    break

        if relative_path.endswith((".md", ".markdown")):
            markdown = CODE_PATTERN.sub("", text)
            for match in LINK_PATTERN.finditer(markdown):
                target = urllib.parse.unquote(_link_target(match.group(1)))
                if not target or target.startswith(("#", "/")) or re.match(r"^[a-z][a-z0-9+.-]*:", target, re.I):
                    continue
                target = target.split("#", 1)[0].split("?", 1)[0]
                if not target:
                    continue
                resolved = (Path(relative_path).parent / target).as_posix()
                normalized = posixpath.normpath(resolved)
                if normalized not in tracked and not any(
                    normalized == link or normalized.startswith(f"{link}/") for link in link_paths
                ):
                    findings.append(issue("broken-link", relative_path, f"broken local link: {target}"))

    if check_catalog:
        catalog = root / generate_catalog.CATALOG
        try:
            expected = generate_catalog.render_catalog(root)
        except (UnicodeDecodeError, ValueError):
            expected = None
        if expected is not None and (not catalog.exists() or catalog.read_text(encoding="utf-8") != expected):
            findings.append(issue("catalog-stale", generate_catalog.CATALOG, "generated catalog is stale"))
    return sorted(findings, key=lambda item: (item.severity, item.path, item.code, item.message))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--no-catalog", action="store_true", help="skip catalog freshness validation")
    args = parser.parse_args(argv)
    findings = validate(ROOT, check_catalog=not args.no_catalog)
    links = sorted(gitlinks(ROOT))
    errors = [item for item in findings if item.severity == "error"]
    warnings = [item for item in findings if item.severity == "warning"]
    if links:
        print(f"gitlinks not traversed ({len(links)}): {', '.join(links)}")
    for item in findings:
        print(f"{item.severity}: {item.path}: {item.message}")
    print(f"validated repository: {len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
