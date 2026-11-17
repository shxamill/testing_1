#!/usr/bin/env python3
"""Check that local HTML and CSS asset references resolve inside this repository."""

from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
IGNORED_DIRS = {".git", "node_modules", "dist", "__pycache__", "temporary screenshots"}
CSS_URL = re.compile(r"url\(\s*(['\"]?)(.*?)\1\s*\)", re.IGNORECASE)


def local_path(value: str) -> str | None:
    value = value.strip()
    if not value or value.startswith("#"):
        return None
    parsed = urlsplit(value)
    if parsed.scheme or parsed.netloc or not parsed.path:
        return None
    return unquote(parsed.path)


def css_references(source: str):
    for match in CSS_URL.finditer(source):
        path = local_path(match.group(2))
        if path:
            yield path


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.references: list[str] = []
        self.in_style = False

    def handle_starttag(self, tag: str, attrs) -> None:
        values = dict(attrs)
        for attribute in ("src", "poster"):
            if values.get(attribute):
                self.references.append(values[attribute])

        href = values.get("href")
        rel = set((values.get("rel") or "").lower().split())
        if href and (tag == "a" or tag == "link" and rel.intersection(
            {"stylesheet", "icon", "manifest", "preload", "modulepreload"}
        )):
            self.references.append(href)

        if values.get("style"):
            self.references.extend(css_references(values["style"]))

        if tag == "style":
            self.in_style = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "style":
            self.in_style = False

    def handle_data(self, data: str) -> None:
        if self.in_style:
            self.references.extend(css_references(data))


def check_reference(source_file: Path, raw_reference: str) -> str | None:
    path = local_path(raw_reference)
    if path is None:
        return None

    target = (source_file.parent / path).resolve()
    try:
        target.relative_to(ROOT)
    except ValueError:
        return f"{source_file.relative_to(ROOT)} references a path outside the repository: {raw_reference}"

    if target.is_dir():
        target = target / "index.html"
    if not target.is_file():
        return f"{source_file.relative_to(ROOT)} references a missing local file: {raw_reference}"
    return None


def main() -> int:
    files = [
        path for path in ROOT.rglob("*")
        if path.is_file()
        and not IGNORED_DIRS.intersection(path.relative_to(ROOT).parts)
        and path.suffix.lower() in {".html", ".htm", ".css"}
    ]
    errors: list[str] = []
    checked = 0

    for source_file in files:
        if source_file.suffix.lower() in {".html", ".htm"}:
            parser = PageParser()
            parser.feed(source_file.read_text(encoding="utf-8"))
            references = parser.references
        else:
            references = list(css_references(source_file.read_text(encoding="utf-8")))

        for reference in references:
            checked += 1
            error = check_reference(source_file, reference)
            if error:
                errors.append(error)

    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors), file=sys.stderr)
        print(f"\n{len(errors)} broken local reference(s) found.", file=sys.stderr)
        return 1

    print(f"Checked {len(files)} HTML/CSS file(s) and {checked} local reference(s): OK.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
