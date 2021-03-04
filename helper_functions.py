# Helper Functions

import os
import glob
import shutil
import numpy as np
from imports.qtlab_data import *
from imports.dataclass import *
from imports.physics_models import *


def match_pattern(*args) -> str:
    """
    Given a list of string it will return the dir pattern.
    Take a look at what the regex does in dedicated website
    """
    m = "|".join(args)
    pattern = ".*?(?P<folder>{}).*?\d+_(?P<exp>[a-zA-Z0-9_]+)_(?P<type>[a-zA-Z0-9\-_]+?)_(?P<device>[a-zA-Z]+[0-9]+)\.(?:dat|csv|txt)".format(
        m
    )
    return pattern


def quick_plot(x, y, title: str = None, log_yaxis: bool = None):
    """
    Very simple plot. Handy use
    """
    import matplotlib.pyplot as plt

    fig = plt.figure()
    ax = fig.add_subplot()
    ax.scatter(x, y)
    if log_yaxis:
        ax.set_yscale("log")
    plt.title(title)
    plt.show()


def quick_plot_smooth(
    x, y, window_length: int, polyorder: int, title: str = None, log_yaxis: bool = None
):
    """
    Quick Simple Plot. y axis smoothed according to savgol_filter algo.

    window_length = 51, polyorder = 3 works most of the time just fine
    """
    from scipy.signal import savgol_filter

    y_smooth = savgol_filter(y, window_length, polyorder)
    fig = plt.figure()
    ax = fig.add_subplot()
    ax.scatter(x, y_smooth)
    if log_yaxis:
        ax.set_yscale("log")
    plt.title(title)
    plt.show()


def D(xlist, ylist):
    """
    Calculate the derivative of a function from first difference
    Ex: vg_deriv, isd_deriv = D(vg_one, isd_one)
    """
    import numpy as np

    yprime = np.diff(ylist) / np.diff(xlist)
    xprime = []
    for i in range(len(yprime)):
        xtemp = (xlist[i + 1] - xlist[i]) / 2
        xprime = np.append(xprime, xtemp)
    return xprime, yprime


def fit_subthreshold_secondOrder(x, y, smooth: bool = None):

    """
    Perform a polynomial fit on the y trace.
    y-axis is first smoothed and then fed inside the algorithm
    """
    from scipy.signal import savgol_filter
    import numpy as np

    Polynomial = np.polynomial.Polynomial

    if smooth:
        y_smooth = savgol_filter(y, 51, 3)

    y_min = np.min(y_smooth)
    vg_points = x
    y_pts = y_smooth * 10 ** np.floor(np.abs(np.log10(i)))
    isd_min, isd_max = (
        np.min(y_pts[: np.argmin(y_pts)]),
        np.max(y_pts[: np.argmin(y_pts)]),
    )
    print(f"Minimum of y at index = {np.argmin(y_min)} w/ value = {isd_min}")

    x_new = np.linspace(
        vg_points[10], vg_points[np.argmin(y_smooth)], num=len(vg_points),
    )

    pfit, stats = Polynomial.fit(
        vg_points[10 : np.argmin(y_smooth)],
        y_pts[10 : np.argmin(y_smooth)],
        2,
        full=True,
        # window=(np.log(isd_min), np.log(isd_max)),
        # domain=(np.log(isd_min), np.log(isd_max))
        window=(isd_min, isd_max),
        domain=(isd_min, isd_max),
    )
    print(8 * "*")
    print("Raw fit results:", pfit, stats, sep="\n")
    const, slope, second = pfit
    resid, rank, sing_val, rcond = stats
    rms = np.sqrt(resid[0] / len(y_pts[: np.argmin(y_smooth)]))
    print(
        f"Fit: const = {const:.3f}; slope = {slope:.3f}; second = {second:.3f}; rms residual = {rms:.4f})"
    )
    print(8 * "*")
    fig1 = plt.figure()
    ax1 = fig1.add_subplot()
    ax1.scatter(vg_points, y_pts)
    ax1.plot(x_new, pfit(x_new), color="orange")
    ax1.set_yscale("log")
    plt.title("Subthreshold Swing")
    plt.text(
        0.35,
        0.8,
        f"Fit Model: c + a0*x + a1*x^2.\n c = {const:.3f}; a0 = {slope:.2f}; a1 = {second:.3f};\n rms residual = {rms:.4f}",
        {"color": "k", "fontsize": 12},
        horizontalalignment="left",
        verticalalignment="top",
        transform=fig1.transFigure,
    )


