#!/usr/bin/env python3
"""Draw the 1200x630 social card used as og:image.

The site itself serves no raster images — diagrams are Mermaid and tables are
Markdown — but link previews and site scanners need one bitmap, so this script
draws it from the site's own palette and writes it to
docs/assets/social-card.png. The output is deterministic: re-running it on an
unchanged configuration produces an identical file, so CI sees no drift.

Run it after changing site_name, the tagline, or the palette:

    python3 scripts/make_social_card.py [--check]

--check redraws into memory and fails if the committed PNG differs.

Fonts are looked up by path, so this runs where the fonts exist (macOS, or a
Linux box with Liberation/DejaVu installed) rather than in CI.
"""

from __future__ import annotations

import io
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs/assets/social-card.png"

W, H = 1200, 630
CHERRY = (186, 12, 47)          # UNM Cherry
CHERRY_DARK = (110, 7, 28)
TURQUOISE = (0, 122, 134)       # UNM Turquoise
WHITE = (255, 255, 255)
MIST = (236, 233, 234)

TITLE = "AI Automation and Agents"
TAGLINE = "From prompts to pipelines: agents, RAG, multi-agent systems,\nand responsible agentic AI"
FOOTER = "Center for Advanced Research Computing  ·  University of New Mexico"
BADGE = "Five modules  ·  40 hours  ·  CC BY 4.0"

BOLD_FONTS = ["/System/Library/Fonts/Supplemental/Arial Bold.ttf",
              "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]
REGULAR_FONTS = ["/System/Library/Fonts/Supplemental/Arial.ttf",
                 "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
                 "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]


def font(candidates: list[str], size: int):
    for path in candidates:
        if Path(path).is_file():
            return ImageFont.truetype(path, size)
    raise SystemExit("error: no usable font found; install Liberation or DejaVu fonts")


def draw_card() -> bytes:
    img = Image.new("RGB", (W, H), CHERRY_DARK)
    d = ImageDraw.Draw(img)

    # A cherry field with a turquoise keyline, the header gradient the site uses.
    d.rectangle([0, 0, W, H - 96], fill=CHERRY)
    d.rectangle([0, H - 96, W, H], fill=CHERRY_DARK)
    d.rectangle([0, H - 100, W, H - 96], fill=TURQUOISE)
    d.rectangle([72, 104, 232, 112], fill=TURQUOISE)

    d.text((72, 160), TITLE, font=font(BOLD_FONTS, 82), fill=WHITE)
    d.multiline_text((72, 290), TAGLINE, font=font(REGULAR_FONTS, 36), fill=MIST, spacing=14)
    d.text((72, 440), BADGE, font=font(BOLD_FONTS, 28), fill=WHITE)
    d.text((72, H - 62), FOOTER, font=font(REGULAR_FONTS, 26), fill=MIST)

    buf = io.BytesIO()
    img.save(buf, format="PNG", optimize=True)
    return buf.getvalue()


def main() -> int:
    data = draw_card()
    if "--check" in sys.argv:
        if not OUT.is_file() or OUT.read_bytes() != data:
            print(f"error: {OUT.relative_to(ROOT)} is out of date — run "
                  "python3 scripts/make_social_card.py", file=sys.stderr)
            return 1
        print(f"{OUT.relative_to(ROOT)} is up to date ({len(data) // 1024} KB)")
        return 0
    OUT.write_bytes(data)
    print(f"wrote {OUT.relative_to(ROOT)} ({W}x{H}, {len(data) // 1024} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
