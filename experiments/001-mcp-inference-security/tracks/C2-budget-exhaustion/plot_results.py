#!/usr/bin/env python3
"""Render the C2 post-cap security-utility frontier without dependencies."""

from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).parent
POLICIES = ("hard_deny", "replay_only", "coarse_fallback", "safe_snapshot", "bounded_override", "oracle")
COLORS = {
    "hard_deny": "#ef4444",
    "replay_only": "#3b82f6",
    "coarse_fallback": "#f59e0b",
    "safe_snapshot": "#06b6d4",
    "bounded_override": "#22c55e",
    "oracle": "#94a3b8",
}
WIDTH, HEIGHT = 960, 620
LEFT, TOP, PLOT_WIDTH, PLOT_HEIGHT = 90, 75, 780, 410


def x(value: float) -> float:
    return LEFT + value / 0.06 * PLOT_WIDTH


def y(value: float) -> float:
    return TOP + (1 - value) * PLOT_HEIGHT


def main() -> None:
    data = json.loads((HERE / "results" / "benchmark.json").read_text(encoding="utf-8"))["summaries"]
    points = []
    for policy in POLICIES:
        rows = [row for row in data if row["policy"] == policy]
        points.append(
            (
                policy,
                sum(row["post_cap_exposure_gain"] for row in rows) / len(rows),
                sum(row["task_completed"] for row in rows) / len(rows),
            )
        )

    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">',
        '<rect width="100%" height="100%" fill="#08131f"/>',
        '<style>text{font-family:system-ui,sans-serif;fill:#dbeafe}.grid{stroke:#294052}</style>',
        '<text x="90" y="34" font-size="21" font-weight="700">C2: task completion versus post-cap exposure</text>',
        '<text x="90" y="55" font-size="12">54,000 synthetic paired trials · upper-left is preferable</text>',
    ]
    for tick in (0, 0.015, 0.030, 0.045, 0.060):
        lines.extend(
            [
                f'<line class="grid" x1="{x(tick)}" y1="{TOP}" x2="{x(tick)}" y2="{TOP + PLOT_HEIGHT}"/>',
                f'<text x="{x(tick)}" y="{TOP + PLOT_HEIGHT + 24}" text-anchor="middle" font-size="11">{tick:.3f}</text>',
            ]
        )
    for tick in (0, 0.25, 0.50, 0.75, 1.0):
        lines.extend(
            [
                f'<line class="grid" x1="{LEFT}" y1="{y(tick)}" x2="{LEFT + PLOT_WIDTH}" y2="{y(tick)}"/>',
                f'<text x="{LEFT - 12}" y="{y(tick) + 4}" text-anchor="end" font-size="11">{tick:.2f}</text>',
            ]
        )
    offsets = {"hard_deny": -14, "safe_snapshot": 24, "replay_only": -14, "oracle": 24}
    for policy, gain, completion in points:
        color = COLORS[policy]
        label_y = y(completion) + offsets.get(policy, -14)
        lines.extend(
            [
                f'<circle cx="{x(gain):.1f}" cy="{y(completion):.1f}" r="8" fill="{color}"/>',
                f'<text x="{x(gain):.1f}" y="{label_y:.1f}" text-anchor="middle" font-size="12">{policy}</text>',
            ]
        )
    lines.extend(
        [
            f'<text x="{LEFT + PLOT_WIDTH / 2}" y="555" text-anchor="middle" font-size="13">mean post-cap exposure gain</text>',
            '<text x="22" y="280" transform="rotate(-90 22 280)" text-anchor="middle" font-size="13">task-completion rate</text>',
            '<text x="90" y="598" font-size="11">Coarse fallback uses an intentionally uncharged namespace; oracle is evaluator-only.</text>',
            "</svg>",
        ]
    )
    (HERE / "results" / "figure-c2-frontier.svg").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
