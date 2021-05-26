


#%%
import os
import string
import numpy as np
from imports.qtlab_data import *
from imports.dataclass import *
from helper_functions import *

def plot_IV(**kwargs):


    for k,v in kwargs.items():
        print(f'key = {k}, value = {v}')  




plot_IV(path=r'I:\2021\Test_3T_Nanogap_chip_8', folder_1 = '1_rtest_gstest', folder_2 = '2_rtest_post_submersion_dil_1to10', dataset_type='R', )


# %%
