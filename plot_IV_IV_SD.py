#%%
import os
import string
import numpy as np
from imports.qtlab_data import *
from imports.dataclass import *
from helper_functions import *

os.chdir(r"I:\2021\Test_3T_Nanogap_chip_10")

# configuration
chip = "Test_3T_Nanogap_chip_10"
eburn = "1_rtest"
mol = "2_rtest_post_submersion_dil_1to1000"
mol_name = "4cnr-OMe"

dset = QTLab_Dataset.find(pattern=pattern_matcher(eburn, mol))
ivset = dset[dset["type"] == "R"]
ivsvgset = dset[dset["type"] == "IVsVg"]
ivset_electroburn = ivset[ivset["folder"] == eburn]
ivset_molps = ivset[ivset["folder"] == mol]
ivsvgset_molps = ivsvgset[ivsvgset["folder"] == mol]
devices = np.unique(ivsvgset_molps["device"])

#%%
for dev in devices:
    fig = Figure()
    d = ivset_electroburn[ivset_electroburn["device"] == dev]
    data = d.load(QTLab_Data)[0]
    if data:
        fig.add_subplot(Subplot_IV(data, title=f"Before {mol_name}"),)
        data_IV = ivset_molps[ivset_molps["device"] == dev]
        data_molps = data_IV.load(QTLab_Data)[0]
        if data_molps:
            fig.add_subplot(Subplot_IV(data_molps, title=f"After {mol_name}"))
            data_IVsVg = ivsvgset_molps[ivsvgset_molps["device"] == dev]
            data_IVsVg_molps = data_IVsVg.load(Stability_Diagram)
            data_IVsVg_molps = data_IVsVg_molps[0]
            data_IVsVg_molps.resample(256, 256)
            fig.add_subplot(
                Subplot_IVsVg(
                    data_IVsVg_molps, title=f"After {mol_name}", cmap="viridis"
                )
            )
        fig.visualise(f"Figures_IV_IV_SD_comparison/{chip}/{dev}.png")


# %%
