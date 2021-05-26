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
ivsvgset = dset[dset["type"] == "R"]
ivsvgset_electroburn = ivsvgset[ivsvgset["folder"] == eburn]
ivsvgset_molps = ivsvgset[ivsvgset["folder"] == mol]
devices = np.unique(ivsvgset_molps["device"])

#%%
for dev in devices:
    fig = Figure()
    d = ivsvgset_electroburn[ivsvgset_electroburn["device"] == dev]
    data = d.load(QTLab_Data)[0]
    if data:
        fig.add_subplot(Subplot_IV(data, title=f"Before {mol_name}", cmap="viridis",),)
        d_ps = ivsvgset_molps[ivsvgset_molps["device"] == dev]
        data_molps = d_ps.load(QTLab_Data)[0]
        if data_molps:
            fig.add_subplot(
                Subplot_IV(data_molps, title=f"After {mol_name}", cmap="viridis",)
            )
        fig.visualise(f"Figures_IV_comparison/{chip}/{dev}.png")
