#!/usr/bin/env python

from html.parser import HTMLParser
from pathlib import Path
import json
import re

KEYWORDS = [
    "Postfach",
    "eAkte",
    "elektronische Akte",
    "Zuständigkeit",
    "Zuständigkeitswechsel",
    "Speicherung",
    "Aufbewahrung",
    "Löschung",
    "löschen",
    "Zugriff",
    "Zugriffsrecht",
    "Datenschutz",
    "Dolmetscher",
    "Sprachunterstützung",
    "Sprache",
    "Nachricht",
    "Dokument",
]

class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in {"script", "style", "noscript"}:
            self.skip += 1

    def handle_endtag(self, tag):
        if tag in {"script", "style", "noscript"} and self.skip:
            self.skip -= 1

    def handle_data(self, data):
        if not self.skip:
            text = " ".join(data.split())
            if text:
                self.parts.append(text)

def html_to_text(raw):
    parser = TextExtractor()
    parser.feed(raw)
    return "\n".join(parser.parts)

archive = Path("sources/archive")
output = Path("data/source-triage-001.md")

lines = [
    "# Source Triage 001",
    "",
    "Generated from archived official/public sources.",
    "",
]

for metadata_path in sorted(archive.rglob("metadata.json")):
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    source_id = metadata["source_id"]
    content_path = Path(metadata["local_path"])

    if not content_path.exists() or content_path.suffix != ".html":
        continue

    raw = content_path.read_text(encoding="utf-8", errors="ignore")
    text = html_to_text(raw)

    lines += [
        f"## {source_id}",
        "",
        f"URL: {metadata['final_url']}",
        f"SHA256: `{metadata['sha256']}`",
        "",
    ]

    found_any = False

    for keyword in KEYWORDS:
        pattern = re.compile(re.escape(keyword), re.IGNORECASE)

        for match in list(pattern.finditer(text))[:5]:
            found_any = True
            start = max(0, match.start() - 350)
            end = min(len(text), match.end() + 500)
            snippet = re.sub(r"\s+", " ", text[start:end]).strip()

            lines += [
                f"### {keyword}",
                "",
                snippet,
                "",
            ]

    if not found_any:
        lines += ["No configured keyword hits.", ""]

output.write_text("\n".join(lines), encoding="utf-8")
print(f"Wrote: {output}")
