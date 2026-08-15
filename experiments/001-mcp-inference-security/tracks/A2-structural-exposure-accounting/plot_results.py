#!/usr/bin/env python3
"""Create an SVG comparing calibration error for request and weighted coverage."""
import json
from pathlib import Path

root = Path(__file__).parent
data = json.loads((root / "results" / "benchmark.json").read_text())
streams = data["streams"]
lookup = {(r["stream"], r["predictor"]): r for r in data["summary"]}
w, h, left, top, chart_h = 1000, 520, 90, 65, 350
parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}">',
         '<rect width="100%" height="100%" fill="#0f172a"/>',
         '<text x="45" y="35" fill="#e2e8f0" font-family="sans-serif" font-size="22" font-weight="bold">A2 calibration error: request count vs weighted coverage</text>']
for pct in (0, .1, .2, .3, .4):
    y = top + chart_h - chart_h * pct / .4
    parts += [f'<line x1="{left}" y1="{y}" x2="960" y2="{y}" stroke="#334155"/>',
              f'<text x="45" y="{y+5}" fill="#94a3b8" font-family="sans-serif" font-size="12">{pct:.1f}</text>']
for i, stream in enumerate(streams):
    x = left + 35 + i * 140
    for offset, predictor, color in ((0, "request_fraction", "#eab308"), (45, "weighted_coverage", "#10b981")):
        value = lookup[(stream, predictor)]["calibration_mae"]
        bh = chart_h * value / .4
        parts.append(f'<rect x="{x+offset}" y="{top+chart_h-bh}" width="38" height="{bh}" fill="{color}" rx="3"/>')
    label = stream.replace("-", " ")
    parts.append(f'<text x="{x+38}" y="440" text-anchor="middle" fill="#cbd5e1" font-family="sans-serif" font-size="11">{label}</text>')
parts += ['<rect x="710" y="475" width="16" height="16" fill="#eab308"/><text x="735" y="488" fill="#cbd5e1" font-family="sans-serif" font-size="13">request fraction</text>',
          '<rect x="850" y="475" width="16" height="16" fill="#10b981"/><text x="875" y="488" fill="#cbd5e1" font-family="sans-serif" font-size="13">weighted</text></svg>']
(root / "results" / "figure-a2-calibration.svg").write_text("\n".join(parts) + "\n")
