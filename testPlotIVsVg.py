import imports.physics_models_p as pm
import imports.dataclass 
from imports.qtlab_data import *
# from scipy.io import loadmat
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgba
import timeit
import time

# point to my files of DFT-calculated modes

dftModesPath = r'C:\Users\albus\OneDrive\Desktop\model fitting james thomas and bart\c4_2pyrene_lambdavector.txt'
dftmodes = pd.read_csv(dftModesPath, sep='\t')
dftmodes['freq'] *= 0.001  # change to eV from meV

# function to make a spectral density from DFT-calculated modes


def prepare_sdm(**settings):
    global dftmodes
    sdm = pm.spectral_density_model(w = np.linspace(1e-5,0.5,1000), time = np.linspace(0,1000,1000), E = settings.get('E',np.linspace(-0.5,0.5,500)))  # initialise an instance of sdm class and parameters
    sdm.add_background(settings['bgnd_L'], settings['bgnd_wc'])  # this function adds the background
    for w, lmbd in zip(dftmodes['freq'].values, dftmodes['lambda'].values):  # loop through each mode in dftmodes
        if lmbd > 0.0:  # only add non-zero lambdas
            sdm.add_mode(w, w*lmbd)  # this function adds the mode
    sdm.calculate_rate_constants(Y=2 * np.pi * (settings['VS'] ** 2 + settings['VD'] ** 2) / 2, T=settings['T'])
    return sdm  # you get the spectral density back


def stabdiag(Vsd,Vg,**settings):
    sdm = prepare_sdm(bgnd_L=settings['lmbd'], bgnd_wc=settings['wc'], VS=settings['VS'], VD=settings['VD'], T=settings['T'])
    return sdm.calculate_IVsVg(Vsd.flatten(),Vg.flatten(),settings['VS'],settings['VD'],settings['alpha_source'], settings['alpha_gate'],  settings['Vc'], settings['T'], spin=settings['spin'])

ivsvg_parameters = {'lmbd': 0.01, 'wc': 0.025, 'VS':1e-4, 'VD':1e-6, 'T':0.2,'alpha_source':0.5, 'alpha_gate':0.1, 'Vc':0, 'spin':0}

vsd = np.linspace(-0.1,0.1,128)
vg = np.linspace(-1,1,128)

vsd_grid, vg_grid = np.meshgrid(vsd,vg)

i = stabdiag(vsd_grid, vg_grid, **ivsvg_parameters)
i_grid = np.reshape(i, vsd_grid.shape)
g_grid = np.gradient(i_grid, vsd[1]-vsd[0], axis=1)
plt.pcolor(vg_grid, vsd_grid, i_grid, cmap='RdBu')
plt.pcolor(vg_grid, vsd_grid, g_grid, cmap='RdBu')
plt.colorbar()
plt.show()

