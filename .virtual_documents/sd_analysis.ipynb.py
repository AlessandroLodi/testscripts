import os
import numpy as np
from imports.qtlab_data import *
from imports.dataclass import *
from matplotlib.colors import to_rgba
try:
    from imports.simmons import simmons
except:
    from imports.physics_models_p import *

    simmons = physics_models.simmons
    # subfolders and pattern matching on the files
from matplotlib.colors import LinearSegmentedColormap


def correct_path_format(path:str):
    """
    Paste the path you copy from windows into this function. It replace the single backslash with the double.
    Needs an r in from of the string.
    """
    lpath = path.split('\\')
    return '\\'.join(lpath)


dat_dir = correct_path_format(r'C:\Users\oums1095\projects\gnr_set\data\5.Temperature_Dataset\copy_justSD_Aug')
fig_dir = correct_path_format(r"C:\Users\oums1095\projects\gnr_set\figures\fit_zbt")
os.chdir(dat_dir)
# find the data
dset = QTLab_Dataset.find()
print(dset)


# load the data, in this case I load just one by indexing the dataset
data = dset[-3].load(Stability_Diagram, axes=("Vg", "T", "Vsd", "Isd", "t"))
sd = data[0]  # the SD is a pandas dataframe that is the first item


sd['Vsd'].values.shape, sd['Isd'].values.shape, sd['T'].values.shape


T = sd['T'].values.mean() # sd is a Pandas df so retrieve the numpy object
print(f"Stability diagram measure at {round(T,2)} K")
sd["Vsd"] *= 1e-3 # the methods want to work in V and not mV
sd.resample(512, 512) # bug! -> this method does not reshape all the axes but just Vsd and Isd apparently
sd.correct_offset() # subtract a (quasi)-zero-bias gate trace
zbgt = sd.zero_bias_gate_trace() # gatetrace is stil a Stability_Diagram Object


sd['Vsd'].values.shape, sd['Isd'].values.shape, sd['T'].values.shape


fig = Figure()
save = True
fig.add_subplot(Subplot_IVsVg(sd, title=f"sd_{T}_K", cmap='plasma')) # plot SD
fig.add_subplot(Subplot_GVsVg(sd, title=f"sd_{round(T,2)}_K", cmap="plasma")) # plot conductance SD 
fig.add_subplot(Subplot_GVg(zbgt, title=f"zbgt_{T}_K", cmap='plasma')) # plot gatetrace
if save:    
    os.chdir(fig_dir)
    fig.visualise(save_as='diocane/adesso')


from IPython.display import display, clear_output


# this method does not work at the moment in a jupyter nb as the figure does not allow the click to be called at runtime
sd.manual_fit_Vc()


vcs = [-15.145847996335647, -9.188144473863547, -2.2866463339701255, 1.7244807900704942, 7.387248494598431, 11.280401291461388]


alpha = 0.023 # meV/V
zbgt_fits = []
vc = vcs[0]
sd_copy = sd.copy()
setdct = {"Vc": vc, "T": T}
sd_copy.ps(**setdct)
peak_lower_lim = sd_copy[sd_copy["Vg"] > (vc - 2)] 
peak_high_lim = sd_copy[sd_copy["Vg"] > (vc +2)]
gMaxTemp = zbgt["Gsd"].values[(np.argmin(np.abs(zbgt["Vg"].values - vc)))]


p0 = {"Vc": vc, "Gmax": gMaxTemp, "alpha": alpha}
bounds = [(vc - 1, 0.5e-11, .85*alpha), (vc + 1, 1.5e-11, 1.15*alpha)]
params, r = sd_copy.fit_coulomb_peak(p0 = p0) 
params["alpha"],params["Gmax"],params["Vc"]


zbgtFits = []
params["T"] = T  # add the temperature to the the dictionary of parameters
vg = zbgt["Vg"].values
fitGsd = physics_models.physics_models.thermal_broadening(vg, **params)  # use the optimised parameters and the gate voltage array to generate the Gsd fit values
zbgtFit = zbgt.copy()  # make a copy of the gate trace
zbgtFit["Gsd"] = fitGsd  # replace the Gsd data with the fitted data
try:
    zbgtFits.append(zbgtFit)  # add the fitted gate trace to the list
except:
    pass

zbgtFitSum = zbgt.copy()  # make another copy of the gate trace to play with
zbgtFitSum["Gsd"] -= zbgtFitSum[
    "Gsd"
].values  # make the Gsd values equal to themselves minus themselves, i.e. make them zero!
for fit in zbgtFits:  # loop over the fits we added to this list
    zbgtFitSum["Gsd"] += fit[
        "Gsd"
    ].values  # add the fit values one by one to generate a sum of fits

zbgtFitSum.ps(
    color="black", label="sum of fits", linewidth=2
)  # change some of the plotting parameters to make it obvious which one is the sum

fig = dataclass.Figure()  # make a figure
fig.add_subplot(
    qtlab_data.Subplot_GVg(zbgt, *zbgtFits, zbgtFitSum, legend=True)
)  # plot the experimental gate traces, and the list of fits all together
fig.visualise(fig_dir) 


dir(physics_models.physics_models)


import pandas as pd
pd.__version__


import numpy as np
import scipy as sp
from scipy.special import expit, logit
import scipy.optimize

def f(x,x0,g,c,k):
    y = c*expit(k*10.*(x-x0)) + g*(1.-c)
    return y

#               x0                      g                       c                       k
p0 = np.array([8.841357069490852e-01, 4.492363462957287e-19, 5.547073496706608e-01, 7.435378446218519e+00])
bounds = np.array([[-1.,1.], [0.,1.], [0.,1.], [0.,20.]])
x = np.array([1.0, 1.0, 1.0, 1.0, 1.0, 0.8911796599834791, 1.0, 1.0, 1.0, 0.33232919909076103, 1.0])
y = np.array([0.999, 0.999, 0.999, 0.999, 0.999, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001])
s = np.array([0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9])

print([pval >= b[0] and pval <= b[1] for pval,b in zip(p0,bounds)])

fit,cov = sp.optimize.curve_fit(f,x,y,p0=p0,sigma=s,bounds=([b[0] for b in bounds],[b[1] for b in bounds]),method='dogbox',tr_solver='exact')

print(fit)
print(cov)


from scipy.optimize import minimize, Bounds
import numpy as np
import sys

working = True
while working:
    bounds = Bounds(np.array([0.1]), np.array([1.0]))
    n_inputs = len(bounds.lb)
    x0 = np.array(bounds.lb + (bounds.ub-bounds.lb) * np.random.random(n_inputs))
    try:
        minimize(lambda x: np.linalg.norm(x), x0, method='SLSQP', bounds=bounds)
        print('.', end='')
    except:
        ex = sys.exc_info()
        print('\nBangget_ipython().getoutput("', ex[0], ex[1])")
        working = False
        
x0, bounds



