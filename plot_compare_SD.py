#%%
import os
import string
import numpy as np
from imports.qtlab_data import *
from imports.dataclass import *
from helper_functions import *

os.chdir(r"H:\2021\AG_LG07_3")

# configuration
chip = "AG_LG_07_3"
eburn = "eburn"
mol = "mol spinvalve"
mol_name = "Spin Valve DyTb"
piezo_driver = False

dset = QTLab_Dataset.find(pattern=pattern_matcher(eburn, mol))
dset = dset[np.argsort(dset["timestamp"])[::-1]]
ivsvgset = dset[dset["type"] == "IVsVg"]
ivsvgset_electroburn = ivsvgset[ivsvgset["folder"] == eburn]
ivsvgset_molps = ivsvgset[ivsvgset["folder"] == mol]
devices = np.unique(ivsvgset_molps["device"])
#%%
for dev in devices:
    current_lst = []
    fig = Figure()
    d = ivsvgset_electroburn[ivsvgset_electroburn["device"] == dev]
    data = d.load(Stability_Diagram)
    if data:
        data = data[0]
        current_lst.append(np.mean(np.abs(data["Isd"].values)) * 5)
        if piezo_driver == True:
            data["Vg"] *= 12.5
        data.resample(256, 256)
        fig.add_subplot(
            Subplot_IVsVg(
                data,
                title=f"Dev {dev} Eburn, No {mol_name}",
                cmap="viridis",
                crange=(-np.max(current_lst), np.max(current_lst)),
            ),
        )
    d_ps = ivsvgset_molps[ivsvgset_molps["device"] == dev]
    data_molps = d_ps.load(Stability_Diagram)
    if data_molps:
        data_molps = data_molps[0]
        current_lst.append(np.mean(np.abs(data_molps["Isd"].values)) * 5)
        data_molps.resample(256, 256)
        if piezo_driver == True:
            data_molps["Vg"] *= 12.5
        fig.add_subplot(
            Subplot_IVsVg(
                data_molps,
                title=f"Dev {dev} Eburn, Yes {mol_name}",
                cmap="viridis",
                crange=(-np.max(current_lst), np.max(current_lst)),
            )
        )
        fig.visualise(f"Figures_SD_Comparison/{chip}/{dev}.png")


#%%
# Sandbox Cell **** Syntax Experimenting ****


def get_dataset(data_folder: str):
    pattern = f".*?(?P<folder>{data_folder}).*?\d+_(?P<exp>[a-zA-Z0-9_]+)_(?P<type>[a-zA-Z0-9\-_]+?)_(?P<device>[a-zA-Z]+[0-9]+)\.(?:dat|csv|txt)"
    dset = QTLab_Dataset.find(pattern=pattern)
    ivsvgset = dset[dset["type"] == "IVsVg"]
    data_folder = ivsvgset[ivsvgset["folder"] == data_folder]
    devices_list = np.unique(data_folder["device"])
    return data_folder, devices_list


exp_dir = ["eburn", "mol spinvalve"]

for burn, mol in zip(*exp_dir):
    data_eburn, device_eburn = get_dataset(burn)
    data_mol, device_mol = get_dataset(mol)

# %%
