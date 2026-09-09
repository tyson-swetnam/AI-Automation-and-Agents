#!/usr/bin/env python3
"""Validate the docs/ tree against Open Knowledge Format (OKF) v0.2 conformance.

Checks (spec §11):
  1. Every non-reserved .md file has a parseable YAML frontmatter block.
  2. Every frontmatter block has a non-empty `type` field.
  3. Reserved filenames follow their structure:
     - index.md: no frontmatter, except the bundle root, which may declare
       `okf_version` (site-presentation keys like `hide`/`icon`/`license`
       produce warnings, not failures — consumers MUST tolerate unknown keys).
     - log.md: date headings in ISO 8601 `## YYYY-MM-DD` form.

Also warns on stale pages (now >= stale_after) and non-actor `generated.by`.

Under GitHub Actions (the GITHUB_ACTIONS environment variable is set) every
finding is additionally printed as a workflow command annotation —
`::error file=docs/<rel>::<msg>` / `::warning file=docs/<rel>::<msg>` — so
it shows up inline on the pull request's Files tab. The plain lines are
always printed.

Adapted from UNM-CARC/docs (scripts/okf_validate.py).

Usage: python scripts/okf_validate.py docs
Exit code 1 on conformance errors; warnings never fail the build.
Exit code 2 when the docs directory does not exist.
"""

from __future__ import annotations

import datetime
import os
import re
import sys
from pathlib import Path

import yaml

RESERVED = {"index.md", "log.md"}
# Site-presentation keys the bundle root index.md may carry beside
# okf_version. `license` names the content license shown in the footer.
ROOT_INDEX_ALLOWED_EXTRA = {"hide", "icon", "title", "description", "license"}
ACTOR_RE = re.compile(r"^(human:.+|process:.+|[\w.-]+/[\w.-]+)$")
DATE_HEADING_RE = re.compile(r"^##\s+\d{4}-\d{2}-\d{2}\s*$")

# (relative path, message) pairs; formatted once at the end.
errors: list[tuple[str, str]] = []
warnings: list[tuple[str, str]] = []


def split_frontmatter(text: str):
    if not text.startswith("---"):
        return None, text
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?", text, re.DOTALL)
    if not m:
        return None, text
    try:
        data = yaml.safe_load(m.group(1))
    except yaml.YAMLError as e:
        raise ValueError(f"unparseable YAML frontmatter: {e}")
    return (data if isinstance(data, dict) else {}), text[m.end():]


def check_concept(path: Path, rel: str):
    try:
        fm, _ = split_frontmatter(path.read_text(encoding="utf-8"))
    except ValueError as e:
        errors.append((rel, str(e)))
        return
    if fm is None:
        errors.append((rel, "missing YAML frontmatter block"))
        return
    t = fm.get("type")
    if not t or not str(t).strip():
        errors.append((rel, "frontmatter missing non-empty `type`"))
    gen = fm.get("generated")
    if isinstance(gen, dict):
        by = str(gen.get("by", ""))
        if by and not ACTOR_RE.match(by):
            warnings.append((rel, f"generated.by {by!r} does not follow the actor convention (§7)"))
    stale = fm.get("stale_after")
    if stale:
        try:
            when = datetime.datetime.fromisoformat(str(stale).replace("Z", "+00:00"))
            if when.tzinfo is None:
                when = when.replace(tzinfo=datetime.timezone.utc)
            if datetime.datetime.now(datetime.timezone.utc) >= when:
                warnings.append((rel, f"stale (stale_after {stale})"))
        except ValueError:
            errors.append((rel, f"stale_after {stale!r} is not an ISO 8601 datetime"))
    status = fm.get("status")
    if status and status not in ("draft", "stable", "deprecated"):
        errors.append((rel, f"status {status!r} not in draft|stable|deprecated (§5.4)"))


def check_index(path: Path, rel: str, is_root: bool):
    try:
        fm, _ = split_frontmatter(path.read_text(encoding="utf-8"))
    except ValueError as e:
        errors.append((rel, str(e)))
        return
    if fm is None:
        if is_root:
            warnings.append((rel, "bundle root index.md should declare okf_version (§12)"))
        return
    if not is_root:
        errors.append((rel, "index.md files must not contain frontmatter (§8)"))
        return
    if "okf_version" not in fm:
        warnings.append((rel, "bundle root index.md frontmatter lacks okf_version (§12)"))
    extra = set(fm) - {"okf_version"} - ROOT_INDEX_ALLOWED_EXTRA
    if extra:
        warnings.append((rel, f"root index.md carries extra frontmatter keys {sorted(extra)} "
                              f"(tolerated by consumers, §11)"))


def check_log(path: Path, rel: str):
    text = path.read_text(encoding="utf-8")
    if text.startswith("---"):
        errors.append((rel, "log.md must not contain frontmatter (§9)"))
    headings = [l for l in text.splitlines() if l.startswith("## ")]
    for h in headings:
        if not DATE_HEADING_RE.match(h):
            errors.append((rel, f"log heading {h!r} is not ISO 8601 `## YYYY-MM-DD` (§9)"))


def annotation_escape(msg: str) -> str:
    """Escape a message for a GitHub workflow command (single line only)."""
    return msg.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")


def report(kind: str, rel: str, msg: str, docs: Path, annotate: bool):
    label = "ERROR" if kind == "error" else "WARN "
    print(f"{label} {rel}: {msg}")
    if annotate:
        # Path relative to the working directory, i.e. docs/<rel> when run
        # from the repository root as CI does.
        file = Path(os.path.relpath(docs / rel)).as_posix()
        print(f"::{kind} file={file}::{annotation_escape(msg)}")


def main():
    docs = Path(sys.argv[1] if len(sys.argv) > 1 else "docs")
    if not docs.is_dir():
        print(f"error: {docs} is not a directory", file=sys.stderr)
        sys.exit(2)
    annotate = bool(os.environ.get("GITHUB_ACTIONS"))
    n = 0
    for path in sorted(docs.rglob("*.md")):
        rel = path.relative_to(docs).as_posix()
        n += 1
        if path.name == "index.md":
            check_index(path, rel, is_root=(path.parent == docs))
        elif path.name == "log.md":
            check_log(path, rel)
        else:
            check_concept(path, rel)
    for rel, msg in warnings:
        report("warning", rel, msg, docs, annotate)
    for rel, msg in errors:
        report("error", rel, msg, docs, annotate)
    print(f"\nChecked {n} markdown files: {len(errors)} error(s), {len(warnings)} warning(s).")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
