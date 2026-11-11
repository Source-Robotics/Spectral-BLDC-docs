"""The figure of the page Encoder table and anti-cogging (docs/05-setup/anti-cogging.md), a light and a dark version.

    python tools/anticogging_figures.py      # writes docs/assets/anti-cogging/<name>.svg and <name>_dark.svg

Needs matplotlib and numpy, which the site build does not (they are not in requirements.txt): run it with a Python
that has them, after a change to the look, and commit the SVGs.

encoder_measurement is an illustration, not a measurement: how the drive gets from its two open-loop passes to the
encoder table (encal.cpp, the same in the STEPFOC and Spectral firmwares). Everything in it is made up for the
picture and defined below: an encoder error of a few slow harmonics, a friction lag that pulls each pass to its
side, and a fast ripple from the motor's own pull (at 6 and 12 per electrical turn of an 11-pole-pair motor, well
above 16 per turn). They go through the drive's steps: the mean per 1/128 of a turn, forward and back averaged,
the harmonics 1 to 16 per turn. No Spectral Micro measurement is plotted: none was kept as data (2026-11). The
STEPFOC manual's figures are from its own bench stepper and do not belong on this page.
"""
from __future__ import annotations

import math
from pathlib import Path

import matplotlib

matplotlib.use("svg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "assets" / "anti-cogging"

CPR = 16384          # encoder counts per shaft turn
TABLE_LEN = 128      # entries of the encoder table (encal.h ENCAL_TABLE_LEN)
HARMONICS = 16       # mechanical harmonics kept (constants.h ENCAL_HARMONICS)
GREEN = "#19c37d"
THEMES = {
    # dark text and axes on the light page, light ones on the dark (slate) page; each on its page's colour, so the
    # file also reads when it is opened on its own
    "light": {"suffix": "", "page": "#ffffff", "fg": "#292B37", "muted": "#5F6270", "grid": "#E1E2E6",
              "grey": "#8C8F9B", "faint": "#C4C6CD", "green": GREEN},
    "dark": {"suffix": "_dark", "page": "#1e2029", "fg": "#E4E4E4", "muted": "#B4B6BE", "grid": "#383B47",
             "grey": "#9EA1AC", "faint": "#5A5D69", "green": GREEN},
}
WIDTH = 8.0          # inches; the page scales the SVG to its text width

# made up for the picture, degrees of the shaft
ENCODER_ERROR = [(1, 0.26, 0.4), (2, 0.07, 1.3), (3, 0.03, 2.2), (5, 0.012, 0.7)]   # (per turn, amplitude, phase)
MOTOR_PULL = [(66, 0.035, 0.6), (132, 0.012, 1.9)]                                  # 6 and 12 x 11 pole pairs
FRICTION_LAG = 0.11

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Roboto", "Segoe UI", "Helvetica", "Arial", "DejaVu Sans"],
    "font.size": 11,
    "svg.fonttype": "none",      # text stays text: the reader's Roboto, or the next font in the list
    "svg.hashsalt": "anti-cogging",
    "axes.linewidth": 0.8,
    "lines.solid_capstyle": "round",
})


def waves(terms, shaft_rad):
    """The sum of amplitude sin(n t + phase) over the terms (n, amplitude, phase)."""
    return sum(amp * np.sin(n * shaft_rad + phase) for n, amp, phase in terms)


def harmonics_at(terms, angle_rad):
    """a cos(h t) + b sin(h t), summed over the terms (h, a, b)."""
    return sum(a * np.cos(h * angle_rad) + b * np.sin(h * angle_rad) for h, a, b in terms)


def fit_harmonics(values, centres_rad, hs):
    """The firmware's fit (encal.cpp en_fit): a = 2/N sum v cos(h t), b = 2/N sum v sin(h t) at the bin centres,
    the mean removed, each divided by the bin average's sinc."""
    n = len(values)
    v = np.asarray(values) - np.mean(values)
    out = []
    for h in hs:
        g = math.sin(math.pi * h / n) / (math.pi * h / n)
        a = 2.0 / n * np.sum(v * np.cos(h * centres_rad)) / g
        b = 2.0 / n * np.sum(v * np.sin(h * centres_rad)) / g
        out.append((h, a, b))
    return out


