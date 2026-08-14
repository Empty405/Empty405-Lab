#!/usr/bin/env python

import argparse
import hashlib
import json
import pathlib
import urllib.request
import urllib.error
from datetime import datetime, timezone


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source_id")
    parser.add_argument("url")
    parser.add_argument("--category", default="misc")
    parser.add_argument("--timeout", type=int, default=30)
    args = parser.parse_args()

    root = pathlib.Path("sources/archive") / args.category / args.source_id
    root.mkdir(parents=True, exist_ok=True)

    req = urllib.request.Request(
        args.url,
        headers={
            "User-Agent": "Empty405-Lab-Research/1.0"
        }
    )

    fetched_at = datetime.now(timezone.utc).isoformat()

    try:
        with urllib.request.urlopen(req, timeout=args.timeout) as response:
            body = response.read()
            status = response.status
            content_type = response.headers.get("Content-Type", "")
            final_url = response.geturl()
    except urllib.error.HTTPError as e:
        body = e.read()
        status = e.code
        content_type = e.headers.get("Content-Type", "")
        final_url = e.geturl()
    except Exception as e:
        print(f"ERROR: {e}")
        raise SystemExit(1)

    digest = sha256_bytes(body)

    if "html" in content_type.lower():
        ext = ".html"
    elif "pdf" in content_type.lower():
        ext = ".pdf"
    elif "json" in content_type.lower():
        ext = ".json"
    else:
        ext = ".bin"

    content_path = root / f"source{ext}"
    metadata_path = root / "metadata.json"

    content_path.write_bytes(body)

    metadata = {
        "source_id": args.source_id,
        "requested_url": args.url,
        "final_url": final_url,
        "fetched_at_utc": fetched_at,
        "http_status": status,
        "content_type": content_type,
        "sha256": digest,
        "bytes": len(body),
        "local_path": str(content_path),
    }

    metadata_path.write_text(
        json.dumps(metadata, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print(json.dumps(metadata, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
