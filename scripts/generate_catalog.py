#!/usr/bin/env python3
"""Generate the deterministic skill catalog from tracked SKILL.md files."""

from __future__ import annotations

import argparse
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CATALOG = "CATALOG.md"


@dataclass(frozen=True)
class Skill:
    path: str
    name: str
    description: str


def tracked_files(root: Path) -> list[str]:
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=root,
        check=True,
        stdout=subprocess.PIPE,
    )
    return sorted(item for item in result.stdout.decode().split("\0") if item)


def parse_frontmatter(path: Path) -> dict[str, str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("frontmatter must start with ---")
    try:
        end = next(index for index, line in enumerate(lines[1:], 1) if line.strip() == "---")
    except StopIteration as error:
        raise ValueError("frontmatter closing --- is missing") from error

    values: dict[str, str] = {}
    frontmatter = lines[1:end]
    index = 0
    while index < len(frontmatter):
        line = frontmatter[index]
        if not line.strip() or line.startswith((" ", "\t")):
            index += 1
            continue
        if ":" not in line:
            raise ValueError(f"invalid frontmatter line: {line!r}")
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if key in {"name", "description"}:
            if value in {"|", ">", "|-", ">-"}:
                block = []
                index += 1
                while index < len(frontmatter) and (
                    not frontmatter[index].strip() or frontmatter[index].startswith((" ", "\t"))
                ):
                    if frontmatter[index].strip():
                        block.append(frontmatter[index].strip())
                    index += 1
                value = " ".join(block)
                if not value:
                    raise ValueError(f"{key} must be non-empty")
                values[key] = value
                continue
            if not value:
                raise ValueError(f"{key} must be a non-empty single-line scalar")
            if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
                value = value[1:-1]
            values[key] = value
        index += 1
    return values


def discover_skills(root: Path) -> list[Skill]:
    skills = []
    for relative_path in tracked_files(root):
        if not relative_path.endswith("SKILL.md"):
            continue
        metadata = parse_frontmatter(root / relative_path)
        skills.append(
            Skill(
                path=relative_path,
                name=metadata.get("name", ""),
                description=metadata.get("description", ""),
            )
        )
    return sorted(skills, key=lambda skill: (skill.name, skill.path))


def category(skill: Skill) -> str:
    value = f"{skill.path}/{skill.name}"
    if "lark" in value or "feishu" in value:
        return "飞书与 Lark"
    if "douyin" in value or "tikhub" in value:
        return "内容与电商"
    if value.startswith("mlops/"):
        return "机器学习"
    if any(part in value for part in ("research", "web-access")):
        return "研究与访问"
    return "通用工具"


def render_catalog(root: Path = ROOT) -> str:
    grouped: dict[str, list[Skill]] = {}
    for skill in discover_skills(root):
        grouped.setdefault(category(skill), []).append(skill)

    lines = [
        "# 技能目录",
        "",
        "> 此文件由 `python3 scripts/generate_catalog.py` 生成，请勿手工编辑。",
        "> 状态仅表示仓库静态检查通过，不代表技能已完成运行时或外部服务集成测试。",
        "",
        f"共 {sum(map(len, grouped.values()))} 个 tracked 技能。",
        "",
    ]
    order = ["飞书与 Lark", "内容与电商", "机器学习", "研究与访问", "通用工具"]
    for heading in order:
        skills = grouped.get(heading)
        if not skills:
            continue
        lines.extend((f"## {heading}", "", "| 技能 | 路径 | 状态 | 描述 |", "|---|---|---|---|"))
        for skill in skills:
            description = skill.description.replace("|", "\\|")
            lines.append(
                f"| `{skill.name}` | [`{skill.path}`]({skill.path}) | 静态检查 | {description} |"
            )
        lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if CATALOG.md is stale")
    args = parser.parse_args(argv)
    rendered = render_catalog(ROOT)
    destination = ROOT / CATALOG
    if args.check:
        if not destination.exists() or destination.read_text(encoding="utf-8") != rendered:
            print("CATALOG.md is stale; run scripts/generate_catalog.py", file=sys.stderr)
            return 1
        print("CATALOG.md is current")
        return 0
    destination.write_text(rendered, encoding="utf-8")
    print(f"wrote {CATALOG} with {len(discover_skills(ROOT))} skills")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
