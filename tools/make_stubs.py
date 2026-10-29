#!/usr/bin/env python3
"""Create every page the nav names and that does not exist yet, as a stub in its template (from par6's tool).

Never overwrites an existing file. Run from the repository root:  python tools/make_stubs.py [--dry-run]

Templates (by what the nav entry is):
  * the manual's landing page  (index.md)                 -> title, hero, document block
  * "About this manual"        (about.md)                 -> scope, finding your way, warnings and notes, related
                                                            documents, document history
  * a chapter page             (<chapter>/index.md)       -> intro + list of its pages
  * the Glossary page          (terminology.md)           -> the shared glossary snippet
  * any other page                                        -> heading + stub notice
Every stub carries `status: draft` in its front matter, so the sidebar shows which pages are not written yet.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from mkdocs.config import load_config

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

MANUAL_KEY = "spectral"
MANUAL_TITLE = "Spectral Micro Manual"
HERO = "assets/spectral-Photoroom.png"

DRAFT = "---\nstatus: draft\n---\n\n"

PUBLISHER = (
    "Source Robotics d.o.o. publishes this document for the Spectral Micro BLDC driver. It is revised as the product and "
    "its firmware change; the document number, firmware version, revision and date above identify the version you are "
    "reading, and the document history on the next page says what changed. Take care that the firmware version named "
    "under *Applies to* matches what `#Info` reports on your driver: the version selector in the header switches "
    "between firmware releases. The licence that covers this text is stated in the documentation repository."
)


def strip_number(title: str) -> str:
    """'3. Technical data' -> 'Technical data'."""
    return re.sub(r"^\d+\.\s+", "", title)


def walk(items, chapter_title=None, out=None):
    """Yield (path, title, kind, siblings) for every page in the nav."""
    if out is None:
        out = []
    for item in items:
        if isinstance(item, str):                       # a bare path: a section's own page
            out.append((item, chapter_title, "section-index", items))
        elif isinstance(item, dict):
            for title, value in item.items():
                if isinstance(value, str):
                    out.append((value, title, "page", items))
                else:
                    walk(value, title, out)
    return out


def landing():
    return (
        "---\nhide:\n  - toc\n---\n\n"
        f"# {MANUAL_TITLE}\n\n"
        f"![Spectral Micro driver]({HERO}){{ .hero }}\n\n"
        f"<!-- doc-meta: {MANUAL_KEY} -->\n\n"
        f"{PUBLISHER}\n"
    )


def about():
    return (
        DRAFT +
        "# About this manual\n\n"
        "## Scope and audience\n\n"
        f"*Stub.* One paragraph on what the {MANUAL_TITLE} covers, who it is for, and what must be read first.\n\n"
        "## Finding your way\n\n"
        '--8<-- "navigation.md"\n\n'
        "## Warnings and notes\n\n"
        "Three kinds of highlighted text appear in this documentation. Read every Danger and Notice before you act "
        "on the step it belongs to.\n\n"
        '--8<-- "symbols.md"\n\n'
        "## Related documents\n\n"
        "<!-- documents-table -->\n\n"
        "## Document history\n\n"
        f"The {MANUAL_TITLE} describes one firmware release; one revision is kept per release, and the version "
        "selector in the header switches between them.\n\n"
        "| Revision | Date | Changes |\n|---|---|---|\n| 2026.A (draft) | — | First version in this form |\n"
    )


def chapter(title, siblings, path):
    lines = [DRAFT.rstrip("\n"), "", f"# {strip_number(title)}", "",
             "*Stub.* One paragraph on what this chapter covers.", "", "## In this chapter", ""]
    folder = Path(path).parent
    for item in siblings:
        if isinstance(item, dict):
            for t, v in item.items():
                if isinstance(v, str) and Path(v).parent == folder and v != path:
                    lines.append(f"- [{t}]({Path(v).name})")
    return "\n".join(lines) + "\n"


def glossary():
    return "# Glossary\n\n" '--8<-- "terminology.md"\n'


def page(title):
    return f"{DRAFT}# {strip_number(title)}\n\n*Stub.*\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    cfg = load_config(str(ROOT / "mkdocs.yml"))
    created = 0
    for path, title, kind, siblings in walk(cfg["nav"]):
        target = DOCS / path
        if target.exists():
            continue
        if path == "index.md":
            text = landing()
        elif path == "about.md":
            text = about()
        elif path.endswith("terminology.md"):
            text = glossary()
        elif kind == "section-index":
            text = chapter(title or Path(path).parent.name, siblings, path)
        else:
            text = page(title or Path(path).stem)
        print(("would create " if args.dry_run else "create ") + path)
        if not args.dry_run:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(text, encoding="utf-8")
        created += 1
    print(f"{created} page(s) {'to create' if args.dry_run else 'created'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
