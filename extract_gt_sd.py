#%%

import os
import glob
import string
import numpy as np
from imports.qtlab_data import *
from imports.dataclass import *
from helper_functions import *

# %%
# Change location
os.chdir(
    r"C:\\Users\\oums1095\\Nexus365\\Simen Sopp - OxNanoSpin Team Folder\\Transport\\Ale01_r31\\5.Temperature_Dataset\copy_justSD_Aug"
)
# %%
# Rename each stability diagram file
# The old name was for example 053623_Ale01_r31(GVIs15_1.0_9_0.1)_SD(Vg-20to20V)(Vsd100mV).dat
def rename_files_SD(match: str = "*SD*.dat", new_suffix: str = "_Ale01_IVsVg_r31.dat"):
    for file in list(glob.glob(match)):
        first_char = file.split("_")[0]
        new_name = first_char + new_suffix
        os.rename(file, new_name)


# %%
# Sort dataset from low to high T. The sorting criteria is timestamp
# as SDs were taking sequentially over different days
dset_temp_sorted = sorted(QTLab_Dataset.find(), key=lambda x: x["timestamp"])
T_list = []

for i, _ in enumerate(dset_temp_sorted):
    data = dset_temp_sorted[i].load(
        Stability_Diagram, axes=("Vg", "T", "Vsd", "Isd", "t")
    )
    dataSD = data[0]
    T_list.append(np.mean(dataSD["T"].values))
    print(f"Stability Diagram measured at {np.mean(dataSD['T'].values):.2} K")

# %%
dataSD = data[0]
T = np.mean(dataSD["T"].values)
print(f"Stability Diagram measured at {T:.2} K")
# %%
# It takes a lot, use it wisely
for i, _ in enumerate(dset):
    data = dset[i].load(Stability_Diagram, axes=("Vg", "T", "Vsd", "Isd", "t"))
    dataSD = data[0]
    dataSD["Vsd"] = 1e-3 * dataSD["Vsd"].values
    dataSD.correct_offset()
    gatetrace = (
        dataSD.zero_bias_gate_trace()
    )  # this method generate a zero-bias condutance gate trace, again see the stability diagram class in qtlab_data for exactly how it works
    fig = (
        Figure()
    )  # make a figure object, you can define things like aspect ratio and size
    fig.add_subplot(
        Subplot_IVsVg(dataSD, title=f"{dset[i]['filename']}", cmap="viridis")
    )  # plot the SD
    fig.add_subplot(
        Subplot_GVsVg(dataSD, title=f"{dset[i]['filename']}", cmap="viridis")
    )  # plot the conductance SD
    fig.add_subplot(Subplot_GVg(gatetrace))  # plot the conductance gate trace
    fig.visualise(f"figures/{dset[i]['filename']}.png")
