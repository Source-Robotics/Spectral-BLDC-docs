#!/usr/bin/env python3
"""Tests for hooks/versions.py, hooks/firmware_pages.py and the shipped data files. No network, no firmware
repository: fixtures and the files in the repository. Run: python tools/test_tools.py (the build check runs it on
every push)."""
from __future__ import annotations

import importlib.util
import json
import re
import sys
import tempfile
from pathlib import Path

import yaml

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
pages = load_module("firmware_pages", ROOT / "hooks" / "firmware_pages.py")
from mkdocs.exceptions import PluginError  # noqa: E402

# ---------------------------------------------------------------- the version hook
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

URLS = GOOD.replace("firmware: {repository: x, tag: V108}",
                    "firmware: {repository: x, tag: V108, released: 2026-08-26}\nsoftware:\n  lib: {repository: y, tag: v1.20}")
udata, err = load_text(URLS)
page = hook.URL_RE.sub(lambda m: hook.version_url(m.group(1), m.group(2), m.group(3), udata),
                       "[f](<!-- version-url: firmware -->/src) <!-- version-link: software.lib -->") if udata else err
check("A10 version-url is the files at the tag, version-link a link to them with the version as text",
      page == "[f](x/tree/V108/src) [1.20](y/tree/v1.20)", page)
check("A11 version-link adds the release date when there is one, version-release is the GitHub release",
      udata is not None and hook.version_url("link", "firmware", None, udata) == "[108](x/tree/V108) (2026-08-26)"
      and hook.version_url("release", "firmware", None, udata) == "x/releases/tag/V108")
cdata, err = load_text(URLS.replace("lib: {repository: y, tag: v1.20}", "lib: {repository: y, tag: abc123, version: \"1.20\"}"))
check("A11b a component whose tag is a commit is named by its version",
      cdata is not None and hook.version_url("link", "software", "lib", cdata) == "[1.20](y/tree/abc123)", err)
for bad in (("url", "software", None), ("link", "software", "nope")):
    try:
        hook.version_url(bad[0], bad[1], bad[2], udata)
        check(f"A12 {bad} stops the build", False, "no error")
    except PluginError:
        check(f"A12 a version placeholder without a known component stops the build: {bad[1]}.{bad[2]}", True)
used = sorted({f"{m.group(2)}{'.' + m.group(3) if m.group(3) else ''}" for p in (ROOT / "docs").rglob("*.md")
               for m in hook.URL_RE.finditer(p.read_text(encoding="utf-8"))})
missing = []
for name in used:
    g, _, k = name.partition(".")
    try:
        hook.component(g, k or None, shipped)
    except PluginError:
        missing.append(name)
check("A13 every version placeholder in the docs names a component of the shipped versions.yml", not missing,
      ", ".join(missing))

# ---------------------------------------------------------------- the firmware pages
try:
    d = pages.load()
    loaded, load_err = True, ""
except PluginError as exc:
    d, loaded, load_err = None, False, str(exc)
