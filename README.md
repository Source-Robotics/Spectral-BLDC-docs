# Spectral Micro documentation

The documentation of the Spectral Micro BLDC motor controller by [Source Robotics](https://source-robotics.com):
the datasheet, setup, flashing, calibration, tuning, the CAN and UART interfaces, and guides.

**Read it at [docs.source-robotics.com/Spectral-BLDC-docs](https://docs.source-robotics.com/Spectral-BLDC-docs/).**

The firmware and hardware files are in
[Source-Robotics/Spectral-Micro-BLDC-controller](https://github.com/Source-Robotics/Spectral-Micro-BLDC-controller).

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

Every push and pull request runs `mkdocs build --strict`, which fails on a broken link or a missing page, and
`python tools/test_tools.py`. Run both before you open a pull request.

## Versions and releases

Each release of the Spectral firmware has its own version of the documentation, named after the release: `101`,
`107`, ... The version selector in the site's header switches between them, and a page of an older version says so
in a bar at the top. The versions are built with [mike](https://github.com/jimporter/mike) and kept in the
`gh-pages` branch; `latest` points at the newest.

**All version facts live in `versions.yml`, never in a page.** It holds:

- `docs_version`: the firmware release these pages describe, which is also the name the version is published under
- `firmware.tag`: that release's tag in the firmware repository (`V` + `docs_version`)
- one entry per document: document number, title, revision, status, publication date, what it applies to

`hooks/versions.py` writes these into the manual's version box and into the list of documents. A malformed or
missing fact stops the build.

### When the firmware releases a new version

1. Set `docs_version` to the new release number and `firmware.tag` to its tag in `versions.yml`.
2. Update the pages for what changed, using the release's notes, and give the manual a new revision letter in
   `versions.yml` with a line in its *Document history*.
3. Commit and push to `main`. The site publishes the new version, `latest` moves to it, and the previous version
   stays as it was.

### Publishing

`.github/workflows/publish.yml` publishes on every push to `main`: a strict build, then `mike deploy` for
`docs_version` with the alias `latest`. In the repository's Settings, under Pages, the source must be "Deploy from a
branch", branch `gh-pages`, folder `/ (root)`. Never run `mkdocs gh-deploy` on this repository: it would overwrite
every version mike keeps there.

The root of `gh-pages` also carries `404.html` (source: `tools/root_404.html`). It forwards addresses from before the
versioning, such as `/Spectral-BLDC-docs/apage7_can/`, to the same page under `latest/`, so old links keep working.

To preview the published versions locally, with the version selector, run `mike serve`.

## The site's address

The site is served at `https://docs.source-robotics.com/Spectral-BLDC-docs/`: the organisation's docs domain plus this
repository's name. Never rename this repository (its address would change and GitHub does not forward the old one),
and never add a `CNAME` file or a custom domain to it (that would take it out of the shared domain).

## Contributing

A small fix can be made from the browser: every page has a link to edit it on GitHub. For anything larger, open an
issue first, then a pull request. Questions about the driver itself go to the firmware repository's issue tracker.
