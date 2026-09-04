# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from IPython import get_ipython

# %% [markdown]
# ## Import Packages

# %%
import os
import numpy as np 
import pandas as pd
import matplotlib.pyplot as pp
get_ipython().run_line_magic('matplotlib', 'inline')

# %% [markdown]
# ## Customise Your Functions

# %%
os.chdir(r'G:\2021\AG_LG06_6\mol gnr_dil1to100_1phenyloctane\AG_LG06_6_IVsVg\20210118')
df_fom = pd.read_excel('SS_fit_results.xlsx', "Sheet1", index_col=None, na_values=["NA"], header=[0,1])


# %%
df_fom.dropna(how='all').head()


# %%
device_list = [dev.split('-')[-2] for dev in df_fom.iloc[:,0]]


# %%

device_list


# %%
df_fom.info()


# %%
df_fom['Intercept']   = df_fom['Intercept'].dropna()
df_fom['Slope'] = -(1e3*df_fom['Slope'].dropna()) # convert the slope in mV and take the positive value
df_fom['Statistics'] = df_fom['Statistics'].dropna()


# %%
df_fom['Slope'].value_counts()


# %%
slope


# %%
df_fom.describe()


# %%
# all the devices at all the bias voltages
df_fom.hist(bins="auto", figsize=(20,15))
pp.show()


# %%
from scipy.stats import binom

n, p = 8, 0.5
mean, var, skew, kurt = binom.stats(n, p, moments='mskv')
print(f" mean = {mean},\n var = {var},\n skew = {skew},\n kurt={kurt}")


# %%
vsd = [0.1, 0.2, 0.3, 0.4]

for i in range(len(vsd)):
    df_fom.iloc[i::4,:].hist(bins=12, figsize=(20,15))
    pp.savefig(f'SS_Fit_Histresult_GT_{vsd[i] * 1e3}mV.png')


# %%
slope = np.array([-0.30607 ,-0.52175 ,-0.51711 ,-0.45377 ,-0.47125 ,-0.35352 ,-0.42711 ,-0.47318 ,-0.39696 ,-0.4395 ,-0.45126 ,-0.49732 ,-0.47806 ,-0.45278 ,-0.40142 ,-0.44564 ,-0.41988 ,-0.48376
,-0.45291 ,-0.29475 ,-0.4117 ,-0.51662 ,-0.45152 ,-0.41858 ,-0.4902 ,-0.4413 ,-0.45296 ,-0.21459 ,-0.43368 ,-0.28086 ,-0.2455 ,-0.42196 ,-0.41667 ,-0.42149 ,-0.32103 ,-0.48186])
1 / slope 


# %%



# %%



# %%



# %%



# %%
import scipy.constants as sc

sc.hbar
sc.elementary_charge
#sc.reduced_Planck_constant_in_eV_s
sc.physical_constants['reduced Planck constant in eV s'][0]


# %%
vf  = 1e6 # ferm velocity of graphene [m/s]
Cg  = 1e-3 # Capacitive Coupling [690 aF/um^2 so I converted it]
DVg = 4.0 # [V]

delta_m = sc.physical_constants['reduced Planck constant in eV s'][0] * vf * (2 * np.pi * (Cg) * DVg / sc.elementary_charge) ** 1/2
delta_m_meV = delta_m * 1e-3
print(f'delta_m = {delta_m}, delta_m_meV = {delta_m_meV}')


# %%
from datetime import date, timedelta

d0 = date(2021, 4, 18)
d1 = date(2022, 3, 15)
delta = d1 - d0
print(delta.days / 7)


# %%
# Python's program to print all Monday's of a specific year
 
def allsundays(year):
   d = date(year, 1, 1)                    # January 1st
   d += timedelta(days = 6 - d.weekday())  # First Sunday
   while d.year == year:
      yield d
      d += timedelta(days = 7)

submission_date = date(2022, 3, 15)
for d in allsundays(2022):
    if d > date.today() and d < submission_date:
         print(f'******* {d} Begin ******')
         print(f'Weeks left to Submission = {np.round((submission_date - d).days / 7, decimals=0)}')
         print(29*'*'+'\n')
         print(f'******** {d} End *******\n')

# %% [markdown]
# # Plot Histogram Manually

# %%
slope_array = np.array([-0.15183,-0.38573 ,-0.46631 ,-0.37996 ,-0.39492 ,-0.31019 ,-0.3363 ,-0.38424 ,-0.32068 ,-0.4267 ,-0.38373 ,-0.4476 ,-0.42954 ,-0.41025 ,-0.36731 ,-0.39161 ,-0.36125 ,-0.41727 ,-0.42316 ,-0.26872 ,-0.37147 ,-0.41755 ,-0.38609 ,-0.34826 ,-0.39332 ,-0.39461 ,-0.36141 ,-0.10558 ,-0.36967 ,-0.25977 ,-0.25353 ,-0.38647 ,-0.35165 ,-0.3091 ,-0.22341 ,-0.39486])

inverse_array = np.power(-slope_array, -1)
inverse_array
max = np.max(inverse_array)
min = np.min(inverse_array)
print(f'Max inverse array = {max}\nMin inverse array = {min}')



# %%
vsd             = 0.5 # [V]. Bias at which the trace is take
device_name     = 'AG_LG06_6'

# bins = 'auto' uses the maximum of the Sturges and Freedman-Diaconis bin choice. You can read more about the options in the
pp.hist(inverse_array, bins='auto', histtype='stepfilled', color='r', alpha=0.5, label=r'Swing $V\,/dec$')
xlabel, ylabel = 5.8, 1.1 * max
pp.text(xlabel, ylabel, rf'max = {np.around(max, decimals=2)} $V\,/dec$' + "\n" + rf'min = {np.around(min, decimals=2)} $V\,/dec$')
pp.title(f"Subthreshold Swing, Vsd = {vsd} V, device {device_name}")
pp.xlabel("Value")
pp.ylabel("Occurance")
pp.legend()
pp.show()


# %%



# %%
max


# %%
