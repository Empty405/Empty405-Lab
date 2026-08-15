#!/usr/bin/env python3
"""Render the B1 exposure curve as dependency-free SVG."""

import json
from pathlib import Path

HERE = Path(__file__).parent
DATA = json.loads((HERE / "results" / "benchmark.json").read_text())["summaries"]
STRATEGIES = ("per_identity", "durable_credential", "deterministic", "probabilistic", "oracle")
COLORS = {"per_identity":"#ef4444", "durable_credential":"#22c55e", "deterministic":"#f59e0b", "probabilistic":"#3b82f6", "oracle":"#a78bfa"}
W, H, LEFT, TOP, PW, PH = 900, 560, 80, 55, 760, 400


def x(v): return LEFT + v / 16 * PW
def y(v): return TOP + (1 - v) * PH


def main():
    lines = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
             '<rect width="100%" height="100%" fill="#08131f"/>',
             '<style>text{font-family:system-ui,sans-serif;fill:#dbeafe}.grid{stroke:#294052;stroke-width:1}.axis{stroke:#94a3b8;stroke-width:1.5}</style>',
             '<text x="80" y="30" font-size="20" font-weight="700">B1: exposure after identity rotation</text>',
             '<text x="80" y="50" font-size="12" fill="#94a3b8">budget=0.25, noisy signals, mean of 1,000 trials</text>']
    for tick in (0, .25, .5, .75, 1):
        lines += [f'<line class="grid" x1="{LEFT}" y1="{y(tick)}" x2="{LEFT+PW}" y2="{y(tick)}"/>',
                  f'<text x="{LEFT-12}" y="{y(tick)+4}" text-anchor="end" font-size="11">{tick:.2f}</text>']
    for tick in (0, 1, 2, 4, 8, 16):
        lines += [f'<line class="grid" x1="{x(tick)}" y1="{TOP}" x2="{x(tick)}" y2="{TOP+PH}"/>',
                  f'<text x="{x(tick)}" y="{TOP+PH+22}" text-anchor="middle" font-size="11">{tick}</text>']
    lines += [f'<line class="axis" x1="{LEFT}" y1="{TOP+PH}" x2="{LEFT+PW}" y2="{TOP+PH}"/>',
              f'<line class="axis" x1="{LEFT}" y1="{TOP}" x2="{LEFT}" y2="{TOP+PH}"/>',
              f'<line x1="{LEFT}" y1="{y(.25)}" x2="{LEFT+PW}" y2="{y(.25)}" stroke="#f8fafc" stroke-dasharray="6 5"/>']
    for index, strategy in enumerate(STRATEGIES):
        rows = [r for r in DATA if r["strategy"] == strategy and r["budget"] == .25 and r["signal_quality"] == "noisy"]
        rows.sort(key=lambda r:r["rotation_count"])
        points = " ".join(f'{x(r["rotation_count"]):.1f},{y(r["exposure"]):.1f}' for r in rows)
        color = COLORS[strategy]
        lines.append(f'<polyline points="{points}" fill="none" stroke="{color}" stroke-width="3"/>')
        for r in rows:
            lines.append(f'<circle cx="{x(r["rotation_count"]):.1f}" cy="{y(r["exposure"]):.1f}" r="3.5" fill="{color}"/>')
        ly = 490 + (index % 2) * 25
        lx = 80 + (index // 2) * 270
        lines += [f'<line x1="{lx}" y1="{ly}" x2="{lx+28}" y2="{ly}" stroke="{color}" stroke-width="4"/>',
                  f'<text x="{lx+36}" y="{ly+4}" font-size="12">{strategy}</text>']
    lines += ['<text x="460" y="545" text-anchor="middle" font-size="12">rotation count</text>',
              '<text x="18" y="255" text-anchor="middle" font-size="12" transform="rotate(-90 18 255)">principal exposure</text>', '</svg>']
    (HERE / "results" / "figure-b1-rotation-exposure.svg").write_text("\n".join(lines)+"\n")


if __name__ == "__main__": main()
