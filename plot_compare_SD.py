#%%

import os
import string
import numpy as np
from imports.qtlab_data import *
from imports.dataclass import *
from helper_functions import *

os.chdir(r"G:\Probestation\AG_LG20_4")

# configuration
chip = "AG_LG20_4"
eburn = "eburn"
mol = "mol spinvalve"
mol_name = "DyTb"
gnr_name = "GNR_AOM"

dset = QTLab_Dataset.find(pattern=pattern_matcher(eburn, mol))
ivsvgset = dset[dset["type"] == "IVsVg"]
ivsvgset_electroburn = ivsvgset[ivsvgset["folder"] == eburn]
ivsvgset_molps = ivsvgset[ivsvgset["folder"] == mol]
# devices = np.unique(ivsvgset_molps["device"])
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
        data.resample(256, 256)
        fig.add_subplot(
            Subplot_IVsVg(
                data,
                # title=f"Dev {dev} Eburn, No {mol_name}",
                title=f"After Burning, Before Dropcasting {mol_name}",
                cmap="viridis",
                crange=(-np.max(current_lst), np.max(current_lst)),
                # range=(-4, 4),
                yrange=(-0.2, 0.2),
            ),
        )
    d_ps = ivsvgset_molps[ivsvgset_molps["device"] == dev]
    data_molps = d_ps.load(Stability_Diagram)
    if data_molps:
        data_molps = data_molps[0]
        current_lst.append(np.mean(np.abs(data_molps["Isd"].values)) * 5)
        data_molps.resample(256, 256)
        fig.add_subplot(
            Subplot_IVsVg(
                data_molps,
                title=f"Check After Dropcasting {mol_name}",
                cmap="viridis",
                crange=(-np.max(current_lst), np.max(current_lst)),
                yrange=(-0.2, 0.2),
            )
        )
    fig.visualise(f"Figures_SD_comparison/{chip}/{dev}.png")


#%%
# Sandbox Cell **** Syntax Experimenting ****


# exp_dir = ["eburn", "mol spinvalve"]

# for burn, mol in zip(*exp_dir):
#     data_eburn, device_eburn = get_dataset(burn)
#     data_mol, device_mol = get_dataset(mol)

# %%
