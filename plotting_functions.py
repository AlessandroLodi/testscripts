import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import os
from os import path
from cycler import cycler
from matplotlib.ticker import (
    MultipleLocator,
    FixedLocator,
    FixedFormatter,
    FormatStrFormatter,
    FuncFormatter,
    AutoMinorLocator,
)


def set_plotting_options():
    colors = (
        np.array(
            [
                [0, 115, 179],
                [230, 160, 37],
                [204, 121, 167],
                [79, 111, 52],
                [223, 197, 153],
                [153, 179, 223],
            ]
        )
        / 255
    )
    """ Set matplotlib plotting settings """
    colmap = "plasma"
    facecol = "#d88f8f"

    # plt.rcParams["text.usetex"] = True
    # plt.rcParams["text.latex.preamble"] = [
    #     r"\newcommand{\sym}[1]{\textit{#1}}",
    #     r"\newcommand{\dIdV}{d\textit{I}/d\textit{V} (2e\textsuperscript{2}/h)}",
    #     r"\newcommand{\sub}[1]{\textsubscript{#1}}",
    # ]
    # I changed to plt, before was mpl.rcParams
    mpl.rcParams["font.family"] = "sans-serif"
    mpl.rcParams["font.sans-serif"] = ["Computer Modern Roman"]
    mpl.rcParams["axes.titlesize"] = 10
    mpl.rcParams["axes.labelsize"] = 10
    mpl.rcParams["xtick.labelsize"] = 10
    mpl.rcParams["ytick.labelsize"] = 10
    mpl.rcParams["legend.fontsize"] = 10
    mpl.rcParams["font.size"] = 14
    mpl.rcParams["figure.figsize"] = [
        15.220700152207002, 9.406910026634625]  # golden ratio
    mpl.rcParams["figure.dpi"] = 180
    mpl.rcParams["ytick.major.size"] = 2.835
    mpl.rcParams["ytick.major.width"] = 0.5
    mpl.rcParams["ytick.minor.size"] = 2.835 * 0.5
    mpl.rcParams["ytick.minor.width"] = 0.5
    mpl.rcParams["ytick.direction"] = "out"
    mpl.rcParams["xtick.major.size"] = 2.835
    mpl.rcParams["xtick.major.width"] = 0.5
    mpl.rcParams["xtick.direction"] = "out"
    mpl.rcParams["xtick.minor.size"] = 2.835 * 0.5
    mpl.rcParams["xtick.minor.width"] = 0.5
    mpl.rcParams["savefig.bbox"] = None
    mpl.rcParams["savefig.pad_inches"] = 0.0
    mpl.rcParams["figure.subplot.left"] = 0.15
    mpl.rcParams["figure.subplot.right"] = 0.9
    mpl.rcParams["figure.subplot.top"] = 0.9  # 0.98
    mpl.rcParams["figure.subplot.bottom"] = 0.15
    mpl.rcParams["axes.linewidth"] = 0.5
    mpl.rcParams["legend.fontsize"] = 7
    mpl.rcParams["legend.loc"] = "upper right"
    mpl.rcParams["lines.markersize"] = 3
    mpl.rcParams["lines.linewidth"] = 1
    mpl.rcParams["pdf.fonttype"] = 42  # Exports text as font not as vector
    colors = [tuple(c) for c in colors]
    plt.rc("axes", prop_cycle=(cycler("color", colors)))



def savefig(fig, fid, fmts=[".png"], dpi=300, border=False):
    """Save figure in mulitple formats.
    Currently this version does not support multiple path generation such as figures/paper/fig1,
    but it only accepts one folder only under the current working directory.

    Args:
        fig ([plt.subplots object]): matplotlib figure
        fid ([str]): string with the path and the filename, e.g. figures/fig1
        fmts (list, optional): list of the file formats. Defaults to [".png"].
        dpi (int, optional): figure resolution. Defaults to 300.
        border (bool, optional): draw a rectangle around the figure. Defaults to False.
    """
    for ax in fig.get_axes():
        ax.set_rasterization_zorder(1)

    dir_name = os.path.dirname(fid)
    if not os.path.exists(dir_name):
        try:
            os.makedirs(dir_name)
        except:
            print(f'Not able to create path {dir_name}')
    for fmt in fmts:
        fig.savefig(fid + fmt, dpi=dpi)
    if border:
        bounds = plt.Rectangle((0, 0), 1, 1, ec="r",
                               fill=False, transform=fig.transFigure)
        fig.add_artist(bounds)


def main():
    import matplotlib.pyplot as plt
    import numpy as np
    x = np.linspace(0, 300, num=300)
    exponent = .75
    def y(x): return 1e-12*x ** exponent
    fig, ax = plt.subplots()
    ax.scatter(x, y(x), color='orange', marker='+',
               label=f'power law with exponent {exponent}')
    ax.legend(numpoints=1, loc='upper left', fontsize=9)
    fid = 'test_figure_vscode/try/new_path/power_plot'
    savefig(fig, fid, fmts=['.png', '.pdf'], border=True)


if __name__ == '__main__':
    main()
