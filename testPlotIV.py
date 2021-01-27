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
    sdm = pm.spectral_density_model(w=np.linspace(1e-5, 0.5, 1000),E=np.linspace(-0.5, 0.5, 1000),time=np.linspace(0,1000,1000))  # initialise an instance of sdm class and parameters
    sdm.add_background(settings['bgnd_L'], settings['bgnd_wc'])  # this function adds the background
    for w, lmbd in zip(dftmodes['freq'].values, dftmodes['lambda'].values):  # loop through each mode in dftmodes
        if lmbd > 0.0:  # only add non-zero lambdas
            sdm.add_mode(w, w*lmbd)  # this function adds the mode
    sdm.calculate_rate_constants(Y=2 * np.pi * (settings['VS'] ** 2 + settings['VD'] ** 2) / 2, T=settings['T'])
    return sdm  # you get the spectral density back

def calculate_IV(Vsd, VS, VD, lmbd, wc, T, alpha_source, spin):
    sdm = prepare_sdm(bgnd_L = lmbd, bgnd_wc = wc, VS= VS, VD=VD, T = T)
    print({'VS': VS, 'VD': VD, 'lmbd': lmbd, 'wc': wc})
    return np.asarray(sdm.calculate_IV(Vsd, VS, VD, alpha_source, T, spin=spin))*1e9

iv_parameters = {'lmbd': 0.01, 'wc': 0.025, 'VS':0.001, 'VD':0.001, 'T':5,'alpha_source':0.5, 'spin':0}
vsd = np.linspace(-0.4,0.4,100)
i = calculate_IV(vsd, **iv_parameters)
g = np.gradient(i, vsd[1]-vsd[0])

plt.plot(vsd,i)
plt.show()

plt.plot(vsd,g)
plt.show()


