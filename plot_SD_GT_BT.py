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

os.chdir(r"I:\2021\AG_LG07_1\mol methoxy_depo_2\AG_LG07_1_IVsVg\20210201")
dset = QTLab_Dataset.find()
data = dset.load(Stability_Diagram)
vgds = [x for x in np.around(np.linspace(0, 4, 10), decimals=2)]
vsds = [x for x in np.around(np.linspace(0, 0.5, 10), decimals=2)]
colors_vg = np.linspace(0.1, 0.5, num=len(vgds))
colors_vsd = np.linspace(0.1, 0.5, num=len(vsds))
for i in range(len(data)):
    biastraces = []
    gatetraces = []
    for vg, color_vg, vsd, color_vsd in zip(vgds, colors_vg, vsds, colors_vsd):
        biastrace = data[i].bias_trace(vg)
        biastrace.ps(
            linewidth=1,
            marker=None,
            label=f"$V_g$ = {vg} mV",
            prop={"size": 4},
            color=plt.cm.viridis(color_vg),
        )
        biastraces.append(biastrace)
        gatetrace = data[i].gate_trace(vsd)
        gatetrace.ps(
            linewidth=1,
            marker=None,
            label=f"$V_g$ = {vsd} mV",
            prop={"size": 4},
            color=plt.cm.magma(color_vsd),
        )
        gatetraces.append(gatetrace)

    fig = Figure(aspect_ratio=1, dpi=150)
    fig.add_subplot(
        Subplot_IVsVg(data[i], title=f"{dset[i]['device']}", cmap="viridis")
    )
    fig.add_subplot(Subplot_IV(*biastraces, legend=True, title=f"{dset[i]['device']}"))
    fig.add_subplot(Subplot_IVg(*gatetraces, legend=True, title=f"{dset[i]['device']}"))
    fig.visualise(
        f"figure_plot_SD_BT-GT_100_4V_1mVstep_first_test/{dset[i]['device']}_{i}.png"
    )
