import imports.physics_models_p as pm
from imports.dataclass import *
from imports.qtlab_data import *
# from scipy.io import loadmat
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgba
import timeit
import time

# point to my files of DFT-calculated modes

dftModesPath = r'C:\Users\james.thomas\Desktop\Oxford\DFT\polyynes\c4_2pyrene_lambdavector.txt'
dftmodes = pd.read_csv(dftModesPath, sep='\t')
dftmodes['freq'] *= 0.001  # change to eV from meV
print(dftmodes)

# function to make a spectral density from DFT-calculated modes


def prepare_sdm(**settings):
    global dftmodes
    sdm = pm.spectral_density_model(w=np.linspace(1e-5, 0.5, 1000))  # initialise an instance of sdm class and parameters
    sdm.add_background(settings['bgnd_L'], settings['bgnd_wc'])  # this function adds the background
    for w, lmbd in zip(dftmodes['freq'].values, dftmodes['lambda'].values):  # loop through each mode in dftmodes
        if lmbd > 0.0:  # only add non-zero lambdas
            sdm.add_mode(w, w*lmbd)  # this function adds the mode
    return sdm  # you get the spectral density back

# add some basic parameters and get your spectral density

parameters = {'bgnd_L': 0.2, 'bgnd_wc': 0.025}
testSpecDensity = prepare_sdm(**parameters)  # call the function

# plot the background, and the modes one-by-one

plt.plot(testSpecDensity.w, testSpecDensity.J)  # plot the background
for mode in testSpecDensity.modes:  # loop through the modes
    plt.plot(mode[0], mode[1], 'ko')  # plot them one-by-one
plt.xlabel('$\hbar\omega$, eV')
plt.show()
