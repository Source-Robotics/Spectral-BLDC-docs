#!/usr/bin/env python3
"""Tests for hooks/versions.py. No network. Run: python tools/test_tools.py (the build check runs it on every push)."""
from __future__ import annotations

import importlib.util
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
fails = []


def check(name, cond, detail=""):
    print(("  PASS  " if cond else "  FAIL  ") + name + (f"   [{detail}]" if detail and not cond else ""))
    if not cond:
        fails.append(name)


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


hook = load_module("versions_hook", ROOT / "hooks" / "versions.py")
from mkdocs.exceptions import PluginError  # noqa: E402

GOOD = """docs_version: "108"
firmware: {repository: x, tag: V108}
manuals:
  spectral: {number: SR-5002, title: Spectral Micro Manual, revision: 2026.A, status: draft, published: null, firmware: true,
             applies_to: "Spectral Micro PCB v2.0", covers: the driver}
  guide: {number: SR-5101, title: Some Guide, revision: 2026.B, status: published, published: 2026-11-02,
          applies_to: "", covers: a guide}
"""


def load_text(text):
    with tempfile.NamedTemporaryFile("w", suffix=".yml", delete=False) as f:
        f.write(text)
    try:
        return hook.load(f.name), None
    except PluginError as exc:
        return None, str(exc)
    finally:
        Path(f.name).unlink()


data, err = load_text(GOOD)
check("A1 a valid versions.yml loads", data is not None, err)
d, e = load_text(GOOD.replace("tag: V108", "tag: v108"))
check("A1b a lowercase tag loads (the v101 tag of the Spectral firmware)", d is not None, e)
for label, bad, word in (
        ("docs_version not a release number", GOOD.replace('"108"', '"1.08"'), "docs_version"),
        ("a tag of another release", GOOD.replace("tag: V108", "tag: V107"), "does not belong"),
        ("a malformed tag", GOOD.replace("tag: V108", "tag: 108"), "firmware.tag"),
        ("a revision not YEAR.LETTER", GOOD.replace("2026.A", "A"), "YEAR.LETTER"),
        ("an unknown status", GOOD.replace("status: draft", "status: final"), "status"),
        ("published without a date", GOOD.replace("published: 2026-11-02", "published: null"), "publication date"),
        ("a missing field", GOOD.replace("covers: the driver", "covers: ''"), "lacks covers")):
    d, e = load_text(bad)
    check(f"A2 refused: {label}", d is None and word in (e or ""), e)
meta = hook.meta_block("spectral", data)
check("A3 a firmware document's box: number, firmware version, revision (draft), applies to the firmware",
      "SR-5002" in meta and "**Firmware version:** 108" in meta and "2026.A (draft)" in meta
      and "**Applies to:** Spectral Micro PCB v2.0, firmware 108" in meta, meta)
meta = hook.meta_block("guide", data)
check("A4 a published document's box: no firmware line, the date, no (draft)",
      "Firmware version" not in meta and "2026-11-02" in meta and "(draft)" not in meta, meta)
try:
    hook.meta_block("nope", data)
    raised = False
except PluginError:
    raised = True
check("A5 an unknown manual stops the build", raised)
table = hook.documents_table(data)
check("A6 the documents table: one row per manual", table.count("| SR-") == 2 and "108" in table, table)
hook._facts = data
page = hook.on_page_markdown("x\n<!-- doc-meta: spectral -->\ny\n<!-- documents-table -->\n", None, None, None)
check("A7 both placeholders are replaced", "doc-meta:" not in page and "documents-table" not in page and "SR-5101" in page)
shipped = hook.load(ROOT / "versions.yml")
check("A8 the shipped versions.yml loads", bool(shipped["docs_version"]))
check("A9 every placeholder in the docs names a manual of versions.yml",
      all(k in shipped["manuals"]
          for p in (ROOT / "docs").rglob("*.md") for k in hook.META_RE.findall(p.read_text(encoding="utf-8"))))

print(f"\n{len(fails)} failure(s)" if fails else "\nall checks passed")
sys.exit(1 if fails else 0)
