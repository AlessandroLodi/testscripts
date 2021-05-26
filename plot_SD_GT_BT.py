#%%
import os
import numpy as numpy
import matplotlib.pyplot as plt
import string
from imports.qtlab_data import *
from imports.dataclass import *
from imports.physics_models import *
from matplotlib.colors import to_rgba

"""
Create images of SD and GTs taken at different biases as specified.
The path needs to point to the dir where the data are and not a parent dir.
parmas: 
    path -> string

returns:
    .png file
"""

os.chdir(r"I:\2019\alessandrofet\stabdiag_GNR_1\GNR2_1\stabdiag_GNR_1_IVsVg")
dset = QTLab_Dataset.find()
data = dset.load(Stability_Diagram)
vg_max = 0.01
vsd_max = 0.39
vgds = [x for x in np.around(np.linspace(0, vg_max, 1), decimals=2)]
vsds = [x for x in np.around(np.linspace(0, vsd_max, 1), decimals=2)]
colors_vg = np.linspace(0.1, vg_max, num=len(vgds))
colors_vsd = np.linspace(0.1, vsd_max, num=len(vsds))
biastrace_dict = {}
gatetrace_dict = {}
gatetrace_lst = []
biastrace_lst = []

for i in range(len(data[:2])):
    biastraces = []
    gatetraces = []
    for vg, color_vg, vsd, color_vsd in zip(vgds, colors_vg, vsds, colors_vsd):
        biastrace = data[i].bias_trace(vg)
        print(f"gate voltage = {vg}, bias voltage = {vsd}")
        biastrace.ps(
            linewidth=1,
            marker=None,
            label=f"$V_g$ = {vg} V",
            prop={"size": 4},
            color=plt.cm.viridis(color_vg),
        )
        biastraces.append(biastrace)
        biastrace_lst.append(biastrace)
        gatetrace = data[i].gatetrace(vsd)
        gatetrace.ps(
            linewidth=1,
            marker=None,
            label=f"$V_b$ = {vsd} mV",
            prop={"size": 4},
            color=plt.cm.magma(color_vsd),
        )
        gatetraces.append(gatetrace)
        gatetrace_lst.append(gatetrace)
    gatetrace_dict.update({f"Vg_device_{dset['device'][i]}": gatetrace_lst[i]["Vg"][:]})
    biastrace_dict.update(
        {f"Vsd_device_{dset['device'][i]}": biastrace_lst[i]["Vsd"][:]}
    )
    fig = Figure(aspect_ratio=1, dpi=150)
    fig.add_subplot(
        Subplot_IVsVg(data[i], title=f"{dset[i]['device']}", cmap="viridis")
    )
    fig.add_subplot(Subplot_IV(*biastraces, legend=True, title=f"{dset[i]['device']}"))
    fig.add_subplot(Subplot_IVg(*gatetraces, legend=True, title=f"{dset[i]['device']}"))
    fig.visualise(f"figure_plot_SD_BT-GT_test/{dset[i]['device']}_{i}.svg")

gt_df = pd.DataFrame(gatetrace_dict)
bs_df = pd.DataFrame(biastrace_dict)
gt_df.to_csv(path_or_buf="gatetrace_test.csv", sep=",", index=False)
bs_df.to_csv(path_or_buf="biastrace_test.csv", sep=",", index=False)
# %%

for i in range(len(data[:25])):
    fig = Figure(size=1.1, dpi=150)
    data[i].resample(256, 256)
    fig.add_subplot(Subplot_IVsVg(data[i], cmap="viridis", yrange=(-0.2, 0.2),))
    fig.visualise(f"figure_justSD_svg/sd_device_{dset[i]['device']}.svg")


# %%
