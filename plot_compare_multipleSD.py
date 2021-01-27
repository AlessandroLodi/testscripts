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

os.chdir(r"I:\2021\AG_LG06_6")

# configuration
chipPiece = "eburn"
folder_electroburn = "eburn"
folder_molps = "mol gnr_dil1to100_1phenyloctane"
folder_molps_2 = "mol gnr_dil1to100_1phenyloctane_LB_2ndCheck"

# Have you used the piezo driver (which multiplies your voltage for 12.5 V) ?
piezo_driver = False

# subfolders and pattern matching on the files
match = "{}|{}|{}".format(folder_molps_2, folder_molps, folder_electroburn)
# match = "{}|{}".format(folder_molps, folder_electroburn)
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
print(ivsvgset_electroburn)
print("###############")
print("###############")
ivsvgset_molps = ivsvgset[ivsvgset["folder"] == folder_molps]
print(ivsvgset_molps)
print("###############")
print("###############")
ivsvgset_molps_2 = ivsvgset[ivsvgset["folder"] == folder_molps_2]
print(ivsvgset_molps_2)


# loop over the devices
devices = np.unique(ivsvgset_molps["device"])
print(devices)
# devices = ['d35']
for dev in devices:
    if dev[0] in string.ascii_lowercase[:]:
        if int(dev[1:]) < 39:
            d = ivsvgset_electroburn[ivsvgset_electroburn["device"] == dev]
            # d.axes = ('Vsd','Vg','n','Isd')
            # Vsd = d['Vsd'].values
            # range = (-2e-8,2e-8)
            fig = Figure()
            print(d)
            # gatetrace = ivgset_electroburn[ivgset_electroburn['device'] == dev]
            data = d.load(Stability_Diagram)
            if data:
                data = data[0]
                if piezo_driver == True:
                    data["Vg"] *= 12.5
                data.resample(256, 256)
                pre_gt = data.zero_bias_gate_trace()
                fig.add_subplot(Subplot_IVsVg(data, title="Probe Station, No GNR, RT"))
            d_ps = ivsvgset_molps[ivsvgset_molps["device"] == dev]
            data_molps = d_ps.load(Stability_Diagram)
            d_ps_2 = ivsvgset_molps_2[ivsvgset_molps_2["device"] == dev]
            data_molps_2 = d_ps_2.load(Stability_Diagram)
            if data_molps:
                data_molps = data_molps[-1]
                data_molps.resample(256, 256)
                if piezo_driver == True:
                    data_molps["Vg"] *= 12.5
                molps_gt = data_molps.zero_bias_gate_trace()
                fig.add_subplot(
                    Subplot_IVsVg(
                        data_molps,
                        title="Device GNR Methoxy, \n 1st Check after gs, RT",
                    )
                )
                if data_molps_2:
                    data_molps_2 = data_molps_2[-1]
                    data_molps_2.resample(256, 256)
                    if piezo_driver == True:
                        data_molps["Vg"] *= 12.5
                    # data_molps_2["Vg"] = data_molps_2["Vg"]
                    molps_gt = data_molps_2.zero_bias_gate_trace()
                    fig.add_subplot(
                        Subplot_IVsVg(
                            data_molps_2,
                            title="Device GNR Methoxy \n 2nd Check, RT",
                        )
                    )
                fig.visualise("Figures_SD_3/{}/{}.png".format(chipPiece, dev))
