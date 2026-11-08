#!/usr/bin/env python3
"""Read the firmware at a release tag and write the generated files the reference pages are built from (the
same idea as par6's tools/sync_runtime.py: facts come from the TAGGED code, never from uncommitted work).

    python tools/sync_firmware.py                      write docs/includes/generated/ from firmware.tag in versions.yml
    python tools/sync_firmware.py --check              exit 1 when a generated file differs from what the tag gives
    python tools/sync_firmware.py --firmware PATH --tag V108
    python tools/sync_firmware.py --print uart|can|defaults [--tag V103]   print one table instead of writing
    python tools/sync_firmware.py --no-network         keep the release notes that are there (no GitHub API call)
    python tools/sync_firmware.py --prerelease 260c774 --no-network
                                                       before the release tag exists: read that commit instead

It reads the firmware repository with `git show <tag>:<file>` and writes, into docs/includes/generated/:

    firmware_facts.json         what the code says: FIRMWARE_VERSION, every CAN command ID with the lengths its
                                handler accepts and the response it sends, every frame the driver transmits with
                                its length (communication_CAN.cpp, and scope.cpp from 2026-11), every parameter
                                number of IN_PARAM_SET / IN_PARAM_GET (PARAM_* in constants.h, from 2026-11), every
                                UART command the parser accepts and every UART handler with its kind (Set/Get,
                                Get, Action), argument type, the mode it enters and the response it prints, the
                                start values of the controller, PID and gripper structures with what #Default
                                sets and #Save keeps (EEPROM.cpp, settings block 2 included), each marked as a
                                setting or internal state
    firmware_release_notes.md   the GitHub Release notes of every release up to docs_version (the release body is
                                the firmware's changelog, see the firmware repository's release_guide.md)

hooks/firmware_pages.py turns the facts and the hand-written descriptions (docs/includes/can_commands.yml,
uart_commands.yml, parameters.yml) into the reference pages at build time, and tools/test_tools.py checks that the
two agree.

--prerelease REF is for writing the pages of a release before it is tagged: the facts are read from REF (a commit
or a branch; give the commit, a branch moves on), labelled with firmware.tag, and marked "prerelease" with REF's
commit. The firmware's FIRMWARE_VERSION may still be the previous release's number then (it is bumped when the
release is cut). tools/test_tools.py fails while the facts are a prerelease, so such a version is never published:
once the tag exists, run the tool again without the option.

The firmware repository (the last part of firmware.repository in versions.yml) is --firmware, else $FIRMWARE_DIR, else a
folder of that name next to this repository, next to its parent, or under ../../projects; firmware.src names its
source folder. Python 3.11+, PyYAML (installed with MkDocs).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "includes" / "generated"
SRC = "Spectral BLDC Firmware/src"            # overridden by firmware.src in versions.yml
REPO_NAME = "Spectral-Micro-BLDC-controller"   # overridden by the last part of firmware.repository in versions.yml


class SyncError(Exception):
    pass


def find_firmware(arg: str | None) -> Path:
    candidates = [arg, os.environ.get("FIRMWARE_DIR"), ROOT.parent / REPO_NAME, ROOT.parent.parent / REPO_NAME,
                  ROOT.parent.parent / "projects" / REPO_NAME]
    for c in candidates:
        if c and (Path(c) / ".git").exists():
            return Path(c)
    raise SyncError(f"no {REPO_NAME} repository found: pass --firmware PATH or set FIRMWARE_DIR")


def git_show(repo: Path, tag: str, path: str) -> str:
    r = subprocess.run(["git", "-C", str(repo), "show", f"{tag}:{path}"], capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    if r.returncode != 0:
        raise SyncError(f"{tag}:{path} not readable in {repo}: {r.stderr.strip()} (are the tags fetched?)")
    return r.stdout


# ---------------------------------------------------------------- UART

STRCMP = re.compile(r'strcmp\(\s*command\s*,\s*"(\w+)"\s*\)\s*==\s*0')
PRINT = re.compile(r'Serialport\.print(?:ln)?\(\s*"([^"]*)"')
MODE = re.compile(r"Controller_mode\s*=\s*(\d+)")
BLOCK_COMMENT = re.compile(r"/\*.*?\*/", re.S)
LINE_COMMENT = re.compile(r"//[^\n]*")


def strip_comments(code: str) -> str:
    """The code without its comments: a commented-out `// controller.Controller_mode = 6;` is not a fact."""
    return LINE_COMMENT.sub("", BLOCK_COMMENT.sub("", code))
ASSIGN = re.compile(r"^\s*(?:controller|PID|Gripper|FOC|parser)\.\w+\s*=\s*[^=]", re.M)
# Controller_mode number -> name, from firmware.modes in versions.yml (the numbering differs between firmwares).
MODE_NAMES: dict[int, str] = {}


def uart_whitelist(parser_cpp: str) -> list[str]:
    """The command names the serial parser accepts (anything else is dropped before a handler sees it)."""
    return list(dict.fromkeys(STRCMP.findall(parser_cpp)))


def handler_starts(text: str) -> list[list[re.Match]]:
    """The handler conditions, in source order: each a list of the names it compares (`"Cal" || "Calonly"`). A
    strcmp that is not part of an if condition (an argument passed to a function inside a handler) starts nothing."""
    groups: list[list[re.Match]] = []
    for m in STRCMP.finditer(text):
        before = text[:m.start()].rstrip()
        if before.endswith("||") and groups:
            groups[-1].append(m)
        elif re.search(r"\bif\s*\($", before):
            groups.append([m])
    return groups


def uart_handlers(communication_cpp: str) -> list[dict]:
    """One entry per UART handler, in source order; names compared in one condition share the handler."""
    text = communication_cpp
    groups = handler_starts(text)
    out = []
    for i, group in enumerate(groups):
        m = group[0]
        start = m.start()
        end = groups[i + 1][0].start() if i + 1 < len(groups) else len(text)
        block = text[group[-1].end():end]
        # the firmware's own comment lines right above the handler
        before = text[:start].rstrip()
        comments = []
        for line in reversed(before.splitlines()):
            s = line.strip()
            if s.startswith("//"):
                comments.append(s[2:].strip())
            elif s in ("", "{", "}") or s.startswith(("else", "if")):
                if comments or s in ("", "{", "}"):
                    break
            else:
                break
        comments.reverse()
        prints = [p for p in PRINT.findall(block) if p.strip()]
        has_arg = "strlen(argument)" in block
        # atof() until the 2026-11 flash savings, parse_float() since; parse_ints() reads a comma-separated list
        arg_type = ("float" if re.search(r"\b(?:atof|parse_float)\(argument\)", block) else
                    "int" if "atoi(argument)" in block else "int list" if "parse_ints(argument" in block else "")
        mode = MODE.search(strip_comments(block))
        # a handler that changes state is an action: it enters a mode, assigns a variable, or calls a function
        # (Write_config(), Set_Default_config(), Bootloader_ResetIntoBootloader(), ...; prints do not count)
        calls = [c for c in re.findall(r"\b([A-Z]\w+)\s*\(", block) if c not in ("Serialport",)]
        changes = bool(mode) or bool(ASSIGN.search(block)) or bool(calls)
        kind = "Set/Get" if has_arg else ("Action" if changes else "Get")
        for g in group:
            out.append({"name": g.group(1), "kind": kind, "arg": arg_type if has_arg else "",
                        "mode": MODE_NAMES.get(int(mode.group(1)), mode.group(1)) if mode else "",
                        "response": (prints[0].strip() if prints else ""), "comment": " ".join(comments)})
    return out


# ---------------------------------------------------------------- CAN

DEFINE = re.compile(r"^#define[ \t]+((?:IN_|OUT_|OUT_IN_)[A-Z0-9_]+|HEARTBEAT_SETUP)[ \t]+(\d+)[ \t]*(?://[ \t]*(.*))?$", re.M)
CASE = re.compile(r"case\s+([A-Z0-9_]+)\s*:")
LEN = re.compile(r"CAN_RX_msg\.len\s*==\s*(\d+)")
LEN_MIN = re.compile(r"CAN_RX_msg\.len\s*>=\s*(\d+)")   # a handler that takes any length from N up
# a response function, called with or without arguments (Param_value_CAN(CAN_RX_msg.data[0]) since 2026-11)
RESPONSE_FN = re.compile(r"\b([A-Z][A-Za-z_0-9]*(?:_CAN|_response|_pack|_pack_data))\((?:[^();]|\([^();]*\))*\)\s*;")
# every function definition (the end of the one before); a transmitting one sets a frame's length and its ID
FN_START = re.compile(r"^(?:static\s+)?(?:void|bool|int|float|uint\d+_t|int\d+_t)\s+(\w+)\s*\([^)]*\)\s*\{", re.M)
TX_LEN = re.compile(r"\b(?:CAN_TX_msg|msg)\.len\s*=\s*(\d+)")
TX_ID = re.compile(r"Combine_2_CAN_ID\([^,]+,\s*([A-Z0-9_]+)")


def can_ids(constants_h: str) -> list[dict]:
    return [{"name": n, "id": int(v), "comment": (c or "").strip()} for n, v, c in DEFINE.findall(constants_h)]


def can_handlers(communication_can_cpp: str) -> dict[str, dict]:
    """For every `case IN_X:` of the receive switch: the frame lengths it accepts and the response functions it calls."""
    text = communication_can_cpp
    matches = list(CASE.finditer(text))
    out = {}
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        block = text[m.start():end]
        # up to the case's own `break;`: the first one that is not inside a loop or an if of the handler
        body = block
        for bm in re.finditer(r"break;", block):
            if block[:bm.start()].count("{") - block[:bm.start()].count("}") <= 1:
                body = block[:bm.start()]
                break
        out[m.group(1)] = {"lengths": sorted({int(x) for x in LEN.findall(body)}),
                           "responds": list(dict.fromkeys(RESPONSE_FN.findall(body))),
                           "empty": body.strip().count("\n") <= 1}
        least = LEN_MIN.findall(body)
        if least:
            out[m.group(1)]["min_length"] = min(int(x) for x in least)
    return out


def can_tx(*sources: str) -> dict[str, dict]:
    """Every frame the driver transmits: the function name -> its command ID define and length (the first length
    the function sets: OUT_PARAM_VALUE's 5; its 1-byte "unknown" answer is in the descriptions). The sources are
    communication_CAN.cpp and, from 2026-11, scope.cpp (OUT_BUFFER_DATA, sent from the main loop)."""
    out = {}
    for text in sources:
        matches = list(FN_START.finditer(text))
        for i, m in enumerate(matches):
            end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
            block = strip_comments(text[m.start():end])
            length, ident = TX_LEN.search(block), TX_ID.search(block)
            if length and ident:
                out[m.group(1)] = {"len": int(length.group(1)), "id_define": ident.group(1)}
    return out


def firmware_version(constants_h: str, tag: str) -> str:
    m = re.search(r"^#define\s+FIRMWARE_VERSION\s+(\d+)", constants_h, re.M)
    if m:
        if f"V{m.group(1)}" != tag:
            raise SyncError(f"constants.h at {tag} says FIRMWARE_VERSION {m.group(1)}")
        return m.group(1)
    return tag.lstrip("V")       # V104 and older: the version came from EEPROM


# ---------------------------------------------------------------- defaults and errors

FIELD = re.compile(r"^[ \t]*volatile[ \t]+(?:unsigned[ \t]+)?(?:int|float|bool|uint\d+_t|int\d+_t)[ \t]+(\w+)[ \t]*=[ \t]*([^;]+);[ \t]*(?://[ \t]*(.*))?$", re.M)
STRUCT_SET = re.compile(r"\b(?:controller|PID|Gripper)\.(\w+)\s*=\s*([^;=][^;]*);")
READ_KEY = re.compile(r"^read(?:Int|Float)\(\s*(\w+)\s*\)$")
READ_TERNARY = re.compile(r"^\(\s*read(?:Int|Float)\(\s*(\w+)\s*\)\s*==\s*(-?\d+)\s*\)\s*\?\s*(-?\d+)\s*:\s*(-?\d+)$")
WRITE_KEY = re.compile(r"\bwrite(?:Int|Float)\(\s*(\w+)\s*,\s*([^;]+?)\)\s*;")
LIMIT = re.compile(r"[<>]=?\s*-?\s*(?:controller|PID)\.(\w+)")
# The words that mark a value set from outside: a UART argument, or the data of a CAN frame.
FROM_UART = ("argument", "var", "temp_var")
FROM_CAN = ("CAN_RX_msg", "temp_buffer", "temp_buffer1", "temp_buffer2", "bitArray", "value", "new_can_id")


def function_body(code: str, name: str) -> str:
    """The body of the C function `name` (between its braces), or "" when the code has none."""
    m = re.search(rf"\b{re.escape(name)}\s*\([^;{{)]*\)\s*\{{", code)
    if not m:
        return ""
    depth, i = 1, m.end()
    while i < len(code) and depth:
        depth += {"{": 1, "}": -1}.get(code[i], 0)
        i += 1
    return code[m.end():i - 1]


def eeprom_facts(eeprom_cpp: str, constants_h: str) -> tuple[dict, dict, dict]:
    """What EEPROM.cpp does with each field: where it is loaded from at power-up (field -> key, or a constant),
    what #Default writes (key -> value), and what #Save writes (field -> key)."""
    code = strip_comments(eeprom_cpp)
    loads: dict[str, dict] = {}
    # settings block 2 (2026-11): its own load, defaults, and write functions beside the first two blocks'
    for fn in ("read_config", "Load_calibration_from_eeprom", "Load_settings_from_eeprom", "Load_settings2_from_eeprom"):
        for field, rhs in STRUCT_SET.findall(function_body(code, fn)):
            rhs = rhs.strip()
            if field in loads:
                continue
            m, t = READ_KEY.match(rhs), READ_TERNARY.match(rhs)
            if m:
                loads[field] = {"key": m.group(1)}
            elif t:
                loads[field] = {"key": t.group(1), "if": int(t.group(2)), "then": t.group(3), "else": t.group(4)}
            elif re.fullmatch(r"[A-Z_][A-Z0-9_]*", rhs):
                c = re.search(rf"^#define[ \t]+{rhs}[ \t]+(\S+)", constants_h, re.M)
                if c:
                    loads[field] = {"value": c.group(1)}
    # block 2 writes its defaults from RAM (controller.x), which Settings2_defaults_to_ram() sets just before
    ram_defaults = {f: v.strip() for f, v in STRUCT_SET.findall(function_body(code, "Settings2_defaults_to_ram"))}
    written: dict[str, str] = {}
    for fn in ("Set_Default_config", "Set_Default_calibration_block", "Set_Default_settings_block",
               "Set_Default_settings2_block"):
        for key, value in WRITE_KEY.findall(function_body(code, fn)):
            value = value.strip()
            f = re.fullmatch(r"controller\.(\w+)", value)
            written[key] = ram_defaults.get(f.group(1), value) if f else value
    saved: dict[str, str] = {}
    for fn in ("Write_config", "Write_settings2_block"):
        for key, value in WRITE_KEY.findall(function_body(code, fn)):
            f = re.search(r"\b(?:controller|PID|Gripper)\.(\w+)", value)
            if f:
                saved.setdefault(f.group(1), key)
    return loads, written, saved


def resolve(value: str, defines: str, depth: int = 4) -> str:
    """A #define name as its number, with the name kept: CURRENT_BANDWIDTH_DEFAULT -> "160 (CURRENT_BANDWIDTH_DEFAULT)".
    Anything that is not a single defined name comes back unchanged."""
    name, v = value, value
    for _ in range(depth):
        if not re.fullmatch(r"[A-Z_][A-Z0-9_]*", v):
            break
        m = re.search(rf"^#define[ \t]+{v}[ \t]+([^\s/]+)", defines, re.M)
        if not m:
            break
        v = m.group(1)
    return value if v == name else f"{v} ({name})"


def set_from_outside(communication_cpp: str, communication_can_cpp: str) -> set[str]:
    """The fields a UART command or a CAN frame sets from its own data (not the flags they reset to a constant)."""
    names = set()
    for code, words in ((communication_cpp, FROM_UART), (communication_can_cpp, FROM_CAN)):
        for field, rhs in STRUCT_SET.findall(strip_comments(code)):
            if any(re.search(rf"\b{w}\b", rhs) for w in words):
                names.add(field)
    return names


def after_default(field: str, loads: dict, written: dict, saved: dict) -> str:
    """The value the driver runs with after #Default (which writes the EEPROM and reads it back)."""
    ld = loads.get(field)
    if ld and "value" in ld:
        return ld["value"]
    if ld:
        v = written.get(ld["key"])
        if v is None:
            return ""
        if "if" in ld:
            try:
                return ld["then"] if int(v) == ld["if"] else ld["else"]
            except ValueError:
                return v
        return v
    if field in saved and saved[field] in written:
        return f"{written[saved[field]]} in the EEPROM, not read back"
    return "—"


def kept_by_save(field: str, loads: dict, saved: dict) -> str:
    ld = loads.get(field)
    if field in saved and ld and "key" in ld:
        return "yes"
    if ld and "value" in ld:
        return "no: set by the firmware"
    if field in saved:
        return "written, not read back"
    return "no"


def defaults(common_h: str, eeprom_cpp: str = "", constants_h: str = "", communication_cpp: str = "",
             communication_can_cpp: str = "", motor_control_cpp: str = "") -> list[dict]:
    """Every field with a start value in common.h. `setting` marks the ones a user meets: stored in the EEPROM, set
    by a UART command or a CAN frame, or a limit the control code compares against; the rest is internal state."""
    loads, written, saved = eeprom_facts(eeprom_cpp, constants_h)
    outside = set_from_outside(communication_cpp, communication_can_cpp)
    limits = set(LIMIT.findall(strip_comments(motor_control_cpp)))
    out = []
    for n, v, c in FIELD.findall(common_h):
        out.append({"name": n, "value": resolve(v.strip(), constants_h), "comment": (c or "").strip(),
                    "setting": n in loads or n in saved or n in outside or n in limits,
                    "after_default": resolve(after_default(n, loads, written, saved), constants_h),
                    "saved": kept_by_save(n, loads, saved)})
    return out


# ---------------------------------------------------------------- tables (--print)

def esc(text) -> str:
    return str(text or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("|", r"\|")


def table_uart(facts: dict) -> str:
    rows = ["| Command | Kind | Argument | Enters mode | Response starts with | Firmware comment |", "|---|---|---|---|---|---|"]
    for h in facts["uart"]["handlers"]:
        rows.append(f"| `{h['name']}` | {h['kind']} | {h['arg']} | {h['mode']} | {esc(h['response'])} | {esc(h['comment'])} |")
    return "\n".join(rows) + "\n"


def table_can(facts: dict) -> str:
    rows = ["| ID | Name | Direction | Handled | Accepted lengths | Driver answers with | Firmware comment |", "|---|---|---|---|---|---|---|"]
    handlers = facts["can"]["handlers"]
    for e in sorted(facts["can"]["ids"], key=lambda e: e["id"]):
        n = e["name"]
        direction = "host → driver" if n.startswith("IN_") or n == "HEARTBEAT_SETUP" else "driver → host"
        if n.startswith("OUT_IN"):
            direction = "host → driver (remote frame), driver → host"
        h = handlers.get(n)
        handled = "no" if h is None or h["empty"] else "yes"
        lengths = ", ".join(str(x) for x in h["lengths"]) if h and h["lengths"] else ("—" if h else "")
        rows.append(f"| {e['id']} | `{n}` | {direction} | {handled} | {lengths} | {esc(', '.join(h['responds']) if h else '')} | {esc(e['comment'])} |")
    return "\n".join(rows) + "\n"


def table_defaults(facts: dict) -> str:
    rows = ["| Variable | Start value | After #Default | Kept by #Save | Setting | Firmware comment |",
            "|---|---|---|---|---|---|"]
    for d in facts["defaults"]:
        rows.append(f"| `{d['name']}` | {esc(d['value'])} | {esc(d.get('after_default'))} | {esc(d.get('saved'))} | "
                    f"{'yes' if d.get('setting') else ''} | {esc(d['comment'])} |")
    return "\n".join(rows) + "\n"


# ---------------------------------------------------------------- release notes

def release_notes(docs_version: str) -> str:
    """Every GitHub Release up to docs_version, newest first: `## V108 (2026-08-26)` + the release body."""
    api = f"https://api.github.com/repos/Source-Robotics/{REPO_NAME}/releases?per_page=100"
    try:
        with urllib.request.urlopen(urllib.request.Request(api, headers={"User-Agent": "Source-Robotics-docs"}), timeout=30) as r:
            releases = json.load(r)
    except Exception as exc:
        raise SyncError(f"GitHub releases not readable: {exc} (use --no-network to keep the file that is there)")
    parts = []
    for rel in sorted(releases, key=lambda x: int(re.sub(r"\D", "", x["tag_name"]) or 0), reverse=True):
        number = int(re.sub(r"\D", "", rel["tag_name"]) or 0)
        if number > int(docs_version):
            continue
        body = (rel.get("body") or "").strip().replace("\r", "")
        body = re.sub(r"^### ", "#### ", body, flags=re.M)
        parts.append(f"## {rel['tag_name']} ({rel['published_at'][:10]})\n\n{body or '*No release notes.*'}\n")
    if not parts:
        raise SyncError("no release found")
    return "\n".join(parts)


# ---------------------------------------------------------------- build

def read_optional(read, name: str) -> str:
    """A source file that older releases do not have (scope.cpp, watchdog_action.h: 2026-11), or ""."""
    try:
        return read(name)
    except SyncError:
        return ""


PARAM = re.compile(r"^#define[ \t]+(PARAM_[A-Z0-9_]+)[ \t]+(\d+)[ \t]*(?://[ \t]*(.*))?$", re.M)


def can_params(constants_h: str) -> list[dict]:
    """The parameter numbers of IN_PARAM_SET / IN_PARAM_GET (2026-11): name, number, the firmware's comment with
    its continuation lines (a `//` line right below, indented)."""
    out = []
    lines = constants_h.splitlines()
    for i, line in enumerate(lines):
        m = PARAM.match(line)
        if not m:
            continue
        comment = [(m.group(3) or "").strip()]
        for nxt in lines[i + 1:]:
            c = re.match(r"^[ \t]+//[ \t]*(.*)$", nxt)
            if not c:
                break
            comment.append(c.group(1).strip())
        out.append({"name": m.group(1), "id": int(m.group(2)), "comment": " ".join(x for x in comment if x)})
    return out


def facts_for(repo: Path, tag: str, prerelease: str | None = None) -> dict:
    """The facts of release `tag`, read at the tag, or at commit `prerelease` before the tag exists."""
    ref = prerelease or tag
    read = lambda name: git_show(repo, ref, f"{SRC}/{name}")
    constants, can_cpp, comm_cpp = read("constants.h"), read("communication_CAN.cpp"), read("communication.cpp")
    defines = constants + "\n" + read_optional(read, "watchdog_action.h")
    commit = subprocess.run(["git", "-C", str(repo), "rev-list", "-n", "1", ref], capture_output=True, text=True).stdout.strip()
    if prerelease and not commit:
        raise SyncError(f"--prerelease {prerelease}: no such commit in {repo}")
    # before the release is cut, FIRMWARE_VERSION may still name the release before it
    version = tag.lstrip("Vv") if prerelease else firmware_version(constants, tag)
    facts = {
        "tag": tag, "version": version, "commit": commit[:12],
        "can": {"ids": can_ids(constants), "handlers": can_handlers(can_cpp),
                "tx": can_tx(can_cpp, read_optional(read, "scope.cpp"))},
        "uart": {"accepted": uart_whitelist(read("SerialPacketParser.cpp")), "handlers": uart_handlers(comm_cpp)},
        "defaults": defaults(read("common.h"), read("EEPROM.cpp"), defines, comm_cpp, can_cpp,
                             read("motor_control.cpp")),
    }
    params = can_params(constants)
    if params:
        facts["can"]["params"] = params
    if prerelease:
        facts["prerelease"] = {"ref": prerelease, "commit": commit[:12],
                               "firmware_version_in_source": re.search(r"^#define\s+FIRMWARE_VERSION\s+(\d+)",
                                                                        constants, re.M).group(1)}
    return facts


def build(repo: Path, tag: str, docs_version: str, network: bool, prerelease: str | None = None) -> dict[str, str]:
    facts = facts_for(repo, tag, prerelease)
    if facts["version"] != docs_version:
        raise SyncError(f"release {tag} is firmware {facts['version']}, docs_version is {docs_version} (versions.yml)")
    if prerelease and network:
        raise SyncError("--prerelease: the release has no notes on GitHub yet; add --no-network")
    head = (f"<!-- Generated by tools/sync_firmware.py from {REPO_NAME} {tag} ({facts['commit']}). Do not "
            f"edit: change the firmware, release it, then run the tool again. -->\n")
    files = {"firmware_facts.json": json.dumps(facts, indent=1, sort_keys=True) + "\n"}
    if network:
        files["firmware_release_notes.md"] = head + "\n" + release_notes(docs_version)
    return files


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--firmware", help="the firmware repository (default: next to this repository, or $FIRMWARE_DIR)")
    ap.add_argument("--tag", help="the release tag (default: firmware.tag in versions.yml)")
    ap.add_argument("--check", action="store_true", help="write nothing; exit 1 when a generated file is out of date")
    ap.add_argument("--no-network", action="store_true", help="do not fetch the release notes from GitHub")
    ap.add_argument("--print", choices=["uart", "can", "defaults"], help="print one table and exit")
    ap.add_argument("--prerelease", metavar="REF", help="before the release tag exists: read the firmware at commit "
                    "REF for the release firmware.tag names (never published: the tests fail on it)")
    args = ap.parse_args(argv)
    facts_yml = yaml.safe_load((ROOT / "versions.yml").read_text(encoding="utf-8"))
    tag = args.tag or facts_yml["firmware"]["tag"]
    global SRC, REPO_NAME
    SRC = facts_yml["firmware"].get("src", SRC)
    REPO_NAME = facts_yml["firmware"]["repository"].rstrip("/").rsplit("/", 1)[-1]
    MODE_NAMES.update({int(k): str(v) for k, v in (facts_yml["firmware"].get("modes") or {}).items()})
    if not MODE_NAMES:
        print("sync_firmware: versions.yml lacks firmware.modes (Controller_mode number -> name)", file=sys.stderr)
        return 2
    try:
        repo = find_firmware(args.firmware)
        if args.print:
            facts = facts_for(repo, tag, args.prerelease)
            sys.stdout.write({"uart": table_uart, "can": table_can, "defaults": table_defaults}[args.print](facts))
            return 0
        files = build(repo, tag, str(facts_yml["docs_version"]), network=not args.no_network,
                      prerelease=args.prerelease)
    except SyncError as exc:
        print(f"sync_firmware: {exc}", file=sys.stderr)
        return 2
    stale = [n for n, text in files.items() if not (OUT / n).exists() or (OUT / n).read_text(encoding="utf-8") != text]
    if args.check:
        for n in stale:
            print(f"out of date: docs/includes/generated/{n}")
        print("generated files up to date" if not stale else f"{len(stale)} out of date: run tools/sync_firmware.py")
        return 1 if stale else 0
    OUT.mkdir(parents=True, exist_ok=True)
    for n in stale:
        (OUT / n).write_text(files[n], encoding="utf-8")
    source = f"{tag}, PRERELEASE from commit {args.prerelease}" if args.prerelease else tag
    print(f"from {REPO_NAME} {source}: {len(stale)} generated file(s) written, {len(files) - len(stale)} unchanged")
    return 0


if __name__ == "__main__":
    sys.exit(main())
