#!/usr/bin/env python3
"""Validate RepoCraft skill packaging and scenario integrity (stdlib only)."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
EXPECTED = {"project-map", "project-refactor", "project-master"}
errors: list[str] = []


def fail(msg: str) -> None:
    errors.append(msg)


def check_markdown_links(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    # Markdown local inline links only; false positives should be reviewed rather than silently ignored.
    for dest in re.findall(r"(?<!!)\[[^\]\n]+\]\(([^)]+)\)", text):
        dest = dest.strip().split("#", 1)[0]
        if not dest or re.match(r"^[a-z][a-z0-9+.-]*:", dest, re.I) or dest.startswith("#"):
            continue
        if dest.startswith("/"):
            fail(f"Absolute link in {path.relative_to(ROOT)}: {dest}")
            continue
        target = (path.parent / unquote(dest)).resolve()
        if not target.is_relative_to(ROOT.resolve()) or not target.exists():
            fail(f"Broken/escaping relative link in {path.relative_to(ROOT)}: {dest}")


def skill_frontmatter(path: Path) -> dict[str, str]:
    source = path.read_text(encoding="utf-8")
    lines = source.splitlines()
    if not lines or lines[0] != "---":
        fail(f"Missing YAML frontmatter: {path}")
        return {}
    try:
        end = lines.index("---", 1)
    except ValueError:
        fail(f"Missing frontmatter terminator: {path}")
        return {}
    data: dict[str, str] = {}
    for row in lines[1:end]:
        if not row.strip():
            continue
        match = re.fullmatch(r"([a-z][a-z0-9-]*):\s*(.*?)\s*", row)
        if not match:
            fail(f"Invalid simple-frontmatter row {path}: {row}")
            continue
        key, value = match.groups()
        if key in data:
            fail(f"Duplicate key in {path}: {key}")
        data[key] = value.strip("'\"")
    if end + 1 >= len(lines) or not any(x.strip() for x in lines[end + 1:]):
        fail(f"Empty instruction body in {path}")
    if len(lines) > 500:
        fail(f"Excessive SKILL.md length ({len(lines)} > 500): {path}")
    return data


def main() -> int:
    actual = {p.name for p in SKILLS.iterdir() if p.is_dir()}
    if actual != EXPECTED:
        fail(f"Expected exactly {sorted(EXPECTED)}, found {sorted(actual)}")
    for folder in sorted(SKILLS.iterdir()):
        if not folder.is_dir():
            fail(f"Unexpected non-folder in skills/: {folder}")
            continue
        file = folder / "SKILL.md"
        if not file.is_file():
            fail(f"Missing {file}")
            continue
        metadata = skill_frontmatter(file)
        name = metadata.get("name", "")
        desc = metadata.get("description", "")
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or len(name) > 64:
            fail(f"Illegal skill name: {name!r}")
        if name != folder.name:
            fail(f"Skill name/directory mismatch: {name!r} != {folder.name!r}")
        if not desc or len(desc) > 1024:
            fail(f"Invalid description length in {file}")
        if "Use" not in desc and "use" not in desc:
            fail(f"Description should include a 'use' trigger in {file}")
        nested = [p for p in folder.rglob("SKILL.md") if p != file]
        if nested:
            fail(f"Unexpected nested SKILL.md in {folder}: {nested}")

    for md in ROOT.rglob("*.md"):
        check_markdown_links(md)
        if not md.read_bytes().endswith(b"\n"):
            fail(f"Missing final newline: {md.relative_to(ROOT)}")

    manifest = ROOT / "evals" / "scenarios.json"
    try:
        data = json.loads(manifest.read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        fail(f"Unable to parse evaluation manifest: {e}")
        data = {}
    scenarios = data.get("scenarios", [])
    if not isinstance(scenarios, list):
        fail("evals/scenarios.json must have a list 'scenarios'")
        scenarios = []
    seen: set[str] = set()
    counts = {name: 0 for name in EXPECTED}
    for item in scenarios:
        if not isinstance(item, dict):
            fail("Evaluation scenario must be a JSON object")
            continue
        for key in ("id", "skill", "fixture", "prompt", "expected", "forbidden"):
            if not item.get(key):
                fail(f"Evaluation {item.get('id', '<unnamed>')} lacks {key}")
        sid = item.get("id", "")
        if sid in seen:
            fail(f"Duplicate scenario ID: {sid}")
        seen.add(sid)
        if item.get("skill") not in EXPECTED:
            fail(f"Unknown skill in scenario {sid}")
        else:
            counts[item["skill"]] += 1
        for key in ("expected", "forbidden"):
            if not isinstance(item.get(key), list) or not all(isinstance(v, str) and v for v in item.get(key, [])):
                fail(f"Evaluation {sid} {key} must be a nonempty list of strings")
    for name, n in sorted(counts.items()):
        if n < 3:
            fail(f"Need at least 3 distinct evaluation scenarios for {name}; got {n}")

    if errors:
        print(f"FAILED ({len(errors)} errors):")
        for e in errors:
            print(f"  - {e}")
        return 1
    print(f"PASS: {len(EXPECTED)} skills, {len(scenarios)} behavioral scenario definitions, local links, frontmatter and package layout")
    print("NOTE: This is structural validation; real agent behavior and code correctness were not evaluated here.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
