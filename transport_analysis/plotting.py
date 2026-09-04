"""Minimal plotting helpers with no import-time configuration side effects."""

from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
from cycler import cycler
from matplotlib.figure import Figure
from numpy.typing import ArrayLike


COLOR_CYCLE = (
    "#0073B3",
    "#E6A025",
    "#CC79A7",
    "#4F6F34",
    "#DFC599",
    "#99B3DF",
)


def apply_plot_style() -> None:
    """Apply the project's publication-oriented Matplotlib defaults."""

    mpl.rcParams.update(
        {
            "axes.labelsize": 10,
            "axes.linewidth": 0.5,
            "axes.prop_cycle": cycler(color=COLOR_CYCLE),
            "axes.titlesize": 10,
            "figure.dpi": 180,
            "figure.figsize": (9.4, 5.8),
            "font.family": "sans-serif",
            "font.size": 10,
            "legend.fontsize": 8,
            "lines.linewidth": 1,
            "pdf.fonttype": 42,
            "xtick.direction": "out",
            "ytick.direction": "out",
        }
    )


def plot_trace(
    x: ArrayLike,
    y: ArrayLike,
    *,
    title: str | None = None,
    log_y: bool = False,
):
    """Create a simple trace plot and return ``(figure, axes)``."""

    figure, axes = plt.subplots()
    axes.plot(x, y)
    axes.set_yscale("log" if log_y else "linear")
    if title:
        axes.set_title(title)
    return figure, axes


def save_figure(
    figure: Figure,
    destination: str | Path,
    *,
    formats: Iterable[str] = ("png",),
    dpi: int = 300,
) -> list[Path]:
    """Save a figure in one or more formats and return the created paths."""

    base_path = Path(destination).expanduser()
    base_path.parent.mkdir(parents=True, exist_ok=True)

    output_paths: list[Path] = []
    for output_format in formats:
        suffix = output_format.removeprefix(".").lower()
        if not suffix or not suffix.isalnum():
            raise ValueError(f"invalid figure format: {output_format!r}")
        output_path = base_path.with_suffix(f".{suffix}")
        figure.savefig(output_path, dpi=dpi, bbox_inches="tight")
        output_paths.append(output_path)
    return output_paths
