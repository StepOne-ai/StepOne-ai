#!/usr/bin/env python3
"""Static neofetch-style info card SVG, lines fade in top to bottom."""

LINES = [
    ("stephen@github", "#58f0a0", True),
    ("---------------", "#3b4048", False),
    ("Role      Fullstack / Go Engineer", "#e6edf3", False),
    ("Title     VK Education Team Lead 2025", "#e6edf3", False),
    ("Intern    Yandex Datum", "#e6edf3", False),
    ("School    BMSTU (IU6) — 2026", "#e6edf3", False),
    ("Experience 2+ yrs — analytics services to clinical systems", "#e6edf3", False),
    ("Architecture Microservices + Clean Architecture + SOLID", "#e6edf3", False),
    ("Stack     Go, Gin/Echo, Postgres, Redis, Docker/K8s", "#e6edf3", False),
    ("Frontend  React, Next.js, Node.js", "#e6edf3", False),
    ("Language  English C2 (IELTS)", "#e6edf3", False),
    ("Hobbies   Chess, motocross", "#e6edf3", False),
]

FONT_SIZE = 14
LINE_H = FONT_SIZE * 1.7
PAD = 16
WIDTH = 580


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build_svg() -> str:
    height = PAD * 2 + LINE_H * len(LINES)
    texts = []
    for i, (line, color, bold) in enumerate(LINES):
        y = PAD + (i + 1) * LINE_H - LINE_H * 0.3
        delay = i * 0.12
        weight = "bold" if bold else "normal"
        texts.append(
            f'<text x="{PAD}" y="{y:.1f}" fill="{color}" font-weight="{weight}" '
            f'opacity="0" font-size="{FONT_SIZE}">{esc(line)}'
            f'<animate attributeName="opacity" from="0" to="1" '
            f'begin="{delay:.2f}s" dur="0.35s" fill="freeze" /></text>'
        )

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {height:.0f}"
     width="100%" font-family="'Courier New', monospace" style="background:#0d1117">
  <rect width="100%" height="100%" rx="10" fill="#0d1117" stroke="#30363d" />
  {"".join(texts)}
</svg>'''


if __name__ == "__main__":
    import sys
    out = sys.argv[1]
    with open(out, "w") as f:
        f.write(build_svg())
    print(f"wrote {out}")