check("B1 the shipped facts and descriptions load and agree (every command described, layouts fit the frames)", loaded, load_err)
if loaded:
    facts = d["facts"]
    check("B2 the generated facts are from the release versions.yml names", facts["tag"] == shipped["firmware"]["tag"]
          and facts["version"] == shipped["docs_version"], f"{facts['tag']} vs {shipped['firmware']['tag']}")
    pre = facts.get("prerelease")
    check("B2b the generated facts come from the release tag, not a prerelease commit (sync_firmware.py --prerelease)",
          not pre, f"read from commit {pre and pre.get('commit')}: run tools/sync_firmware.py once the tag exists")
    missing = [g["page"] for src in (d["can"], d["uart"]) for g in src["groups"].values()]
    missing = [p for p, base in zip(missing, ["can"] * len(d["can"]["groups"]) + ["uart"] * len(d["uart"]["groups"]))
               if not (ROOT / "docs" / "reference" / base / p).exists()]
    check("B3 every command group has its reference page", not missing, str(missing))
    check("B4 the compatibility table has a row for this docs version",
          any(str(r.get("firmware")) == shipped["docs_version"] for r in d["compat"]["rows"]))
    check("B5 every column of the compatibility table has a key and a title",
          all("key" in c and "title" in c for c in d["compat"]["columns"]))
    gen = ROOT / "docs" / "includes" / "generated" / "firmware_release_notes.md"
    check("B6 the release notes cover the release this site describes",
          gen.exists() and f"## {shipped['firmware']['tag']} (" in gen.read_text(encoding="utf-8"))
    # the hook refuses a description file that drifts from the facts
    bad_can = json.loads(json.dumps(d["can"]))
    if d["can"].get("partial"):   # a partial reference may leave commands out, but not invent one
        bad_can["commands"]["IN_NOPE"] = {"name": "Nope", "group": next(iter(bad_can["groups"])), "description": "x"}
    else:
        bad_can["commands"].pop("IN_ESTOP")
    try:
        pages.check(facts, bad_can, d["uart"])
        refused = False
    except PluginError:
        refused = True
    check("B7 a CAN command the firmware has but the descriptions lack (or one it does not have) stops the build", refused)
    bad_can = json.loads(json.dumps(d["can"]))
    first_form = next(n for n, c in bad_can["commands"].items() if c.get("forms"))
    bad_can["commands"][first_form]["forms"][0]["fields"][0]["bytes"] = "0-7"
    try:
        pages.check(facts, bad_can, d["uart"])
        refused = False
    except PluginError:
        refused = True
    check("B8 a byte layout that does not fit the frame stops the build", refused)
    bad_uart = json.loads(json.dumps(d["uart"]))
    bad_uart["commands"]["Nope"] = {"group": next(iter(bad_uart["groups"])), "description": "x"}
    try:
        pages.check(facts, d["can"], bad_uart)
        refused = False
    except PluginError:
        refused = True
    check("B9 a UART command the firmware lacks stops the build", refused)
    # the rendered tables name every command
    over = pages.can_overview(d)
    check("B10 the CAN overview lists every described command ID",
          all(f"| {e['id']} |" in over for e in facts["can"]["ids"] if e["name"] in d["can"]["commands"]))
    uo = pages.uart_overview(d)
    check("B11 the UART overview lists every described handler",
          all(f"`#{h['name']}`" in uo for h in facts["uart"]["handlers"] if h["name"] in d["uart"]["commands"]))
    with_forms = [n for n, c in d["can"]["commands"].items() if c.get("forms")]
    answered = next((n for n in with_forms if facts["can"]["handlers"].get(n, {}).get("responds")), with_forms[0])
    sec = pages.can_section(answered, d["can"]["commands"][answered], d)
    check("B12 a command section: facts strip, the accepted lengths, the answer",
          "cmd-facts" in sec and "bytes" in sec and ("Respond_" in sec or not facts["can"]["handlers"].get(answered, {}).get("responds")), sec[:200])
    dt = pages.defaults_table(d)
    internal = [x["name"] for x in facts["defaults"] if not x.get("setting")]
    shown = [x["name"] for x in facts["defaults"] if x.get("setting")]
    check("B13 the defaults table: what #Default sets and #Save keeps, the settings only, no internal state",
          "After `#Default`" in dt and "Kept by `#Save`" in dt and bool(shown) and bool(internal)
          and all(f"| `{n}` |" in dt for n in shown) and not any(f"| `{n}` |" in dt for n in internal if n not in shown),
          dt[:200])
    # the parameters (firmware 109 and newer): every PARAM_* number described, nothing invented, one row each
    if facts["can"].get("params"):
        pt = pages.params_tables(d)
        check("B14 the parameter tables list every parameter of the firmware with its number",
              all(f"| {p['id']} | `{p['name']}` |" in pt for p in facts["can"]["params"]), pt[:200])
        bad = json.loads(json.dumps(d["params"]))
        bad["params"].pop(next(iter(bad["params"])))
        try:
            pages.check_params(facts, bad)
            refused = False
        except PluginError:
            refused = True
        check("B15 a parameter the firmware has but parameters.yml lacks stops the build", refused)
    # a UART handler the serial parser does not accept is flagged in the overview and in its group's table; a
    # parser without a list of its own (firmware 109 and newer) refuses nothing
    fake = json.loads(json.dumps({k: d[k] for k in ("facts", "uart")}))
    fake["facts"]["uart"]["accepted"] = [h["name"] for h in fake["facts"]["uart"]["handlers"]]
    name = next(iter(fake["uart"]["commands"]))
    fake["facts"]["uart"]["accepted"].remove(name)
    group = fake["uart"]["commands"][name]["group"]
    check("B16 a command the parser does not accept is flagged as answered Unknown command",
          f"`#{name}`" in pages.uart_overview(fake).split("does not accept")[0].rsplit("handler for", 1)[-1]
          and "does not accept the name" in pages.uart_group(group, fake))
    fake["facts"]["uart"]["accepted"] = []
    check("B16b a parser without a command list flags nothing", not pages.refused(fake))


