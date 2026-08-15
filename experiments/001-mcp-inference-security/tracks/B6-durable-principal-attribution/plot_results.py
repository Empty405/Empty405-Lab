#!/usr/bin/env python3
"""Render the B6 security-linkability frontier without third-party packages."""

from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).parent
MECHANISMS = ("session", "account", "global_id", "pairwise", "anonymous_credential", "oracle")
COLORS = {
    "session": "#ef4444",
    "account": "#f59e0b",
    "global_id": "#8b5cf6",
    "pairwise": "#3b82f6",
    "anonymous_credential": "#22c55e",
    "oracle": "#94a3b8",
}
WIDTH, HEIGHT = 940, 620
LEFT, TOP, PLOT_WIDTH, PLOT_HEIGHT = 90, 75, 760, 410


def x(value: float) -> float:
    return LEFT + value / 4 * PLOT_WIDTH


def y(value: float) -> float:
    return TOP + (1 - value) * PLOT_HEIGHT


def main() -> None:
    data = json.loads((HERE / "results" / "benchmark.json").read_text(encoding="utf-8"))["summaries"]
    points = []
    for mechanism in MECHANISMS:
        rows = [row for row in data if row["mechanism"] == mechanism]
        points.append(
            (
                mechanism,
                sum(row["linked_contexts"] for row in rows) / len(rows),
                sum(row["budget_bypass"] for row in rows) / len(rows),
            )
        )

    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">',
        '<rect width="100%" height="100%" fill="#08131f"/>',
        '<style>text{font-family:system-ui,sans-serif;fill:#dbeafe}.grid{stroke:#294052}</style>',
        '<text x="90" y="34" font-size="21" font-weight="700">B6: budget bypass versus cross-context linkability</text>',
        '<text x="90" y="55" font-size="12">108,000 synthetic paired trials · lower-left is preferable</text>',
    ]
    for tick in (0, 1, 2, 3, 4):
        lines.extend(
            [
                f'<line class="grid" x1="{x(tick)}" y1="{TOP}" x2="{x(tick)}" y2="{TOP + PLOT_HEIGHT}"/>',
                f'<text x="{x(tick)}" y="{TOP + PLOT_HEIGHT + 24}" text-anchor="middle" font-size="11">{tick}</text>',
            ]
        )
    for tick in (0, 0.25, 0.50, 0.75, 1.0):
        lines.extend(
            [
                f'<line class="grid" x1="{LEFT}" y1="{y(tick)}" x2="{LEFT + PLOT_WIDTH}" y2="{y(tick)}"/>',
                f'<text x="{LEFT - 12}" y="{y(tick) + 4}" text-anchor="end" font-size="11">{tick:.2f}</text>',
            ]
        )
    for mechanism, linkability, bypass in points:
        color = COLORS[mechanism]
        label_y = y(bypass) - 12 if mechanism != "anonymous_credential" else y(bypass) + 22
        lines.extend(
            [
                f'<circle cx="{x(linkability):.1f}" cy="{y(bypass):.1f}" r="8" fill="{color}"/>',
                f'<text x="{x(linkability):.1f}" y="{label_y:.1f}" text-anchor="middle" font-size="12">{mechanism}</text>',
            ]
        )
    lines.extend(
        [
            f'<text x="{LEFT + PLOT_WIDTH / 2}" y="555" text-anchor="middle" font-size="13">linked contexts (ordinal model)</text>',
            '<text x="22" y="280" transform="rotate(-90 22 280)" text-anchor="middle" font-size="13">budget-bypass rate</text>',
            '<text x="90" y="598" font-size="11">Oracle is evaluator-only and is not a deployable privacy mechanism.</text>',
            "</svg>",
        ]
    )
    (HERE / "results" / "figure-b6-frontier.svg").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
