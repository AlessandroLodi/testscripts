# %%
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import string
from imports.qtlab_data import *
from imports.dataclass import *
from imports.physics_models import *
from helper_functions import *


# Change dir and import dataset
os.chdir(r"G:\2021\AG_LG06_6\mol gnr_dil1to100_1phenyloctane\AG_LG06_6_IVsVg\20210118")
dset = QTLab_Dataset.find()

# create the array for slice and colors. Initialise list for putting all the traces

# vsds = [x for x in np.around(np.linspace(0, 0.5, 5), decimals=2)]
vsds = [0.500]
colors_vsd = np.linspace(0.1, 0.5, num=len(vsds))
gt_list = []
dev_extracted = []

#%%
# create a device list and loop through over each device on that list
def extract_single_column(gt):
    return gt["Vg"][:].T, gt["Isd"][:].T


device_list = [dev for dev in np.unique(dset["device"])]


for i in range(len(device_list)):
    # for each device I want GT and the right color for the colormap
    for vsd, color in zip(vsds, colors_vsd):
        # load a Stability_Diagram object, by indexig the dset object
        actual_data = dset[dset["type"] == "IVsVg"][i].load(Stability_Diagram)
        # the actual data create a list so we need to take the first element each time of that list
        # this seems a bit stupid to me
        actual_data = actual_data[0]
        actual_data.resample(256, 256)
        # gt_list.append(actual_data.gatetrace(vs=vsd))
        gt_single = actual_data.gatetrace(vs=vsd)  # .shift_gatetrace(smooth=True)
        vg, isd = extract_single_column(gt_single)
        if np.log10(np.mean(isd)) > -7:
            dev_extracted.append(device_list[i])
            isd_rolled = np.roll(isd, (np.argmin(np.abs(vg)) - np.argmin(np.abs(isd))))
            gt_list.append(gt_single)

#%%
dt = {}
dt.update({"Vg": gt_list[0]["Vg"][:]})
for i in range(len(gt_list)):
    dt.update({f"Isd-{dev_extracted[i]}{i+1}": gt_list[i]["Isd"][:]})

df = pd.DataFrame(dt)
df.to_csv(
    path_or_buf="GT_{dev_mol_name[0]}_{dev_mol_name[1]}.csv", sep=",", index=False
)

#%%
dt_log = {}
dt_log.update({"Vg [V]": gt_list[0]["Vg"][:]})
for i in range(len(gt_list)):
    dt_log.update(
        {f"Isd_Log-{dev_extracted[i]}-{i+1} [A^-1]": np.log10(gt_list[i]["Isd"][:])}
    )

dev_mol_name = os.getcwd().split("\\")[2:4]
df_log = pd.DataFrame(dt_log)
df_log.to_csv(
    path_or_buf=f"GT_{vsd}V_Log_NoVgShift_{dev_mol_name[0]}_{dev_mol_name[1]}.csv",
    sep=",",
    index=False,
)

# %%
# Sandbox Cell **** Syntax Experimenting ****


def add_matrix_column(mat: np.array):
    aug_mat = np.zeros((len(mat)))
    aug_mat[:, :-1] = mat
    return aug_mat


vg_col = np.zeros((len(gt_list), len(gt_list)))
isd_col = np.zeros((len(gt_list), len(gt_list)))

for i in gt_list:
    vg_temp, isd_temp = extract_single_column(i)
    vg_col = add_matrix_column(vg_temp)
    isd_col = add_matrix_column(isd_temp)

# %%
