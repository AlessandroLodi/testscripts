"""Compatibility layer for older notebooks.

New code should import from :mod:`transport_analysis`. The aliases in this
module keep existing research notebooks working while using the refactored,
tested implementations.
"""

from __future__ import annotations

import warnings
from pathlib import Path

import numpy as np

from transport_analysis.analysis import differentiate, fit_polynomial
from transport_analysis.datasets import build_filename_pattern
from transport_analysis.files import copy_files, rename_files
from transport_analysis.plotting import plot_trace


def match_pattern(*folders: str) -> str:
    """Return the QTLab filename pattern for one or more folders."""

    return build_filename_pattern(folders)


def pattern_matcher(eburn: str, mol: str) -> str:
    """Backward-compatible two-folder form of :func:`match_pattern`."""

    return match_pattern(eburn, mol)


def quick_plot(x, y, title: str | None = None, log_yaxis: bool = False):
    """Create and show a simple trace plot."""

    import matplotlib.pyplot as plt

    figure, axes = plot_trace(x, y, title=title, log_y=log_yaxis)
    plt.show()
    return figure, axes


def quick_plot_smooth(
    x,
    y,
    window_length: int,
    polyorder: int,
    title: str | None = None,
    log_yaxis: bool = False,
):
    """Smooth a trace with Savitzky-Golay filtering, then plot it."""

    from scipy.signal import savgol_filter

    smoothed = savgol_filter(y, window_length, polyorder)
    return quick_plot(x, smoothed, title=title, log_yaxis=log_yaxis)


def D(xlist, ylist):
    """Backward-compatible alias for :func:`differentiate`."""

    return differentiate(xlist, ylist)


def fit_subthreshold_secondOrder(x, y, smooth: bool = False):
    """Fit a quadratic to a trace and return a structured result."""

    return _fit_trace(x, y, degree=2, smooth=smooth)


def fit_ss_firstOrder(x, y, smooth: bool = False):
    """Fit a line to a trace and return a structured result."""

    return _fit_trace(x, y, degree=1, smooth=smooth)


def _fit_trace(x, y, *, degree: int, smooth: bool):
    values = np.asarray(y, dtype=float)
    if smooth:
        from scipy.signal import savgol_filter

        if values.size < 5:
            raise ValueError("at least five samples are required for smoothing")
        window = min(51, values.size if values.size % 2 else values.size - 1)
        values = savgol_filter(values, window, min(3, window - 1))
    return fit_polynomial(x, values, degree=degree)


def to_excel(x, y, title: str | None = None) -> Path:
    """Export two columns to CSV and return the output path.

    The historical function name is retained even though the output is CSV.
    """

    if not title:
        raise ValueError("title must provide an output filename")
    output_path = Path(title).with_suffix(".csv")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    np.savetxt(
        output_path,
        np.column_stack((x, y)),
        delimiter=",",
        header="Vg,Gsd",
        comments="",
        fmt="%.18e",
    )
    return output_path


def get_dataset(data_folder: str):
    """Find stability-diagram datasets and their device identifiers."""

    from imports.qtlab_data import QTLab_Dataset

    dataset = QTLab_Dataset.find(pattern=match_pattern(data_folder))
    stability_diagrams = dataset[dataset["type"] == "IVsVg"]
    selected = stability_diagrams[stability_diagrams["folder"] == data_folder]
    return selected, np.unique(selected["device"])


def copy_allFiles(path, dst):
    """Backward-compatible alias for :func:`copy_files`."""

    return copy_files(path, dst)


def rename_filenames(path, old_string, new_string):
    """Backward-compatible alias for :func:`rename_files`."""

    return rename_files(path, old_string, new_string)


def rename(path, old, new):
    """Backward-compatible recursive rename helper."""

    return rename_files(path, old, new, recursive=True)


def count_data_files(directory: str | Path) -> int:
    """Return the number of ``.dat`` files below *directory*."""

    path = Path(directory)
    if not path.is_dir():
        raise NotADirectoryError(path)
    return sum(1 for candidate in path.rglob("*.dat") if candidate.is_file())


def func(dirname):
    """Deprecated print-based wrapper around :func:`count_data_files`."""

    warnings.warn("func() is deprecated; use count_data_files()", DeprecationWarning)
    count = count_data_files(dirname)
    print(f"{dirname} has {count} .dat files")
    return count


__all__ = [
    "D",
    "copy_allFiles",
    "count_data_files",
    "fit_ss_firstOrder",
    "fit_subthreshold_secondOrder",
    "func",
    "get_dataset",
    "match_pattern",
    "pattern_matcher",
    "quick_plot",
    "quick_plot_smooth",
    "rename",
    "rename_filenames",
    "to_excel",
]
