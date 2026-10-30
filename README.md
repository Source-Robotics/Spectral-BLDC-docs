# Spectral Micro documentation

The documentation of the Spectral Micro BLDC motor controller by [Source Robotics](https://source-robotics.com): the
manual (safety, technical data, mounting, setup, operation, firmware), the CAN and UART reference, and guides.

**Read it at [docs.source-robotics.com/Spectral-BLDC-docs](https://docs.source-robotics.com/Spectral-BLDC-docs/).**

The firmware and hardware files are in
[Source-Robotics/Spectral-Micro-BLDC-controller](https://github.com/Source-Robotics/Spectral-Micro-BLDC-controller).

## What is in this repository

| | |
|---|---|
| `docs/` | the pages: the manual chapters at the top level, `reference/`, `guides/`, `support/`, `appendix/` |
| `docs/includes/` | text shared by pages (glossary, symbols, abbreviations) and the data the reference pages are built from |
| `docs/includes/can_commands.yml`, `uart_commands.yml` | the hand-written descriptions of every CAN message and UART command |
| `docs/includes/generated/` | written by `tools/sync_firmware.py` from the firmware's release tag: `firmware_facts.json`, `firmware_release_notes.md`. Never edit |
| `versions.yml` | every version fact: the firmware release the site describes, the manual's number and revision |
| `compatibility.yml` | which firmware release works with which bootloader, Python library, PAR6 runtime and board |
| `hooks/` | `versions.py` writes the version facts into the pages; `firmware_pages.py` builds the reference pages; `llms.py` writes the Markdown twin of every page, `llms.txt` and `llms-full.txt` |
| `tools/` | `sync_firmware.py`, `test_tools.py`, `make_stubs.py`, `root_404.html` |
| `overrides/` | the theme changes: the older-version banner, the edit/report line, the header's repository card |

The site is built with [MkDocs](https://www.mkdocs.org/) and the
[Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) theme, in the same form as the
[PAR6 documentation](https://github.com/Source-Robotics/par6).

## Preview it locally

You need Python 3.11 or newer.

```bash
git clone https://github.com/Source-Robotics/Spectral-BLDC-docs.git
cd Spectral-BLDC-docs
python -m venv .venv
.venv/Scripts/pip install -r requirements.txt      # Linux and macOS: .venv/bin/pip
mkdocs serve
```

Open `http://127.0.0.1:8000/Spectral-BLDC-docs/`. The page reloads by itself when you save a file.

Every push and pull request runs `python tools/test_tools.py` and `mkdocs build --strict`, which fails on a broken
link or a missing page. Run both before you open a pull request.

## The reference is generated from the firmware

The command IDs, the frame lengths the firmware accepts, the responses it sends, the list of UART commands with
their kind, argument type, the mode they enter and what they print, and the defaults are read from the firmware's
source **at its release tag** by `tools/sync_firmware.py`, never from uncommitted work. The descriptions, units and
byte layouts are written by hand in `docs/includes/can_commands.yml` and `uart_commands.yml`. The build fails when
the two disagree: a command the firmware has and the descriptions lack, or the other way round, or a byte layout
that does not fit the frame.

```bash
python tools/sync_firmware.py            # write docs/includes/generated/ from firmware.tag in versions.yml
python tools/sync_firmware.py --check    # exit 1 if they are out of date
python tools/sync_firmware.py --print uart --tag v101   # look at another release's commands
```

The tool needs a clone of the firmware repository with its tags, next to this repository or named by
`--firmware PATH` / `FIRMWARE_DIR`, and the network for the release notes (`--no-network` keeps the file
that is there). The CI build does not run it; the generated files are committed.

## Markdown twins and the "Last update" dates

`hooks/llms.py` writes, at every build, a Markdown twin of every page next to its HTML (`…/index.md`), `llms.txt`
(an index of the twins by tab) and `llms-full.txt` (every page in one file), with the links absolute to the
published version (`extra.llms_base`). The "Copy this page as Markdown" button in the page header reads the twin.

The "Last update" date under every page comes from the `git-revision-date-localized` plugin (the page's last
commit; the CI checks out the whole history for it).

## Analytics and comments

The "Was this page helpful?" widget at the end of every page is configured under `extra.analytics.feedback`.
With `provider: google` (the Google Analytics property all the docs sites share, loaded only after the reader
accepts the cookie banner of `extra.consent`), Material's own integration records the page views and sends each
vote as an event named `feedback`.

Comments under every page come from Giscus, wired in `overrides/partials/comments.html` and configured under
`extra.comments`: all the docs sites share one Discussions home, the hub repository
`Source-Robotics/source-robotics.github.io`, with one thread per site and page. A page opts out with
`comments: false` in its front matter (the landing page does).

## Versions and releases

Each release of the Spectral firmware has its own version of the documentation, named after the release: `101`,
`107`, ... The version selector in the site's header switches between them, and a page of an older version says so
in a bar at the top. The versions are built with [mike](https://github.com/jimporter/mike) and kept in the
`gh-pages` branch; `latest` points at the newest.

**All version facts live in `versions.yml`, never in a page**: `docs_version` (the firmware release these pages
describe, which is also the name the version is published under), `firmware.tag` (`V` + `docs_version`), and the
manual's number, title, revision, status and publication date. `hooks/versions.py` writes them into the version
box on the landing page and into the list of documents on the About page; a malformed or missing fact stops the
build.

### When the firmware releases a new version

1. Set `docs_version` and `firmware.tag` in `versions.yml`; add a row to `compatibility.yml`.
2. Run `python tools/sync_firmware.py`. If the firmware added or removed a command, the build now fails until
   `can_commands.yml` / `uart_commands.yml` describe it: write the description.
3. Update the pages for what changed, using the release notes; give the manual a new revision letter in
   `versions.yml` and a line in its *Document history* on `docs/about.md`.
4. Commit and push to `main`. The site publishes the new version, `latest` moves to it, and the previous version
   stays as it was.

### Publishing

`.github/workflows/publish.yml` publishes on every push to `main`: the tests, a strict build, then `mike deploy`
for `docs_version` with the alias `latest`. In the repository's Settings, under Pages, the source must be "Deploy
from a branch", branch `gh-pages`, folder `/ (root)`. Never run `mkdocs gh-deploy` on this repository: it would
overwrite every version mike keeps there.

The root of `gh-pages` also carries `404.html` (source: `tools/root_404.html`). It forwards addresses from before
the versioning, such as `/Spectral-BLDC-docs/apage7_can/`, to the same page under `latest/`, where the `redirects` plugin in
`mkdocs.yml` maps the old page names to the new pages. To preview the published versions locally, with the version
selector, run `mike serve`.

## The site's address

The site is served at `https://docs.source-robotics.com/Spectral-BLDC-docs/`: the organisation's docs domain plus this
repository's name. Never rename this repository (its address would change and GitHub does not forward the old one),
and never add a `CNAME` file or a custom domain to it (that would take it out of the shared domain).

## License

- **Text and images:** [Creative Commons Attribution-ShareAlike 4.0](https://creativecommons.org/licenses/by-sa/4.0/),
  see [LICENSE](LICENSE). You may copy, adapt and share them, also commercially, if you credit Source Robotics and
  share your changes under the same license.
- **Code:** the [MIT license](LICENSE-CODE). This covers the code examples in the pages and the site's own code
  (hooks, tools, overrides, scripts), so you can use an example in your own program without other conditions.
- **Names and logos:** the Source Robotics name, the product names and the logos are not covered by either license.

By contributing you agree that your contribution is published under these licenses.

## Contributing

A small fix can be made from the browser: every page ends with a link to edit it on GitHub. For anything larger,
open an issue first, then a pull request. The *Contributing* page on the site has the house rules. Questions about
the driver itself go to the firmware repository's issue tracker.
