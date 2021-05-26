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

os.chdir(r"I:\2019\alessandrofet\stabdiag\stabdiag\stabdiag_IVsVg")
dset = QTLab_Dataset.find()
data = dset.load(Stability_Diagram)
max_vsd = 0.39
vsds = [x for x in np.around(np.linspace(0, max_vsd, num=5), decimals=2)]
colors = np.linspace(0.1, max_vsd, num=5)
for i in range(len(data)):
    gatetraces = []
    for vsd, color in zip(vsds, colors):
        gate_trace = data[i].gatetrace(vsd)
        gate_trace.ps(
            linewidth=1,
            marker=None,
            label=f"$V_b$ = {1e3*vsd} mV",
            color=plt.cm.viridis(color),
            yrange=(-0.2, 0.2),
        )
        gatetraces.append(gate_trace)

    fig = Figure(aspect_ratio=1, dpi=150)
    fig.add_subplot(
        Subplot_IVsVg(data[i], title=f"{dset[i]['device']}", cmap="viridis")
    )
    fig.add_subplot(Subplot_IVg(*gatetraces, legend=True, title=f"{dset[i]['device']}"))
    fig.visualise(f"figure_plot_SD_GT_positve/{dset[i]['device']}_{i}.png")

# %%