def style(ax, t, xlabel=None, ylabel=None):
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(t["muted"])
    ax.tick_params(colors=t["fg"], labelcolor=t["fg"], length=3, width=0.8)
    ax.grid(True, axis="y", color=t["grid"], linewidth=0.8)
    ax.set_axisbelow(True)
    ax.set_facecolor(t["page"])
    if xlabel:
        ax.set_xlabel(xlabel, color=t["fg"])
    if ylabel:
        ax.set_ylabel(ylabel, color=t["fg"])


def angle_axis(ax):
    ax.set_xlim(0, 360)
    ax.set_xticks(range(0, 361, 45))
    ax.set_xticklabels([f"{d}°" for d in range(0, 361, 45)])


def legend(ax, t, ncol, **kw):
    """Above the plot, left-aligned: it never covers a curve."""
    kw.setdefault("loc", "lower left")
    kw.setdefault("bbox_to_anchor", (0.0, 1.0))
    return ax.legend(frameon=False, labelcolor=t["fg"], handlelength=2.2, ncol=ncol, fontsize=10,
                     borderaxespad=0.2, columnspacing=1.6, **kw)


def save(fig, name, t):
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"{name}{t['suffix']}.svg"
    fig.savefig(path, format="svg", facecolor=t["page"], bbox_inches="tight", pad_inches=0.08,
                metadata={"Date": None, "Creator": None})
    plt.close(fig)
    # the page colour as a background rect, so the file reads when it is opened on its own (house rule)
    svg = path.read_text(encoding="utf-8")
    rect = f'<rect width="100%" height="100%" fill="{t["page"]}"/>'
    svg = svg.replace('<g id="figure_1">', rect + '\n <g id="figure_1">', 1)
    path.write_text(svg, encoding="utf-8", newline="\n")
    return path


# ---------- the figure ----------

def encoder_measurement(t):
    """Illustration: how the drive gets from two open-loop passes to the table."""
    fine = np.arange(0, CPR, 8)                                     # 2048 points per turn
    shaft = 2 * np.pi * fine / CPR
    error = waves(ENCODER_ERROR, shaft)
    pull = waves(MOTOR_PULL, shaft)
    fwd, bwd = error - FRICTION_LAG + pull, error + FRICTION_LAG + pull
    # the drive's steps: the mean per 1/128 of a turn, forward and back averaged, harmonics 1-16, mean removed
    bins = fine >> 7
    avg = np.array([(fwd[bins == b].mean() + bwd[bins == b].mean()) / 2 for b in range(TABLE_LEN)])
    centres = 2 * np.pi * (128 * np.arange(TABLE_LEN) + 64) / CPR
    terms = fit_harmonics(avg, centres, range(1, HARMONICS + 1))
    raw = 128 * np.arange(TABLE_LEN)
    table = harmonics_at(terms, 2 * np.pi * raw / CPR)

    fig, ax = plt.subplots(figsize=(WIDTH, 3.4))
    deg = fine * 360.0 / CPR
    ax.plot(deg, bwd, color=t["grey"], linewidth=0.7, label="backward pass")
    ax.plot(deg, fwd, color=t["grey"], linewidth=0.7, linestyle=(0, (4, 1.5)), label="forward pass")
    ax.plot(np.append(raw, CPR) * 360.0 / CPR, np.append(table, table[0]), color=t["green"], linewidth=2.2,
            label="the table: their average, harmonics 1 to 16")
    style(ax, t, "shaft angle", "error, degrees of the shaft")
    angle_axis(ax)
    ax.set_ylim(-0.56, 0.48)
    ax.text(0.995, 0.03, "ILLUSTRATION", transform=ax.transAxes, ha="right", va="bottom", color=t["muted"],
            fontsize=9.5, fontweight="bold")
    legend(ax, t, 3)
    return save(fig, "encoder_measurement", t)


def main():
    for t in THEMES.values():
        print(encoder_measurement(t).relative_to(ROOT).as_posix())


if __name__ == "__main__":
    main()
