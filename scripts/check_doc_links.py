#!/usr/bin/env python3
"""Validate the Lacerta documentation sources before a Sphinx build.

Checks, for ``docs/en`` and ``docs/es``:

* every relative Markdown link, image, figure/image directive path, ``<a href>`` and ``<img src>``
  points at a file that exists (downloads are looked up in ``docs/assets/downloads``, which Sphinx
  copies to the site root);
* Markdown links with a ``#fragment`` point at an existing heading;
* both languages contain the same set of pages, so the language switcher never lands on a 404;
* the repository README does not link to files that were moved or removed.

Placeholder author links are reported as warnings and do not fail the check.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
DOWNLOADS = DOCS / "assets" / "downloads"
LANGUAGES = ("en", "es")

MD_LINK = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
DIRECTIVE_PATH = re.compile(r"^:{3,}\{(?:figure|image)\}\s+(\S+)", re.MULTILINE)
HTML_ATTR = re.compile(r"""<(?:a|img)\b[^>]*?\b(?:href|src)="([^"]+)\"""")
HEADING = re.compile(r"^#{1,6}\s+(.+?)\s*$", re.MULTILINE)
PLACEHOLDER = re.compile(r"https?://example\.(?:com|org)/")
EXTERNAL = ("http://", "https://", "mailto:", "data:", "#")


def slug(heading: str) -> str:
    heading = re.sub(r"[`*_~]", "", heading).strip().lower()
    heading = re.sub(r"[^\w\s-]", "", heading, flags=re.UNICODE)
    return re.sub(r"[-\s]+", "-", heading).strip("-")


def anchors(path: Path) -> set[str]:
    return {slug(h) for h in HEADING.findall(path.read_text(encoding="utf-8"))}


def resolve(source: Path, target: str) -> Path | None:
    """Return the file a relative target refers to, or None if it does not exist."""
    path_part = target.split("#", 1)[0]
    if not path_part:
        return source
    candidate = (source.parent / path_part).resolve()
    if candidate.exists():
        return candidate
    # Bare file names are download links: Sphinx copies docs/assets/downloads to the site root.
    if "/" not in path_part and (DOWNLOADS / path_part).exists():
        return DOWNLOADS / path_part
    return None


def targets(text: str) -> list[str]:
    found = MD_LINK.findall(text) + DIRECTIVE_PATH.findall(text) + HTML_ATTR.findall(text)
    return [t.strip("<>") for t in found if t and not t.startswith(EXTERNAL)]


def check_file(path: Path, errors: list[str]) -> int:
    text = path.read_text(encoding="utf-8", errors="replace")
    count = 0
    for target in targets(text):
        count += 1
        resolved = resolve(path, target)
        if resolved is None:
            errors.append(f"BROKEN  {path.relative_to(ROOT)} -> {target}")
            continue
        _, _, fragment = target.partition("#")
        if fragment and resolved.suffix == ".md" and fragment not in anchors(resolved):
            errors.append(f"ANCHOR  {path.relative_to(ROOT)} -> {target}")
    return count


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    pages: dict[str, set[str]] = {}
    total = 0

    for language in LANGUAGES:
        tree = DOCS / language
        files = sorted(tree.rglob("*.md"))
        pages[language] = {str(f.relative_to(tree)) for f in files}
        for path in files:
            total += check_file(path, errors)
            if PLACEHOLDER.search(path.read_text(encoding="utf-8")):
                warnings.append(f"PLACEHOLDER {path.relative_to(ROOT)} still has placeholder links")

    only_en = sorted(pages["en"] - pages["es"])
    only_es = sorted(pages["es"] - pages["en"])
    for name in only_en:
        errors.append(f"PARITY  docs/es is missing {name}")
    for name in only_es:
        errors.append(f"PARITY  docs/en is missing {name}")

    readme = ROOT / "README.md"
    if readme.exists():
        total += check_file(readme, errors)

    for warning in warnings:
        print(f"WARN    {warning}")
    if errors:
        for error in errors:
            print(error)
        print(f"\nFAIL: {len(errors)} documentation issue(s) found.")
        return 1
    print(f"PASS: {total} links checked across {sum(map(len, pages.values()))} pages and README.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
