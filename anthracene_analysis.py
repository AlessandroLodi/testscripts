#%%
import os
import numpy as np
import matplotlib.pyplot as plt
import string
import fnmatch
from imports.qtlab_data import *
from imports.dataclass import *
from imports.physics_models import *
from helper_functions import *
from pathlib import Path

path = Path("G:/2021/anthracene")
os.chdir(path)


def subdirs(path):
    for entry in os.scandir(path):
        if not entry.name.startswith(".") and entry.is_dir():
            yield entry.name


# python power: create a list with the experiments in each subfolders
# exclude the folders called Figures and eburn. Take advantage of the Unix filename pattern matching
# module fnmatch and of the subdirs function created above. The list comp is a double for loop, since
# one current value can be the iterator for the next loop

exp_lst = [
    dirs
    for top_dirs in subdirs(path)
    for dirs in subdirs(top_dirs)
    if not fnmatch.fnmatch(dirs, "eburn*") and not fnmatch.fnmatch(dirs, "figure*")
]

# use the QTLab_Dataset method for creating a huge list object with all the devices inside
# use my method match_pattern which is very general as it uses list splat operator
#%%
dset = []
for single_dataset in range(len(exp_lst)):
    dset.append(QTLab_Dataset.find(pattern=match_pattern(exp_lst[single_dataset])))

# %%
def extract_single_column(gt):
    return gt["Vg"][:].T, gt["Isd"][:].T


vsds = [0.500]
colors_vsd = np.linspace(0.1, 0.5, num=len(vsds))
gt_list = []
dev_extracted = []
for i in range(len(dset)):
    dataset = dset[i]
    dataset_type = dataset[dataset["type"] == "IVsVg"]
    if dataset_type:
        devices_dataset = np.unique(dataset_type["device"])
        for j in range(len(devices_dataset)):
            for vsd, color in zip(vsds, colors_vsd):
                try:
                    actual_data = dataset_type[j].load(Stability_Diagram)
                    actual_data = actual_data[0]
                    actual_data.resample(256, 256)
                    gate_trace_single = actual_data.gatetrace(vs=vsd)
                    Vg, Isd = extract_single_column(gate_trace_single)
                    if np.log10(np.mean(Isd)) > -7:
                        dev_extracted.append(devices_dataset[j])
                        Isd_rolled = np.roll(
                            Isd, np.argmin(np.abs(Vg)) - np.argmin(np.abs(Isd))
                        )
                        gt_list.append(gate_trace_single)
                except AttributeError:
                    continue

# %%
