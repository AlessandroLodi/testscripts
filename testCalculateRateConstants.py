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

# function to make a spectral density from DFT-calculated modes


def prepare_sdm(**settings):
    global dftmodes
    sdm = pm.spectral_density_model(w=np.linspace(1e-5, 0.5, 1000),E=np.linspace(-0.5, 0.5, 1000),time=np.linspace(0,8000,1000))  # initialise an instance of sdm class and parameters
    sdm.add_background(settings['bgnd_L'], settings['bgnd_wc'])  # this function adds the background
    for w, lmbd in zip(dftmodes['freq'].values, dftmodes['lambda'].values):  # loop through each mode in dftmodes
        if lmbd > 0.0:  # only add non-zero lambdas
            sdm.add_mode(w, w*lmbd)  # this function adds the mode
    sdm.calculate_rate_constants(Y=2 * np.pi * (settings['VS'] ** 2 + settings['VD'] ** 2) / 2, T=settings['T'])  # calculates rate constants
    return sdm  # you get the spectral density back

# add some basic parameters and get your spectral density

parameters = {'bgnd_L': 0.15, 'bgnd_wc': 0.025, 'VS':0.001, 'VD':0.0001, 'T':5}

testSpecDensity = prepare_sdm(**parameters)  # call the function

plt.plot(testSpecDensity.E, np.real(testSpecDensity.k_ox))
plt.plot(testSpecDensity.E, np.real(testSpecDensity.k_red))
plt.show()

raise SystemExit