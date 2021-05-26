import os
import string
import numpy as np
from imports.qtlab_data import *
from imports.dataclass import *
from helper_functions import *

os.chdir(r"G:\Probestation\AG_LG20_5")

# configuration
chipPiece = "AG_LG20_5"
folder_1 = "eburn"
folder_2 = "mol spinvalve"
folder_3 = "mol spinvalve_2"
mol_name = "Dy–Tb"

# subfolders and pattern matching on the files
# match = "{}|{}|{}".format(folder_3, folder_2, folder_1)
match = "{}|{}".format(folder_2, folder_1)
pattern = ".*?(?P<folder>{}).*?\d+_(?P<exp>[a-zA-Z0-9_]+)_(?P<type>[a-zA-Z0-9\-_]+?)_(?P<device>[a-zA-Z]+[0-9]+)\.(?:dat|csv|txt)".format(
    match
)

# find all QTLab files in the folder and sort them newer to the front
dset = QTLab_Dataset.find(pattern=pattern)
ivsvgset = dset[dset["type"] == "IVsVg"]
ivsvgset_electroburn = ivsvgset[ivsvgset["folder"] == folder_1]
ivsvgset_molps = ivsvgset[ivsvgset["folder"] == folder_2]
ivsvgset_molps_2 = ivsvgset[ivsvgset["folder"] == folder_3]


# loop over the devices
devices = np.unique(ivsvgset_electroburn["device"])
for dev in devices:
    current_lst = []
    fig = Figure()
    print("***** Start Loading Here ******")
    d = ivsvgset_electroburn[ivsvgset_electroburn["device"] == dev]
    d_ps = ivsvgset_molps[ivsvgset_molps["device"] == dev]
    d_ps_2 = ivsvgset_molps_2[ivsvgset_molps_2["device"] == dev]
    print(d_ps_2)
    if d_ps_2:
        print("execute first if statement")
        data = d.load(Stability_Diagram)
        data_molps = d_ps.load(Stability_Diagram)
        data_molps_2 = d_ps_2.load(Stability_Diagram)
        data = data[0]
        data_molps = data_molps[0]
        data_molps_2 = data_molps_2[0]
        data.resample(256, 256)
        data_molps.resample(256, 256)
        data_molps_2.resample(256, 256)
        current_lst.append(np.mean(np.abs(data["Isd"].values)) * 5)
        fig.add_subplot(
            Subplot_IVsVg(
                data,
                title=f"Before Dropcasting {mol_name}",
                cmap="viridis",
                crange=(-np.max(current_lst), np.max(current_lst)),
            ),
        )
        current_lst.append(np.mean(np.abs(data_molps["Isd"].values)) * 5)
        fig.add_subplot(
            Subplot_IVsVg(
                data_molps,
                title=f"After Dropcasting {mol_name}",
                cmap="viridis",
                crange=(-np.max(current_lst), np.max(current_lst)),
            )
        )
        current_lst.append(np.mean(np.abs(data_molps_2["Isd"].values)) * 5)
        fig.add_subplot(
            Subplot_IVsVg(
                data_molps_2,
                title=f"After 2$^nd$ Dropcast {mol_name}",
                cmap="viridis",
                crange=(-np.max(current_lst), np.max(current_lst)),
            ),
        )
        fig.visualise(f"Figures_3_SD/{chipPiece}/{dev}.png")
    elif d_ps:
        data = d.load(Stability_Diagram)
        data_molps = d_ps.load(Stability_Diagram)
        data = data[0]
        data_molps = data_molps[0]
        data.resample(256, 256)
        data_molps.resample(256, 256)
        current_lst.append(np.mean(np.abs(data["Isd"].values)) * 5)
        fig.add_subplot(
            Subplot_IVsVg(
                data,
                title=f"Before Dropcasting {mol_name}",
                cmap="viridis",
                crange=(-np.max(current_lst), np.max(current_lst)),
            ),
        )
        current_lst.append(np.mean(np.abs(data_molps["Isd"].values)) * 5)
        fig.add_subplot(
            Subplot_IVsVg(
                data_molps,
                title=f"After Dropcasting {mol_name}",
                cmap="viridis",
                crange=(-np.max(current_lst), np.max(current_lst)),
            )
        )
        fig.visualise(f"Figures_just_2_SD/{chipPiece}/{dev}.png")
    else:
        continue
