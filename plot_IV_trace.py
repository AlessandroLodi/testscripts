# %%
import os
import numpy as np
from imports.dataclasse import *
from imports.qtlab_data import *
from matplotlib.colors import to_rgba

try:
    from imports.simmons import simmons
except:
    from imports.physics_models_p import *

    simmons = physics_models.simmons
import string
import matplotlib.pyplot as plt

# configuration
folder_electroburn = "mol gnr_methoxy_dil1to100_tol_gs_sd_goodev"
# Have you used the piezo driver (which multiplies your voltage for 12.5 V) ?
piezo_driver = False

chipPiece = "AG_GG01"
# subfolders and pattern matching on the files
match = "{}".format(folder_electroburn)
pattern = ".*?(?P<folder>{}).*?\d+_(?P<exp>[a-zA-Z0-9_]+)_(?P<type>[a-zA-Z0-9\-_]+?)_(?P<device>[a-zA-Z]+[0-9]+)\.(?:dat|csv|txt)".format(
    match
)
os.chdir(r"H:\2021\AG_LG06_5_GNR_anthracene")
# find all QTLab files in the folder and sort them newer to the front
dset = QTLab_Dataset.find(pattern=pattern)
dset = dset[np.argsort(dset["timestamp"])[::-1]]

print(dset)


ivsvgset = dset[dset["type"] == "IVg"]
devices = np.unique(ivsvgset["device"])

for dev in devices:
    if dev[0] in string.ascii_lowercase[:]:
        if int(dev[1:]) < 39:
            d = ivsvgset[ivsvgset["device"] == dev]
            fig = Figure(aspect_ratio=1.0, rows=1, font=None, dpi=150, size=1.0)
            data = d.load(QTLab_Data)[0]
            print(data["Vg"])
            # %%

            print(data_vg)
            # %%
            if data:
                if piezo_driver == True:
                    data["Vg"] *= 12.5
                data["Isd"] *= 1e9
                data.plot_settings(
                    linewidth=0.8, color=to_rgba("C0", 0.6), label="raw data"
                )

                fig.add_subplot(
                    Subplot_IVg(
                        data,
                        title="Gate Sweep, RT, Vsd = 0.2 V",
                    )
                )
                fig.visualise("Figures_gs_gooddev/{}/{}.png".format(chipPiece, dev))