def fit_ss_firstOrder(x, y, smooth: bool = None):

    """
    Perform a polynomial fit on the y trace.
    y-axis is first smoothed and then fed inside the algorithm
    """
    from scipy.signal import savgol_filter
    import numpy as np

    Polynomial = np.polynomial.Polynomial

    if smooth:
        y_smooth = savgol_filter(y, 51, 3)

    y_min = np.min(y_smooth)
    vg_points = x
    y_pts = y_smooth * 10 ** np.floor(np.abs(np.log10(i)))
    isd_min, isd_max = (
        np.min(y_pts[: np.argmin(y_pts)]),
        np.max(y_pts[: np.argmin(y_pts)]),
    )
    print(f"Minimum of y at index = {np.argmin(y_min)} w/ value = {isd_min}")

    x_new = np.linspace(
        vg_points[10], vg_points[np.argmin(y_smooth)], num=len(vg_points),
    )

    pfit, stats = Polynomial.fit(
        vg_points[40 : np.argmin(y_smooth)],
        y_pts[40 : np.argmin(y_smooth)],
        1,
        full=True,
        # window=(np.log(isd_min), np.log(isd_max)),
        # domain=(np.log(isd_min), np.log(isd_max))
        window=(isd_min, isd_max),
        domain=(isd_min, isd_max),
    )
    print(8 * "*")
    print("Raw fit results:", pfit, stats, sep="\n")
    const, slope = pfit
    resid, rank, sing_val, rcond = stats
    rms = np.sqrt(resid[0] / len(y_pts[: np.argmin(y_smooth)]))
    print(f"Fit: const = {const:.3f}; slope = {slope:.3f}; rms residual = {rms:.4f})")
    print(8 * "*")
    fig1 = plt.figure()
    ax1 = fig1.add_subplot()
    ax1.scatter(vg_points, y_pts)
    ax1.plot(x_new, pfit(x_new), color="orange")
    ax1.set_yscale("log")
    plt.title("Subthreshold Swing")
    plt.text(
        0.35,
        0.8,
        f"Fit Model: c + a0*x \n c = {const:.3f}; a0 = {slope:.2f}; \n rms residual = {rms:.4f}",
        {"color": "k", "fontsize": 12},
        horizontalalignment="left",
        verticalalignment="top",
        transform=fig1.transFigure,
    )


def to_excel(x, y, title: str = None):
    """
    Create a table with just two columns 
    Ex: to_excel(vg, gsd)
    """
    import numpy as np

    a = np.asarray([x, y])
    np.savetxt(
        title + ".csv", a.T, delimiter=",", header="Vg, Gsd", comments="", fmt="%.18f",
    )


def pattern_matcher(eburn: str, mol: str):
    return f".*?(?P<folder>{eburn}|{mol}).*?\d+_(?P<exp>[a-zA-Z0-9_]+)_(?P<type>[a-zA-Z0-9\-_]+?)_(?P<device>[a-zA-Z]+[0-9]+)\.(?:dat|csv|txt)"


def get_dataset(data_folder: str):
    pattern = f".*?(?P<folder>{data_folder}).*?\d+_(?P<exp>[a-zA-Z0-9_]+)_(?P<type>[a-zA-Z0-9\-_]+?)_(?P<device>[a-zA-Z]+[0-9]+)\.(?:dat|csv|txt)"
    dset = QTLab_Dataset.find(pattern=pattern)
    ivsvgset = dset[dset["type"] == "IVsVg"]
    data_folder = ivsvgset[ivsvgset["folder"] == data_folder]
    devices_list = np.unique(data_folder["device"])
    return data_folder, devices_list


def func(dirname):
    if os.path.exists(os.path.join(dirname, ".dat")):
        c = 0
        for roots, dir, files in os.walk(dirname):
            c += len([f for f in files if f.endswith(".dat")])
        print(f"{dirname} has {c} number of dat")


# func('E:\\AG_LG06_4_GNR_anthracene\\')


def func2(dirname, test):
    for root, dirs, files in os.walk(dirname):
        d = [f for f in files if f.endswith(".dat") and f]
        if d and d is not None:
            # this just replace the string but doesnt actually change the filename
            a = (", ".join(str(i) for i in d)).replace(
                "GNR_anthracene", "GNR-2_anthracene"
            )
            print(a)
            # print(f'length of a: {len(a)} and length of d: {len(d)}')
            # shutil.copy(a, test)


def copy_allFiles(path, dst):
    if not os.path.exists(dst):
        os.makedirs(dst)
    for root, dirs, files in os.walk(path):
        for f in files:
            path_file = os.path.join(root, f)
            shutil.copy2(path_file, dst)


def rename(path, old, new):
    # os.chdir(path)
    for t in os.walk(path):
        # os.walk returns a tuple so i walk thr the tuple to get the individual lists
        for l in t:
            # the first two things are garbage so remove them
            str1 = ",".join(l[2:])
            os.rename(
                os.path.join(path, str1), os.path.join(path, str1.replace(old, new))
            )


def rename_filenames(path, old_string, new_string):
    os.chdir(path)
    for f in os.listdir(path):
        if old_string in f:
            os.rename(
                os.path.join(path, f),
                os.path.join(path, f.replace(old_string, new_string)),
            )


def replace_noInPlace(path, dst):
    if not os.path.exists(dst):
        os.makedirs(dst)
    os.chdir(path)
    for roots, dir, files in os.walk(path):
        for f in files:
            f.replace("GNR_anthracene", "GNR-2_anthracene")


def grab_just_SD(path):
    for roots, dirs, files in os.walk(path):
        for f in files:
            if f.endswith("dat") and "IVsVg" in f:
                QTLab_Dataset.find().load(Stability_Diagram)


def data_folder(path):
    for dirs in os.walk(path):
        if "burn" or "mol" in dirs:
            print(dirs)
