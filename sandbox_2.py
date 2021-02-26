# import os
# import numpy as numpy
# import matplotlib.pyplot as plt
# import string
# from imports.qtlab_data import *
# from imports.dataclass import *
# from imports.physics_models import *
# from helper_functions import *
# from matplotlib.colors import to_rgba


# # Change dir and import dataset
# os.chdir(r"G:\2021\AG_LG06_6\mol gnr_dil1to100_1phenyloctane\AG_LG06_6_IVsVg\20210118")
# vsd = 0.4
# dset = QTLab_Dataset.find()
# actual_data = dset[dset["type"] == "IVsVg"][-18].load(Stability_Diagram)
# actual_data = actual_data[0]
# actual_data.resample(256, 256)
# gt_single = actual_data.gatetrace(vs=vsd).shift_gatetrace()
# for att in dir(gt_single):
#     print(att, getattr(gt_single, att))
# fig = Figure()
# fig.add_subplot(Subplot_IVg(gt_single))
# fig.visualise(f"gt_rolled.png")


from datetime import date, timedelta

year = 2021
date_object = date(year, 1, 1)
date_object += timedelta(days=1 - date_object.isoweekday())

while date_object.year == year:
    print(date_object)
    date_object += timedelta(days=7)


# %%
