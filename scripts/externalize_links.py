#!/usr/bin/env python3
"""Sweep docs/ so every external hyperlink opens in a new browser tab.

Idempotent transform, identical to the one the migration pipeline applies:
appends {target=_blank} to external [text](http...) links, injects
target=_blank into existing attr blocks, and patches raw HTML anchors.
Internal/relative links, mailto:, and fenced code blocks are left untouched.
Frontmatter is preserved byte-for-byte.

Standalone: `externalize_links(text)` below is the single source of truth and
may be imported by other scripts (`from externalize_links import
externalize_links`).

Adapted from UNM-CARC/docs (scripts/externalize_links.py and
migrate_quickbytes.externalize_links).

Usage: python3 scripts/externalize_links.py [docs]
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# Top-level directories under docs/ that hold no content pages.
SKIP_TOP = {"assets", "materials", "stylesheets"}


def externalize_links(md: str) -> str:
    """Make external links open in new tabs: append {target=_blank} to
    [text](http...) links, add target=_blank into existing attr blocks, and
    patch raw HTML anchors. Internal/relative and mailto: links are left
    untouched; fenced code blocks are skipped. Idempotent."""
    out, fence = [], None
    for line in md.splitlines():
        stripped = line.lstrip()
        marker = stripped[:3]
        if marker in ("```", "~~~"):
            if fence is None:
                fence = marker
            elif marker == fence:
                fence = None
            out.append(line)
            continue
        if fence:
            out.append(line)
            continue
        # external md links with an existing attr block: ensure target=
        def attr_sub(m):
            attrs = m.group(3)
            if "target=" in attrs:
                return m.group(0)
            return f"{m.group(1)}{attrs.rstrip()} target=_blank }}"
        line = re.sub(r"((?<!\!)\[[^\]]*\]\((https?://[^)\s]+)\)\{)([^}]*)\}",
                      attr_sub, line)
        # external md links without an attr block
        line = re.sub(r"((?<!\!)\[[^\]]*\]\((https?://[^)\s]+)\))(?!\{)",
                      r"\1{target=_blank}", line)
        # raw HTML anchors to external URLs
        line = re.sub(r'(<a\s+)(?![^>]*\btarget=)([^>]*href="https?://[^"]*")',
                      r'\1target="_blank" \2', line)
        out.append(line)
    return "\n".join(out)


def split_frontmatter(text: str):
    if text.startswith("---"):
        m = re.match(r"^(---\s*\n.*?\n---\s*\n)", text, re.DOTALL)
        if m:
            return m.group(1), text[m.end():]
    return "", text


def main():
    docs = Path(sys.argv[1] if len(sys.argv) > 1 else
                Path(__file__).resolve().parent.parent / "docs")
    if not docs.is_dir():
        print(f"error: {docs} is not a directory", file=sys.stderr)
        sys.exit(2)
    changed = 0
    for path in sorted(docs.rglob("*.md")):
        if path.relative_to(docs).parts[0] in SKIP_TOP:
            continue
        text = path.read_text(encoding="utf-8")
        fm, body = split_frontmatter(text)
        new_body = externalize_links(body)
        if body.endswith("\n") and not new_body.endswith("\n"):
            new_body += "\n"  # splitlines/join must not eat the final newline
        if new_body != body:
            path.write_text(fm + new_body, encoding="utf-8")
            changed += 1
            print(f"  updated {path.relative_to(docs)}")
    print(f"{changed} file(s) updated.")


if __name__ == "__main__":
    main()
