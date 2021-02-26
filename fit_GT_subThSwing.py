#%%
import os
import numpy as np
import matplotlib.pyplot as plt
import string
from imports.qtlab_data import *
from imports.dataclass import *
from imports.physics_models import *
from matplotlib.colors import to_rgba
import math

# Instead of navigating the submodule np.polynomial.polynomial.Polynomial
# I'm benefitting from the convenience class numpy.polynomial
Polynomial = np.polynomial.Polynomial

"""
Create images of SD and GTs taken at different biases as specified.
The path needs to point to the dir where the data are and not a parent dir.
parmas: 
    path -> string

returns:
    .png file
"""

os.chdir(r"G:\2021\AG_LG06_6\mol gnr_dil1to100_1phenyloctane\AG_LG06_6_IVsVg\20210118")
output_dir = "test"
with open(f"output_{output_dir}.csv", "w") as f:
    f.write("\t".join(["dev", "Vg", "Isd", "slope"]) + "\n")

dset = QTLab_Dataset.find()
dset = dset[dset["device"] == "j22"]
data = dset.load(Stability_Diagram)
vsds = [x for x in np.around(np.linspace(0.1, 0.5, 5), decimals=2)]
colors = np.linspace(0.1, 0.5, num=5)

#%%
for i in range(len(data)):
    gatetraces = []
    list_const = []
    list_slope = []
    list_second = []
    fig = Figure(aspect_ratio=1, dpi=150)

    for vsd, color in zip(vsds, colors):
        trace = data[i].gatetrace(vsd)
        trace.ps(
            linewidth=1,
            marker=None,
            label=f"$V_b$ = {1e3*vsd} mV",
            color=plt.cm.viridis(color),
        )
        y_min = np.min(trace["Isd"].values)
        vg_points = trace["Vg"].values
        isd_pts = trace["Isd"].values * 1e6
        isd_pts_derivative = 
        isd_min, isd_max = (
            np.min(isd_pts[: np.argmin(isd_pts)]),
            np.max(isd_pts[: np.argmin(isd_pts)]),
        )
        print(
            f'Minimum Isd at index = {np.argmin(trace["Isd"].values)} w/ value = {isd_min}'
        )

        x_new = np.linspace(
            vg_points[10],
            vg_points[np.argmin(trace["Isd"].values)],
            num=len(vg_points),
        )

        pfit, stats = Polynomial.fit(
            vg_points[30 : np.argmin(trace["Isd"].values)],
            isd_pts[30 : np.argmin(trace["Isd"].values)],
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
        rms = np.sqrt(resid[0] / len(isd_pts[: np.argmin(trace["Isd"].values)]))
        print(
            f"Fit: const = {const:.3f}; slope = {slope:.3f}; second = {second:.3f}; rms residual = {rms:.4f})"
        )
        print(8 * "*")

        list_const.append(const)
        list_slope.append(slope)
        list_second.append(second)
        fig1 = plt.figure()
        ax1 = fig1.add_subplot(111)
        ax1.scatter(vg_points, isd_pts)
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
        # plt.show()
        plt.savefig(f"Subthreshold_swing_gt@{vsd}.png")
        gatetraces.append(trace)
    fig.add_subplot(
        Subplot_IVsVg(data[i], title=f"{dset[i]['device']}", cmap="viridis")
    )
    fig.add_subplot(Subplot_IVg(*gatetraces, legend=True, title=f"{dset[i]['device']}"))
    fig.visualise(
        f"figure_plot_SD_and_GT_100_500mV_100mVstep_test/{dset[i]['device']}_{i}.png"
    )

# %%
fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.scatter(gt['Vg'][:], gt['Isd'][:])
ax1.plot(gt['Vg'][:], sub_th, color="orange")
ax1.set_yscale("log")
plt.title("Subthreshold Swing")
plt.show()
# %%
