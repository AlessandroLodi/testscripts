# %%
import os
import numpy as numpy
import matplotlib.pyplot as plt
import string
from imports.qtlab_data import *
from imports.dataclass import *
from imports.physics_models import *
from matplotlib.colors import to_rgba

folder_IVg = "mol gnr_methoxy_dil1to100_tol_gs_sd_goodev_2ndTest"
chipPiece = "AG_LG06_5_GNR_anthracene"
match = "{}".format(folder_IVg)
pattern = ".*?(?P<folder>{}).*?\d+_(?P<exp>[a-zA-Z0-9_]+)_(?P<type>[a-zA-Z0-9\-_]+?)_(?P<device>[a-zA-Z]+[0-9]+)\.(?:dat|csv|txt)".format(
    match
)
os.chdir(r"G:\2021\AG_LG06_5_GNR_anthracene")
dset = QTLab_Dataset.find(pattern=pattern)
dset = dset[np.argsort(dset["timestamp"])[::-1]]
# dset[dset["type"] == "IVsVg"]
# data = dset.load(Stability_Diagram)
# data1 = dset.load(QTLab_Data)
# data2 = dset.load(QTLab_Data)


#%%


#%%
for i in range(len(data)):
    fig = Figure()
    fig.add_subplot(Subplot_IVg(data[i], title=f"device pure {dset['device'][i]}_{i}"))
    fig.add_subplot(Subplot_IVg(data1[i].cycle_to_trace(cyclic_axis="Isd", method="average"),title=f"device cycle_to_trace {dset['device'][i]}_{i}"))
    fig.add_subplot(Subplot_IVg(data2[i].average_cycles(),title=f"device average_cycles {dset['device'][i]}_{i}"))
    fig.visualise(f"Figure/{folder_IVg}/method_comparison/{dset['device'][i]}_{i}.png")
# %%

import os
import numpy as numpy
import matplotlib.pyplot as plt
import string
from imports.qtlab_data import *
from imports.dataclass import *
from imports.physics_models import *
from matplotlib.colors import to_rgba
import helper_functions 

os.chdir(r"G:\2021\AG_LG06_5_GNR_anthracene")


dir_exp = [
    "mol gnr_methoxy_dil1to100_tol",
    "mol gnr_methoxy_dil1to100_tol_checkSDuptob30",
    "mol gnr_methoxy_dil1to100_tol_gs_sd_goodev",
    "mol gnr_methoxy_dil1to100_tol_gs_sd_goodev",
    "mol gnr_methoxy_dil1to100_tol_gs_sd_goodev_2ndTest",
]
for f in range(len(dir_exp[1])):

    dset = QTLab_Dataset.find(pattern=match_pattern(dir_exp[f]))
    print("##################")
    print("New Dataset Loaded")
    print("\n")
    exp_type = dset[dset["type"] == "IVsVg"]
    exp_folder = exp_type[exp_type["folder"] == dir_exp[f]]
    fig = Figure()
    current_list = []
    gatetraces = []
    if exp_folder:
        print("##################")
        print("Figure CREATED  ya")
        print("\n")
        for dev in np.unique(dset["device"]):
            data_single_device = exp_folder[exp_folder["device"] == dev].load(Stability_Diagram)
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
        print("\n")
        print("Figure Finished ya")
        print("##################")


# %%

# %%

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
print(dset)
data = dset[0].load(Stability_Diagram)
device = dset["device"]
dat = data[0]
vsds = [0.1, 0.2, 0.3]
colors = ["red", "blue", "orange"]
gatetraces = []

for vsd, color in zip(vsds, colors):
    gatetraces = dat.gate_trace(vsd)
    gatetrace.ps(linewidth=1, color=color, marker=None, label=f"$V_sd$ = {1e3*vsd} mV")
    gatetraces.append(gatetrace)

cmap = "magma"
fig = Figure(aspect_ratio=1, dpi=150)
fig.add_subplot(Subplot_IVsVg(dat))
fig.add_subplot(Subplot_IVg(*gatetraces, legend=True))
fig.visualise()
# %%
