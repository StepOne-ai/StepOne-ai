#!/usr/bin/env python3
"""Fetch a GitHub user's public contribution calendar and render it as an
animated SVG (boxes slide in diagonally, week by week)."""
import re
import sys
from datetime import date

import requests

LEVEL_COLORS = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]
BOX = 11
GAP = 3
CELL = BOX + GAP
PAD = 4


def fetch_levels(user: str) -> dict[date, int]:
    html = requests.get(
        f"https://github.com/users/{user}/contributions", timeout=15
    ).text
    cells = re.findall(r'data-date="([\d-]+)"[^>]*data-level="(\d)"', html)
    return {
        date.fromisoformat(d): int(level)
        for d, level in cells
    }


def build_svg(levels: dict[date, int]) -> str:
    if not levels:
        raise SystemExit("no contribution data found")

    days = sorted(levels)
    start = days[0]
    start -= __import__("datetime").timedelta(days=start.weekday() + 1 if start.weekday() != 6 else 0)

    boxes = []
    max_week = 0
    for d in days:
        week = (d - start).days // 7
        day_of_week = (d.weekday() + 1) % 7  # Sunday-first
        max_week = max(max_week, week)
        level = levels[d]
        x = PAD + week * CELL
        y = PAD + day_of_week * CELL
        delay = (week + day_of_week) * 0.012
        boxes.append(
            f'<rect x="{x - 10}" y="{y - 10}" width="{BOX}" height="{BOX}" rx="2" '
            f'fill="{LEVEL_COLORS[level]}" opacity="0">'
            f'<animate attributeName="opacity" from="0" to="1" begin="{delay:.3f}s" dur="0.3s" fill="freeze" />'
            f'<animate attributeName="x" from="{x - 10}" to="{x}" begin="{delay:.3f}s" dur="0.3s" fill="freeze" />'
            f'<animate attributeName="y" from="{y - 10}" to="{y}" begin="{delay:.3f}s" dur="0.3s" fill="freeze" />'
            f'</rect>'
        )

    width = PAD * 2 + (max_week + 1) * CELL
    height = PAD * 2 + 7 * CELL

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}"
     width="100%" style="background:#0d1117">
  <rect width="100%" height="100%" fill="#0d1117" />
  {"".join(boxes)}
</svg>'''


if __name__ == "__main__":
    user, out = sys.argv[1], sys.argv[2]
    svg = build_svg(fetch_levels(user))
    with open(out, "w") as f:
        f.write(svg)
    print(f"wrote {out}")
