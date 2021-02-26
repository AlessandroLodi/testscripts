#%%
from helper_functions import *
import numpy as np


energy = np.linspace(0, 4, 100)
y = (
    energy[i] ** 2 * np.exp(-energy[i] / (1.3806e-5 * 298)) for i in range(len(energy))
)

for i in y:
    print(np.floor(np.abs(np.log10(i))))

