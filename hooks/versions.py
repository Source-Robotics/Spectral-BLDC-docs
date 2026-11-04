"""Write the version facts of versions.yml into the pages (the same hook as Source-Robotics/par6, for firmware docs).

Five placeholders, each replaced when the site is built:

    <!-- doc-meta: KEY -->      a manual's version box, on its landing page: document number, firmware version (for
                                a document that describes one firmware release), revision, publication date, what
                                it applies to
    <!-- documents-table -->    the list of every document, on the About page
    <!-- version-url: COMPONENT -->      the address of the component's files at its tag, {repository}/tree/{tag}, to
                                build a link to a folder: COMPONENT is firmware or software.KEY
    <!-- version-link: COMPONENT -->     a link to that address with the version as its text (the tag without its
                                V, or the component's version: when the tag is a commit), and the release date
                                when versions.yml has one (the same two as PAROL-docs')
    <!-- version-release: COMPONENT -->  the address of the component's GitHub release, {repository}/releases/tag/{tag}

The facts live in versions.yml only. A malformed or missing fact, or an unknown manual, stops the build: a version
on a page is never guessed. Registered in mkdocs.yml under `hooks:`.
"""
from __future__ import annotations

import datetime
import re
from pathlib import Path

import yaml
from mkdocs.exceptions import PluginError

META_RE = re.compile(r"<!--\s*doc-meta:\s*([A-Za-z0-9_-]+)\s*-->")
TABLE_RE = re.compile(r"<!--\s*documents-table\s*-->")
URL_RE = re.compile(r"<!--\s*version-(url|link|release):\s*([A-Za-z0-9_-]+)(?:\.([A-Za-z0-9_-]+))?\s*-->")
REQUIRED = ("number", "title", "revision", "status", "covers")

_facts: dict = {}


def load(path) -> dict:
    """versions.yml, checked. Raises PluginError naming what is wrong."""
    try:
        data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise PluginError(f"versions.yml: {exc}") from exc
    if not isinstance(data, dict):
        raise PluginError("versions.yml: not a mapping")
    docs_version = str(data.get("docs_version", ""))
    if not re.fullmatch(r"\d+", docs_version):
        raise PluginError(f"versions.yml: docs_version {docs_version!r} is not a firmware release number, e.g. \"108\"")
    tag = str((data.get("firmware") or {}).get("tag", ""))
    if not re.fullmatch(r"[Vv]\d+", tag):
        raise PluginError(f"versions.yml: firmware.tag {tag!r} is not a release tag like V108")
    if tag.upper() != f"V{docs_version}":
        raise PluginError(f"versions.yml: firmware.tag {tag} does not belong to docs_version {docs_version}")
    manuals = data.get("manuals")
    if not isinstance(manuals, dict) or not manuals:
        raise PluginError("versions.yml: no manuals")
    for key, doc in manuals.items():
        missing = [f for f in REQUIRED if not (doc or {}).get(f)]
        if missing:
            raise PluginError(f"versions.yml: manual {key!r} lacks {', '.join(missing)}")
        if not re.fullmatch(r"\d{4}\.[A-Z]", str(doc["revision"])):
            raise PluginError(f"versions.yml: manual {key!r} revision {doc['revision']!r} is not YEAR.LETTER, e.g. 2026.A")
        if doc["status"] not in ("draft", "published"):
            raise PluginError(f"versions.yml: manual {key!r} status {doc['status']!r} is not draft or published")
        published = doc.get("published")
        if doc["status"] == "published" and not isinstance(published, datetime.date):
            raise PluginError(f"versions.yml: manual {key!r} is published but has no publication date (YYYY-MM-DD)")
    return data


def meta_block(key: str, data: dict) -> str:
    """The version box of manual `key`."""
    doc = data["manuals"].get(key)
    if doc is None:
        raise PluginError(f"doc-meta: no manual {key!r} in versions.yml")
    draft = doc["status"] == "draft"
    lines = [f"**Document number:** {doc['number']}"]
    if doc.get("firmware"):
        lines.append(f"**Firmware version:** {data['docs_version']}")
    lines.append(f"**Revision:** {doc['revision']}" + (" (draft)" if draft else ""))
    published = doc.get("published")
    lines.append(f"**Published:** {published.isoformat() if isinstance(published, datetime.date) else '—'}")
    applies = [f"firmware {data['docs_version']}"] if doc.get("firmware") else []
    if doc.get("applies_to"):
        applies.insert(0, str(doc["applies_to"]))
    lines.append(f"**Applies to:** {', '.join(applies)}")
    lines.append("*Original instructions*")
    return '<div class="doc-meta" markdown>\n\n' + "\n\n".join(lines) + "\n\n</div>"


def documents_table(data: dict) -> str:
    """Every document, with its number and what it covers."""
    rows = [f"| {d['title']} | {d['number']} | {d['covers']} |" for d in data["manuals"].values()]
    return ("| Document | Number | Covers |\n|---|---|---|\n" + "\n".join(rows) + "\n\n"
            f"A document marked with a firmware version describes that firmware release, here {data['docs_version']}; "
            "the version selector in the header switches between releases. The compatibility table says which "
            "firmware, Python library and hardware revisions work together.")


def component(group: str, key, data: dict) -> dict:
    """firmware, or software.KEY. Unknown names, and a component without a repository or a tag, stop the build."""
    if group == "firmware" and key is None:
        comp = data.get("firmware")
    elif group == "software" and key:
        comp = (data.get("software") or {}).get(key)
    else:
        comp = None
    name = group + (f".{key}" if key else "")
    if not comp or not comp.get("repository") or not comp.get("tag"):
        raise PluginError(f"versions.yml: no {name} with a repository and a tag for <!-- version-url/link/release: {name} -->")
    return comp


def version_url(kind: str, group: str, key, data: dict) -> str:
    """<!-- version-url: ... -->, <!-- version-link: ... --> and <!-- version-release: ... -->."""
    comp = component(group, key, data)
    repo = str(comp["repository"]).rstrip("/")
    if kind == "release":
        return f"{repo}/releases/tag/{comp['tag']}"
    url = f"{repo}/tree/{comp['tag']}"
    if kind == "url":
        return url
    tag = str(comp["tag"])
    text = str(comp.get("version") or (tag[1:] if re.fullmatch(r"[Vv]\d.*", tag) else tag))
    released = comp.get("released")
    date = f" ({released.isoformat()})" if isinstance(released, datetime.date) else ""
    return f"[{text}]({url}){date}"


def on_config(config):
    global _facts
    _facts = load(Path(config.config_file_path).parent / "versions.yml")
    config.extra["docs_version"] = _facts["docs_version"]
    return config


def on_page_markdown(markdown, page, config, files):
    markdown = META_RE.sub(lambda m: meta_block(m.group(1), _facts), markdown)
    markdown = URL_RE.sub(lambda m: version_url(m.group(1), m.group(2), m.group(3), _facts), markdown)
    return TABLE_RE.sub(lambda m: documents_table(_facts), markdown)
