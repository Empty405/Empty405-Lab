#!/usr/bin/env python3
"""Generate a dependency-free SVG summary from benchmark.json."""

import json
from pathlib import Path

ROOT = Path(__file__).parent
data = json.loads((ROOT / "results" / "benchmark.json").read_text())
rows = [r for r in data["summary"] if r["scenario"] == "unique" and r["observer"] == "patient"]
order = ["baseline", "rate_limit", "lifetime_quota", "coverage_budget", "hybrid"]
by_policy = {r["policy"]: r for r in rows}
colors = {"baseline": "#64748b", "rate_limit": "#eab308", "lifetime_quota": "#8b5cf6", "coverage_budget": "#10b981", "hybrid": "#06b6d4"}
width, height = 900, 500
left, top, chart_h = 90, 70, 330
bar_w, gap = 105, 55
parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
         '<rect width="100%" height="100%" fill="#0f172a"/>',
         '<text x="45" y="35" fill="#e2e8f0" font-family="sans-serif" font-size="22" font-weight="bold">A1: patient observer, unique-query scenario</text>']
for pct in range(0, 101, 25):
    y = top + chart_h - chart_h * pct / 100
    parts.append(f'<line x1="{left}" y1="{y}" x2="850" y2="{y}" stroke="#334155"/>')
    parts.append(f'<text x="45" y="{y+5}" fill="#94a3b8" font-family="sans-serif" font-size="13">{pct}%</text>')
for i, policy in enumerate(order):
    value = by_policy[policy]["observable_state_mean"]
    x = left + 25 + i * (bar_w + gap)
    h = chart_h * value
    y = top + chart_h - h
    parts.append(f'<rect x="{x}" y="{y}" width="{bar_w}" height="{h}" rx="5" fill="{colors[policy]}"/>')
    parts.append(f'<text x="{x+bar_w/2}" y="{y-10}" text-anchor="middle" fill="#f8fafc" font-family="sans-serif" font-size="15">{value*100:.0f}%</text>')
    label = policy.replace("_", " ")
    parts.append(f'<text x="{x+bar_w/2}" y="430" text-anchor="middle" fill="#cbd5e1" font-family="sans-serif" font-size="13">{label}</text>')
parts.append('<text x="450" y="475" text-anchor="middle" fill="#94a3b8" font-family="sans-serif" font-size="13">Final observable state; 1000 trials; seed 40501</text></svg>')
(ROOT / "results" / "figure-a1-observable-state.svg").write_text("\n".join(parts) + "\n")
