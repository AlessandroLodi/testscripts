import os
import numpy as np
from imports.qtlab_data import *
from imports.dataclass import *
from matplotlib.colors import to_rgba
from collections import defaultdict
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
# os.chdir(dat_dir)
dset = QTLab_Dataset.find(dat_dir)
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


sd['Vsd'].values.shape, sd['Isd'].values.shape


fig = Figure()
fig.add_subplot(Subplot_IVsVg(sd, title=f"sd_{round(T,2)}_K", cmap='plasma')) # plot SD
fig.add_subplot(Subplot_GVsVg(sd, title=f"sd_{round(T,2)}_K", cmap="plasma")) # plot conductance SD 
fig.add_subplot(Subplot_GVg(zbgt, title=f"zbgt_{round(T,2)}_K", cmap='plasma')) # plot gatetrace
fig.visualise(f'{fig_dir}/sd_zbgt_{int(T)}_K')


vcs = [-17.97, -12.16, -6.25, -0.81, 3.69, 8.67, 15.05]
alpha = 0.023 # meV/V
gatetraceFits = []  # an empty list to add the gate trace fits to in the for loop
zbgt_fits = []


fit_dct_deafult = defaultdict()

for vc in vcs:  
    dat2 = sd.copy() 
    setdct = {"Vc": vc, "T": T}  
    dat2.ps(**setdct) 
    dat2 = dat2[(dat2["Vg"] > (vc - 2.5)) & (dat2["Vg"] < (vc + 2.5))]  
    gMaxTemp = zbgt["Gsd"].values[(np.argmin(np.abs(zbgt["Vg"].values - vc)))] # We will take this as the initial guess for Gmax for the fitting
    # print("Max Gsd in this window: {:.3e} S".format(gMaxTemp))  # print the Gmax
    p0 = {
        "T": T,
        "Vc": vc,
        "Gmax": gMaxTemp,
        "alpha": alpha
    }  
    # print(f">>> P0 in the script = {p0}")
    bounds = [
        (T - 0.5, vc - 1, 0.3, 0.85 * alpha),
        (T + 0.5, vc + 1, 0.75, 1.15 * alpha)] 
    params, r = dat2.fit_coulomb_peak(bounds=bounds, p0=p0) 
    print(f">>> Opimised Params for peak @ {vc} V: alpha_gate = {params['alpha']:.2f} meV/V, Gmax = {params['Gmax']:.2e} S, Peak position: {params['Vc']:.3f} Vg")  # print the optimised parameters
    params["T"] = T 
    vg = zbgt["Vg"].values  
    fitGsd = physics_models.thermal_broadening(vg, **params)  # use the optimised parameters and the gate voltage array to generate the Gsd fit values. First argument has to be Vg.
    gatetraceFit = zbgt.copy()
    gatetraceFit["Gsd"] = fitGsd
    # fit_dct[vc] = params
    
    try:
        # add the fitted gate trace to the list
        gatetraceFits.append(gatetraceFit)
    except:
        pass


gatetraceFitSum = zbgt.copy()
gatetraceFitSum["Gsd"] -= gatetraceFitSum["Gsd"].values  

for fit in gatetraceFits:  
    gatetraceFitSum["Gsd"] += fit["Gsd"].values  

gatetraceFitSum.ps(color="black", label="sum of fits", linewidth=2)  

fig = Figure()
fig.add_subplot(Subplot_GVg(zbgt, title=f"zbgt_{round(T,2)}_K", cmap='plasma')) # plot gatetrace
fig.add_subplot(Subplot_GVg(zbgt, *gatetraceFits, gatetraceFitSum, legend=True))  
fig.visualise(f"{fig_dir}/fit_gatetrace_{int(T)}_K")


a = [[round(T,2)], vcs]
a # this will be used as multiindex
index = pd.MultiIndex.from_product(a, names=['temperature', 'peak_vg'])
a = pd.DataFrame(np, index=index, columns=['T', 'Vc', 'Gmax', 'alpha'])


n_fit_params, n_vg_peak = len(params), len(vcs)
parm_mat = np.zeros((n_fit_params,n_vg_peak)) # np.zeros((n_fit_params, n_vg_peak))
f_ax, s_ax = parm_mat.shape
parm_mat[0] = params['Vc']
parm_mat[1] = params['Gmax']
parm_mat[2] = params['alpha']
parm_mat.shape



b = pd.DataFrame(parm_mat.T, index=index, columns=['Vc', 'Gmax', 'alpha', 'T'])
b


d = {}
for row_key in range(5):
    d[row_key] = {}
    for idx, col in enumerate(vcs):
        d[row_key][col] = params
d