# ---------------------------------------------------------------- the sync tool, on fixtures
sync = load_module("sync_firmware", ROOT / "tools" / "sync_firmware.py")
sync.MODE_NAMES.update({2: "velocity", 5: "open loop", 6: "gripper"})
UART_FIXTURE = """
            if (strcmp(command, "Ud") == 0)
            {
                PID.Ud_setpoint = atoi(argument);
                // controller.Controller_mode = 6;
                /* controller.Controller_mode = 5; */
            }
            else if (strcmp(command, "V") == 0)
            {
                PID.Velocity_setpoint = atoi(argument);
                controller.Controller_mode = 2; // velocity mode
            }
"""
modes = {h["name"]: h["mode"] for h in sync.uart_handlers(UART_FIXTURE)}
check("C1 a commented-out Controller_mode assignment is not a mode the command enters",
      modes == {"Ud": "", "V": "velocity"}, str(modes))
COMMON_FIXTURE = """
    volatile int CAN_ID = 0; // node ID
    volatile int cyclic_period = 0; // ms
    volatile int interrupt_tick = 0; // ISR ticks
"""
EEPROM_FIXTURE = """
static void Load_settings_from_eeprom()
{
  controller.CAN_ID = readInt(CAN_ID_EEPROM);
}
void read_config()
{
  Load_settings_from_eeprom();
}
void Write_config()
{
  writeInt(CAN_ID_EEPROM, controller.CAN_ID);
}
static void Set_Default_settings_block()
{
  writeInt(CAN_ID_EEPROM, 0);
}
void Set_Default_config()
{
  Set_Default_settings_block();
}
"""
dfl = {x["name"]: x for x in sync.defaults(COMMON_FIXTURE, EEPROM_FIXTURE, "",
                                          "controller.cyclic_period = atoi(argument);", "", "")}
check("C2 the defaults: a saved setting with its #Default value, a RAM-only setting, internal state left out",
      dfl["CAN_ID"]["setting"] and dfl["CAN_ID"]["after_default"] == "0" and dfl["CAN_ID"]["saved"] == "yes"
      and dfl["cyclic_period"]["setting"] and dfl["cyclic_period"]["saved"] == "no"
      and not dfl["interrupt_tick"]["setting"], str(dfl))

# ---------------------------------------------------------------- E. the figures hook
fig = load_module("figures_hook", ROOT / "hooks" / "figures.py")
pair = "\n".join(["Text.", "", '![A board](a.webp#only-light){ width="9" }',
                  '![A board](a_dark.webp#only-dark){ width="9" }', "", "More."])
out, n = fig.transform(pair, 1, "3.")
check("E1 a light and a dark picture are one figure, numbered on from the chapter's count, alt text as caption",
      n == 1 and out.count("<figure") == 1 and "<figcaption>Figure 3.2: A board.</figcaption>" in out, out)
