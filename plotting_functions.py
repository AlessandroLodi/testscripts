"""Compatibility wrappers for the historical plotting helper module."""

from __future__ import annotations

from transport_analysis.plotting import apply_plot_style, save_figure


def set_plotting_options() -> None:
    """Apply the project's Matplotlib style."""

    apply_plot_style()


def savefig(fig, fid, fmts=(".png",), dpi=300, border=False):
    """Save *fig* in each requested format.

    ``border`` is retained for API compatibility and adds a diagnostic red
    rectangle before saving when requested.
    """

    if border:
        import matplotlib.pyplot as plt

        bounds = plt.Rectangle(
            (0, 0), 1, 1, edgecolor="red", fill=False, transform=fig.transFigure
        )
        fig.add_artist(bounds)
    return save_figure(fig, fid, formats=fmts, dpi=dpi)


__all__ = ["savefig", "set_plotting_options"]
