#!/usr/bin/env python3
"""Convert a photo into a self-typing ASCII-art SVG for the profile README."""
import sys
import numpy as np
from PIL import Image

RAMP = " .`:-=+*cs#%@"
COLS = 140
FONT_SIZE = 7
CHAR_W = FONT_SIZE * 0.6
LINE_H = FONT_SIZE * 1.15


def to_ascii_rows(src_path: str) -> list[str]:
    img = Image.open(src_path).convert("L")
    w, h = img.size
    # downsample on the full-res image first so hair/skin texture is properly
    # averaged away, then shrink the rest of the way to the char grid
    img = img.resize((w // 4, h // 4), Image.LANCZOS)
    w, h = img.size
    rows = round(COLS * (h / w) * (CHAR_W / LINE_H))
    small = np.array(img.resize((COLS, rows), Image.LANCZOS)).astype(np.float32)

    lo, hi = np.percentile(small, [2, 98])
    small = np.clip((small - lo) / max(hi - lo, 1) * 255, 0, 255)

    idx = (small / 255 * (len(RAMP) - 1)).round().astype(int)
    return ["".join(RAMP[v] for v in row) for row in idx]


def build_svg(rows: list[str]) -> str:
    width = COLS * CHAR_W
    height = len(rows) * LINE_H
    row_delay = 0.05

    defs = []
    texts = []
    for i, row in enumerate(rows):
        escaped = (
            row.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        )
        clip_id = f"clip{i}"
        start = i * row_delay
        defs.append(f'''
    <clipPath id="{clip_id}">
      <rect x="0" y="{i * LINE_H:.2f}" width="0" height="{LINE_H:.2f}">
        <animate attributeName="width" from="0" to="{width:.2f}"
          begin="{start:.2f}s" dur="0.4s" fill="freeze" />
      </rect>
    </clipPath>''')
        texts.append(
            f'<text x="0" y="{(i + 1) * LINE_H:.2f}" clip-path="url(#{clip_id})">{escaped}</text>'
        )

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width:.0f} {height:.0f}"
     width="100%" font-family="'Courier New', monospace" font-size="{FONT_SIZE}"
     style="background:#0d1117">
  <style>text {{ fill: #58f0a0; white-space: pre; }}</style>
  <rect width="100%" height="100%" fill="#0d1117" />
  <defs>{"".join(defs)}
  </defs>
  {"".join(texts)}
</svg>'''


if __name__ == "__main__":
    src, out = sys.argv[1], sys.argv[2]
    rows = to_ascii_rows(src)
    svg = build_svg(rows)
    with open(out, "w") as f:
        f.write(svg)
    print(f"wrote {out}: {COLS}x{len(rows)} chars")
