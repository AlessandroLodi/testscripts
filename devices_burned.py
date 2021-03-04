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

path = Path("I:/AL_LG05_1")
os.chdir(path)

chip = "AG_LG_07_3"
eburn = "eburn"
mol_name = "Spin Valve DyTb"
piezo_driver = False

dset = QTLab_Dataset.find(pattern=match_pattern(eburn))
dset = dset[np.argsort(dset["timestamp"])[::-1]]
ivsvgset = dset[dset["type"] == "IVsVg"]
ivsvgset_electroburn = ivsvgset[ivsvgset["folder"] == eburn]
devices = np.unique(ivsvgset_electroburn["device"])

# %%