inline = "\n".join(["A line of text", "![A board](a.webp)", "", "![Hero](h.webp){ .hero }", ""])
out, n = fig.transform(inline, 0, "")
check("E2 a picture inside a paragraph and a hero picture are left alone", n == 0 and "<figure" not in out, out)
check("E3 numbered chapters count across pages, other pages on their own",
      fig.chapter("03-technical-data/connectors.md") == ("03-technical-data", "3.")
      and fig.chapter("02-safety.md") == ("02-safety.md", "2.")
      and fig.chapter("guides/quadruped.md") == ("guides/quadruped.md", ""))
shot = "\n".join(['![Before](b.webp)', "", '<figure class="gui-shot" markdown="1">', '<div markdown="1">', "",
                  '![A screen](s.jpg){ width="9" }', "", "</div>",
                  '<figcaption markdown="1">Figure 7: **1. Port:** pick it.</figcaption>', "</figure>", "",
                  '![After](c.webp)', ""])
out, n = fig.transform(shot, 0, "5.")
check("E4 an HTML figure is numbered in sequence, a typed number replaced, the picture inside it left alone",
      n == 3 and out.count("<figure") == 3 and '<figcaption markdown="1">Figure 5.2: **1. Port:** pick it.' in out
      and "Figure 5.1: Before." in out and "Figure 5.3: After." in out and "Figure 7" not in out, out)
typed = [str(p.relative_to(ROOT)) for p in (ROOT / "docs").rglob("*.md")
         if "generated" not in p.parts and re.search(r"<figcaption[^>]*>\s*Figure\s+\d", p.read_text(encoding="utf-8"))]
check("E5 no caption carries a number typed by hand (the hook numbers them)", not typed, "; ".join(typed))

# ---------------------------------------------------------------- F. the known issues hook
ki = load_module("known_issues_hook", ROOT / "hooks" / "known_issues.py")
DOCS = ROOT / "docs"
try:
    shipped_ki, err = ki.load(ROOT / "known_issues.yml", DOCS), None
except PluginError as exc:
    shipped_ki, err = None, str(exc)
check("F1 known_issues.yml loads, and every issue's page exists", shipped_ki is not None, err)
check("F2 an issue's link is relative to the page it lands on",
      ki.link({"page": "06-operation/gripper-mode.md#moving", "title": "T"}, "08-troubleshooting/known-issues.md")
      == "[T](../06-operation/gripper-mode.md#moving)")
ISSUE = {"id": "KI-1", "component": "c", "summary": "s", "workaround": "w", "page": "index.md", "title": "t",
         "status": "open", "since": "2026-11-04"}


def load_issues(issues):
    text = yaml.safe_dump({"components": {"c": {"name": "C", "version": "1"}}, "issues": issues})
    with tempfile.NamedTemporaryFile("w", suffix=".yml", delete=False) as f:
        f.write(text.replace("'2026-11-04'", "2026-11-04"))
    try:
        return ki.load(f.name, DOCS), None
    except PluginError as exc:
        return None, str(exc)
    finally:
        Path(f.name).unlink()


_, err = load_issues([dict(ISSUE, component="x")])
check("F3 an unknown component stops the build", err is not None and "not under components" in err, err)
_, err = load_issues([ISSUE, dict(ISSUE)])
check("F4 a repeated id stops the build", err is not None and "twice" in err, err)
kdata, err = load_issues([ISSUE, dict(ISSUE, id="KI-2", status="fixed", fixed_in="109")])
out = ki.all_issues(kdata, "08-troubleshooting/known-issues.md") if kdata else ""
check("F5 open issues are listed by component, fixed ones under Fixed with their release",
      "### C" in out and "### Fixed" in out and "| KI-2 | s | 109 |" in out and "| KI-1 | s | w |" in out, err or out)

print(f"\n{len(fails)} failure(s)" if fails else "\nall checks passed")
sys.exit(1 if fails else 0)
