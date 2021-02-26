# %%
# Given a list of dirs as strings, loop thr all of them
#

import os
import numpy as numpy
import helper_functions
import matplotlib.pyplot as plt
from imports.qtlab_data import *
from imports.dataclass import *
from imports.physics_models import *
from matplotlib.colors import to_rgba


os.chdir(r"G:\2021\AG_LG06_5_GNR_anthracene")

dir_exp = [
    "mol gnr_methoxy_dil1to100_tol",
    "mol gnr_methoxy_dil1to100_tol_checkSDuptob30",
    "mol gnr_methoxy_dil1to100_tol_gs_sd_goodev",
    "mol gnr_methoxy_dil1to100_tol_gs_sd_goodev",
    "mol gnr_methoxy_dil1to100_tol_gs_sd_goodev_2ndTest",
]

for f in range(len(dir_exp)):

    dset = QTLab_Dataset.find(pattern=match_pattern(dir_exp[f]))
    print(8 * "*", f"{(dir_exp[f]).upper()}", 8 * "*")
    exp_type = dset[dset["type"] == "IVsVg"]
    exp_folder = exp_type[exp_type["folder"] == dir_exp[f]]
    fig = Figure()
    current_list = []
    gatetraces = []
    if exp_folder:
        print(8 * "*", f"{('figure created').upper()}", 8 * "*")
        for dev in np.unique(dset["device"]):
            data_single_device = exp_folder[exp_folder["device"] == dev].load(
                Stability_Diagram
            )
            data_single_device = data_single_device[0]
            data_single_device.resample(256, 256)
            gatetraces.append(data_single_device.gate_trace(vs=0.1))
            current_mean = np.mean(np.abs(data_single_device["Isd"].values)) * 5
        fig.add_subplot(
            Subplot_IVsVg(
                data_single_device,
                title=f"Dev {dev} in\n {dir_exp[f][15:]}",
                crange=(-current_mean, current_mean),
                cmap="viridis",
            )
        )
        fig.add_subplot(Subplot_IVg(*gatetraces, legend=True))
        fig.visualise(f"figure_nb_test6/{dir_exp[f]}/{dev}.png")
        print(8 * "*", f"{('figure finished and saved').upper()}", 8 * "*")

# %%
import os
import numpy as numpy
import matplotlib.pyplot as plt
import string
from imports.qtlab_data import *
from imports.dataclass import *
from imports.physics_models import *
from matplotlib.colors import to_rgba

os.chdir(r"G:\2021\AG_LG06_6\mol gnr_dil1to100_1phenyloctane\AG_LG06_6_IVsVg\20210118")
dset = QTLab_Dataset.find()
dset = dset[dset["device"] == "j22"]
data = dset.load(Stability_Diagram)
device = dset["device"]
dat = data[0]
vsds = [0.1, 0.2, 0.3]
colors = ["red", "blue", "orange"]
gatetraces = []

for vsd, color in zip(vsds, colors):
    gatetrace = dat.gate_trace_derivative(vsd)
    gatetrace.ps(linewidth=1, color=color, marker=None, label=f"$V_sd$ = {1e3*vsd} mV")
    gatetraces.append(gatetrace)

cmap = "magma"
fig = Figure(aspect_ratio=1, dpi=150)
fig.add_subplot(Subplot_IVsVg(dat))
fig.add_subplot(Subplot_GVg(*gatetraces, legend=True))
fig.visualise()
