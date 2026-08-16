#!/usr/bin/env python3
"""Render the C4 security-utility frontier without dependencies."""

from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).parent
POLICIES = (
    "global_fifo",
    "rate_limit",
    "reservation",
    "marginal_cap",
    "fair_share",
    "bounded_hybrid",
    "oracle",
)
COLORS = {
    "global_fifo": "#ef4444",
    "rate_limit": "#f97316",
    "reservation": "#3b82f6",
    "marginal_cap": "#06b6d4",
    "fair_share": "#a855f7",
    "bounded_hybrid": "#22c55e",
    "oracle": "#94a3b8",
}
WIDTH, HEIGHT = 980, 640
LEFT, TOP, PLOT_WIDTH, PLOT_HEIGHT = 90, 75, 800, 430


def main() -> None:
    data = json.loads((HERE / "results" / "benchmark.json").read_text(encoding="utf-8"))["summaries"]
    points = []
    for policy in POLICIES:
        rows = [
            row
            for row in data
            if row["policy"] == policy
            and row["strategy"] == "adaptive_burn"
            and row["intensity"] == "high"
        ]
        points.append(
            (
                policy,
                sum(row["attacker_capture_ratio"] for row in rows) / len(rows),
                sum(row["legitimate_completion_rate"] for row in rows) / len(rows),
            )
        )
    x = lambda value: LEFT + value * PLOT_WIDTH
    y = lambda value: TOP + (1 - value) * PLOT_HEIGHT
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">',
        '<rect width="100%" height="100%" fill="#08131f"/>',
        '<style>text{font-family:system-ui,sans-serif;fill:#dbeafe}.grid{stroke:#294052}</style>',
        '<text x="90" y="34" font-size="21" font-weight="700">C4: legitimate utility versus attacker budget capture</text>',
        '<text x="90" y="55" font-size="12">75,600 paired trials · high-intensity adaptive burn · upper-left is preferable</text>',
    ]
    for tick in (0, 0.25, 0.50, 0.75, 1.0):
        lines.extend(
            [
                f'<line class="grid" x1="{x(tick)}" y1="{TOP}" x2="{x(tick)}" y2="{TOP + PLOT_HEIGHT}"/>',
                f'<text x="{x(tick)}" y="{TOP + PLOT_HEIGHT + 24}" text-anchor="middle" font-size="11">{tick:.2f}</text>',
                f'<line class="grid" x1="{LEFT}" y1="{y(tick)}" x2="{LEFT + PLOT_WIDTH}" y2="{y(tick)}"/>',
                f'<text x="{LEFT - 12}" y="{y(tick) + 4}" text-anchor="end" font-size="11">{tick:.2f}</text>',
            ]
        )
    for policy, capture, completion in points:
        lines.extend(
            [
                f'<circle cx="{x(capture):.1f}" cy="{y(completion):.1f}" r="8" fill="{COLORS[policy]}"/>',
                f'<text x="{x(capture):.1f}" y="{y(completion) - 13:.1f}" text-anchor="middle" font-size="11">{policy}</text>',
            ]
        )
    lines.extend(
        [
            f'<text x="{LEFT + PLOT_WIDTH / 2}" y="575" text-anchor="middle" font-size="13">attacker budget-capture ratio</text>',
            '<text x="22" y="290" transform="rotate(-90 22 290)" text-anchor="middle" font-size="13">legitimate task-completion rate</text>',
            '<text x="90" y="615" font-size="11">Oracle is evaluator-only; exact identity and marginal exposure are assumed.</text>',
            "</svg>",
        ]
    )
    (HERE / "results" / "figure-c4-frontier.svg").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
