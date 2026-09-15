from __future__ import annotations

import re
from pathlib import Path

MARKDOWN_LINK = re.compile(r"!?\[[^]]*\]\(([^)]+)\)")


def test_relative_markdown_links_exist() -> None:
    root = Path(__file__).resolve().parents[1]
    for document in root.rglob("*.md"):
        if ".venv" in document.parts:
            continue
        text = document.read_text(encoding="utf-8")
        for raw_target in MARKDOWN_LINK.findall(text):
            target = raw_target.split("#", 1)[0]
            if not target or "://" in target or target.startswith("mailto:"):
                continue
            resolved = (document.parent / target).resolve()
            assert resolved.exists(), f"Broken link in {document}: {raw_target}"
