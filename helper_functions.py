# Helper Functions


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
