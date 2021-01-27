# %%
import os
import numpy as numpy
import matplotlib.pyplot as plt
import string
from imports.qtlab_data import *
from imports.dataclass import *
from imports.physics_models import *
from matplotlib.colors import to_rgba
folder_IVg  = "mol gnr_methoxy_dil1to100_tol_gs_sd_goodev"
chipPiece   = "AG_LG06_5_GNR_anthracene"
match = "{}".format(folder_IVg)
pattern = ".*?(?P<folder>{}).*?\d+_(?P<exp>[a-zA-Z0-9_]+)_(?P<type>[a-zA-Z0-9\-_]+?)_(?P<device>[a-zA-Z]+[0-9]+)\.(?:dat|csv|txt)".format(match)
os.chdir(r"D:\2021\AG_LG06_5_GNR_anthracene")
dset = QTLab_Dataset.find(pattern=pattern)
dset = dset[np.argsort(dset["timestamp"])[::-1]]
dset[dset['type']=='IVg']
data = dset.load(QTLab_Data)
data1 = dset.load(QTLab_Data)
data2 = dset.load(QTLab_Data)

#%%
# data[0].cycle_to_trace(cyclic_axis='Isd', method='average')
# print(data[0])
# print(data[1])

#%%


#%%
for i in range(len(data)):
    fig = Figure()
    fig.add_subplot(Subplot_IVg(data[i], title=f"device pure {dset['device'][i]}_{i}"))
    fig.add_subplot(Subplot_IVg(data1[i].cycle_to_trace(cyclic_axis='Isd', method='average'), title=f"device cycle_to_trace {dset['device'][i]}_{i}"))
    fig.add_subplot(Subplot_IVg(data2[i].average_cycles(), title=f"device average_cycles {dset['device'][i]}_{i}"))
    fig.visualise(f"Figure/{folder_IVg}/method_comparison/{dset['device'][i]}_{i}.png")
# %%
for i in range(len(data)):
    fig = Figure()
    fig.add_subplot(Subplot_IVg(data[i], title=f"device {dset['device'][i]}_{i}"))
    fig.visualise(f"Figure/{folder_IVg}/average_justload()/{dset['device'][i]}_{i}.png")
# %%

# %%

# %%
