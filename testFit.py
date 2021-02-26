# %%

import imports.physics_models_p as pm
from imports.dataclass import *
from imports.qtlab_data import *

# from scipy.io import loadmat
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgba
import timeit
import time

path = r"C:\Users\albus\OneDrive\Desktop\model fitting james thomas and bart\170822_TL_300_6_TL_IVsVg-raw_g14.dat"
dftModesPath = r"C:\Users\albus\OneDrive\Desktop\model fitting james thomas and bart\c4_2pyrene_lambdavector.txt"
dftmodes = pd.read_csv(dftModesPath, sep="\t")
dftmodes["freq"] *= 0.001


def prepare_sdm(**settings):
    global dftmodes
    sdm = pm.spectral_density_model(
        w=np.linspace(1e-5, 0.5, 1000),
        time=np.linspace(0, 500, 1000),
        E=settings.get("E", np.linspace(-0.5, 0.5, 500)),
    )
    sdm.add_background(settings["bgnd_L"], settings["bgnd_wc"])
    for w, lmbd in zip(dftmodes["freq"].values, dftmodes["lambda"].values):
        if lmbd > 0.0:
            sdm.add_mode(w, w * lmbd)
    sdm.calculate_rate_constants(
        Y=2 * np.pi * (settings["VS"] ** 2 + settings["VD"] ** 2) / 2, T=settings["T"]
    )
    return sdm


def calculate_IV(Vsd, VS, VD, lmbd, wc, T, alpha_source, spin):
    sdm = prepare_sdm(bgnd_L=lmbd, bgnd_wc=wc, VS=VS, VD=VD, T=T)
    print({"VS": VS, "VD": VD, "lmbd": lmbd, "wc": wc})
    return np.asarray(sdm.calculate_IV(Vsd, VS, VD, alpha_source, T, spin=spin)) * 1e9


def stabdiag(Vsd, Vg, **settings):
    sdm = prepare_sdm(
        bgnd_L=settings["lmbd"],
        bgnd_wc=settings["wc"],
        VS=settings["VS"],
        VD=settings["VD"],
        T=settings["T"],
    )
    return sdm.calculate_IVsVg(
        Vsd.flatten(),
        Vg.flatten(),
        settings["VS"],
        settings["VD"],
        settings["alpha_source"],
        settings["alpha_gate"],
        settings["Vc"],
        settings["T"],
        spin=settings["spin"],
    )


dat = Stability_Diagram.load_from_file(path, cyclic_method="average")
dat.plot_settings(T=77)

# print(dat.manual_fit_Vc()) # use this function to get Vc
# print(dat.manual_fit_alpha()) # use this function to get alpha_source and alpha_gate

#%%

sts = {
    "Vc": 57.329551960119417,
    "alpha_source": 0.48694930170632039,
    "alpha_gate": 0.0051023140720955094,
}  # these values are obtained from the manual_fit_Vc() and manual_fit_alpha() functions
params = {
    "VS": 5e-4,
    "VD": 5e-6,
    "lmbd": 0.2,
    "wc": 0.025,
    "T": 77,
    "alpha_source": 0.4863911384199851,
    "spin": 0.0,
}  # initial guesses for parameters
dat.ps(**sts)
dat.resample(128, 128)
dat.correct_offset(zero=0.01)
trace = dat.resonance_bias_trace()
trace["Isd"] *= 1e9
(
    params,
    r2,
    fit,
) = trace.fit(  # this is the fitting function..so we fit the calculate_IV and return the parameters
    calculate_IV,
    p0=params,
    bounds={"VS": [1e-6, 1e-1], "VD": [1e-6, 1e-1], "lmbd": [1e-2, 1], "wc": [0, 0.1]},
    fix=[
        "T",
        "alpha_source",
        "spin",
        "wc",
    ],  # fix those that you know, here we fit: 'VS','VD','lmbd'
    followprogress=True,
    return_dict=True,
)
print(params)
params["alpha_gate"] = sts["alpha_gate"]  # IVsVg needs the alpha_gate
params["Vc"] = sts["Vc"]  # IVsVg needs Vc (i.e. the gate voltage of the transition

fitsd = dat.copy()

fitsd["Isd"] = np.reshape(
    stabdiag(fitsd["Vsd"].values, fitsd["Vg"].values, **params),
    fitsd["Vsd"].values.shape,
)
fig = Figure()
fig.add_subplot(Subplot_IV(trace, fit))
fig.add_subplot(Subplot_GVsVg(dat, method="savgol5_1"))
fig.add_subplot(Subplot_GVsVg(fitsd, method="savgol5_1"))
fig.visualise()
