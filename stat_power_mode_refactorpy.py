# Two-sided inverse Students t-distribution
# p - probability, df - degrees of freedom
# %%
import re
from scipy.stats import linregress
import scipy.stats as stats
import numpy as np
from numpy.random import normal, binomial
import matplotlib.pyplot as plt


def tinv(p, df): return abs(t.ppf(p/2, df))


def plot_ci_manual(t, s_err, n, x, x2, y2, ax=None):
    if ax is None:
        ax = plt.gca()

    ci = t * s_err * np.sqrt(1/n + (x2 - np.mean(x)) **
                             2 / np.sum((x - np.mean(x))**2))
    ax.fill_between(x2, y2 + ci, y2 - ci, color="#b9cfe7", edgecolor="")

    return ax


def plot_ci_bootstrap(xs, ys, resid, nboot=500, ax=None):

    if ax is None:
        ax = plt.gca()

    for _ in range(nboot):
        resamp_resid = resid[np.random.randint(0, len(resid) - 1, len(resid))]
        # Make coeffs of for polys
        pc = np.polyfit(xs, ys + resamp_resid, 1)
        # Plot bootstrap cluster
        ax.plot(xs, np.polyval(pc, xs), "b-",
                linewidth=2, alpha=3.0 / float(nboot))

    return ax


def fit_linear_reg(x_data, y_data):
    return linregress(x_data, y_data)


def compute_stats(ax, N=40):
    x_data, y_data = generate_linear_data(N)
    lin_model_result = fit_linear_reg(x_data, y_data)
    def y_model(x_data): return lin_model_result.intercept + \
        x_data * lin_model_result.slope
    resid = y_data - y_model(x_data)
    chi2 = np.sum((y_data - y_model(x_data))**2)
    dof = x_data.size - 2  # only two parameter for a linear regression
    t = stats.t.ppf(0.975, dof)
    chi2_red = chi2 / dof
    s_err = np.sqrt(np.sum(resid**2) / dof)

    ax.plot(
        x_data, y_data, "o", color="#b9cfe7", markersize=8,
        markeredgewidth=1, markeredgecolor="b", markerfacecolor="None"
    )

    # Fit
    ax.plot(x_data, y_model(x_data), "-", color="0.1",
            linewidth=1.5, alpha=0.5, label="Fit")

    x2 = np.linspace(np.min(x_data), np.max(x_data), 100)
    y2 = y_model(x2)

    # Confidence Interval (select one)
    #plot_ci_manual(t, s_err, N, x_data, x2, y2, ax=ax)
    plot_ci_bootstrap(x_data, y_data, resid, ax=ax)

    # Prediction Interval
    pi = t * s_err * np.sqrt(1 + 1/N + (x2 - np.mean(x_data))
                             ** 2 / np.sum((x_data - np.mean(x_data))**2))
    ax.fill_between(x2, y2 + pi, y2 - pi, color="None", linestyle="--")
    ax.plot(x2, y2 - pi, "--", color="0.5", label="95% Prediction Limits")
    ax.plot(x2, y2 + pi, "--", color="0.5")

    plt.show()


def generate_linear_data(N):
    x = np.linspace(1, 100, num=N)
    gauss_noise1 = normal(0, 5, size=(N))  # gauss_noise1 ~ N(0, 5)
    gauss_noise2 = normal(1, 1, size=(N))    # gauss_noise2 ~ N(1, 1)
    binom_noise = binomial(4, 0.5, size=(N))  # binom_noise ~ B(2, .05)
    def y(x): return (x * .5 + gauss_noise1 +
                      gauss_noise2 * binom_noise)
    return x, y(x)


def main():
    compute_stats(100)


if __name__ == '__main__':
    main()
