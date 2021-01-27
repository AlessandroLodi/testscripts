import os

import numpy as np
from matplotlib.colors import to_rgba

from imports.dataclasse import *
from imports.qtlab_data import *

try:
    from imports.simmons import simmons
except:
    from imports.physics_models_p import *

    simmons = physics_models.simmons
import string

os.chdir(r"H:\2021\AG_LG06_4_GNR_anthracene")

# configuration
chipPiece = "AG_LG06_4_GNR_anthracene"
folder_electroburn = "eburn"
folder_molps = "mol gnr_dil1to100_1phenyloctane_r_gs_sd"


# Have you used the piezo driver (which multiplies your voltage for 12.5 V) ?
piezo_driver = False

# subfolders and pattern matching on the files
match = "{}|{}".format(folder_molps, folder_electroburn)
pattern = ".*?(?P<folder>{}).*?\d+_(?P<exp>[a-zA-Z0-9_]+)_(?P<type>[a-zA-Z0-9\-_]+?)_(?P<device>[a-zA-Z]+[0-9]+)\.(?:dat|csv|txt)".format(
    match
)


# find all QTLab files in the folder and sort them newer to the front
dset = QTLab_Dataset.find(pattern=pattern)
dset = dset[np.argsort(dset["timestamp"])[::-1]]

print(dset)

# select only the IVsVg data
ivsvgset = dset[dset["type"] == "IVsVg"]

print(ivsvgset)

# ivgset = dset[dset["type"] == "IVsVg"]

ivsvgset_electroburn = ivsvgset[ivsvgset["folder"] == folder_electroburn]
print("###############")
print("###############")
print(ivsvgset_electroburn)
ivsvgset_molps = ivsvgset[ivsvgset["folder"] == folder_molps]
print("###############")
print("###############")
print(ivsvgset_molps)


# loop over the devices
devices = np.unique(ivsvgset_molps["device"])
print(devices)
for dev in devices:
    if dev[0] in string.ascii_lowercase[:]:
        d = ivsvgset_electroburn[ivsvgset_electroburn["device"] == dev]
        fig = Figure()
        print(d)
        data = d.load(Stability_Diagram)
        if data:
            data = data[0]
            if piezo_driver == True:
                data["Vg"] *= 12.5
            data.resample(256, 256)
            pre_gt = data.zero_bias_gate_trace()
            fig.add_subplot(Subplot_IVsVg(data, title="probe station, no GNR, RT"))
        d_ps = ivsvgset_molps[ivsvgset_molps["device"] == dev]
        data_molps = d_ps.load(Stability_Diagram)
        if data_molps:
            data_molps = data_molps[-1]
            data_molps.resample(256, 256)
            if piezo_driver == True:
                data_molps["Vg"] *= 12.5
            molps_gt = data_molps.zero_bias_gate_trace()
            fig.add_subplot(
                Subplot_IVsVg(data_molps, title="Device GNR Anthracene, RT")
            )
            fig.visualise("Figures_SD_comparison/{}/{}.png".format(chipPiece, dev))
