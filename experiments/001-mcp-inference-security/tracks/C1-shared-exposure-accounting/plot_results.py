#!/usr/bin/env python3
"""Render the C1 security-coordination frontier without dependencies."""

from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).parent
MECHANISMS = ("independent", "central", "eventual", "hierarchical", "escrow", "oracle")
COLORS = {
    "independent": "#ef4444",
    "central": "#f59e0b",
    "eventual": "#3b82f6",
    "hierarchical": "#06b6d4",
    "escrow": "#22c55e",
    "oracle": "#94a3b8",
}
WIDTH, HEIGHT = 960, 620
LEFT, TOP, PLOT_WIDTH, PLOT_HEIGHT = 90, 75, 780, 410


def x(value: float) -> float:
    return LEFT + value / 128 * PLOT_WIDTH


def y(value: float) -> float:
    return TOP + (0.60 - value) / 0.60 * PLOT_HEIGHT


def main() -> None:
    data = json.loads((HERE / "results" / "benchmark.json").read_text(encoding="utf-8"))["summaries"]
    points = []
    for mechanism in MECHANISMS:
        rows = [row for row in data if row["mechanism"] == mechanism]
        points.append(
            (
                mechanism,
                sum(row["coordination_messages"] for row in rows) / len(rows),
                sum(row["overrun_event"] for row in rows) / len(rows),
            )
        )

    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">',
        '<rect width="100%" height="100%" fill="#08131f"/>',
        '<style>text{font-family:system-ui,sans-serif;fill:#dbeafe}.grid{stroke:#294052}</style>',
        '<text x="90" y="34" font-size="21" font-weight="700">C1: budget overrun versus coordination</text>',
        '<text x="90" y="55" font-size="12">54,000 synthetic paired trials · lower-left is preferable</text>',
    ]
    for tick in (0, 32, 64, 96, 128):
        lines.extend(
            [
                f'<line class="grid" x1="{x(tick)}" y1="{TOP}" x2="{x(tick)}" y2="{TOP + PLOT_HEIGHT}"/>',
                f'<text x="{x(tick)}" y="{TOP + PLOT_HEIGHT + 24}" text-anchor="middle" font-size="11">{tick}</text>',
            ]
        )
    for tick in (0, 0.15, 0.30, 0.45, 0.60):
        lines.extend(
            [
                f'<line class="grid" x1="{LEFT}" y1="{y(tick)}" x2="{LEFT + PLOT_WIDTH}" y2="{y(tick)}"/>',
                f'<text x="{LEFT - 12}" y="{y(tick) + 4}" text-anchor="end" font-size="11">{tick:.2f}</text>',
            ]
        )
    offsets = {"independent": -14, "oracle": 24, "hierarchical": -14, "escrow": 24}
    for mechanism, messages, overrun in points:
        color = COLORS[mechanism]
        label_y = y(overrun) + offsets.get(mechanism, -14)
        lines.extend(
            [
                f'<circle cx="{x(messages):.1f}" cy="{y(overrun):.1f}" r="8" fill="{color}"/>',
                f'<text x="{x(messages):.1f}" y="{label_y:.1f}" text-anchor="middle" font-size="12">{mechanism}</text>',
            ]
        )
    lines.extend(
        [
            f'<text x="{LEFT + PLOT_WIDTH / 2}" y="555" text-anchor="middle" font-size="13">mean coordination messages per trial</text>',
            '<text x="22" y="280" transform="rotate(-90 22 280)" text-anchor="middle" font-size="13">budget-overrun event rate</text>',
            '<text x="90" y="598" font-size="11">Oracle is evaluator-only; zero messages do not make it deployable.</text>',
            "</svg>",
        ]
    )
    (HERE / "results" / "figure-c1-frontier.svg").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
