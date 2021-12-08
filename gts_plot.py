import os
import numpy as np
import random
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


def correct_path_format(path: str):
    """
    Paste the path you copy from windows into this function. It replace the single backslash with the double.
    Needs an r in from of the string.
    """
    lpath = path.split('\\')
    return '\\'.join(lpath)


def extract_sd_temp(dset, resample_size=512, axes=("Vg", "T", "Vsd", "Isd", "t")):
    sd = dset.load(Stability_Diagram, axes=axes)
    sd = sd[0]
    sd["Vsd"] *= 1e-3
    T = round(sd['T'].values.mean(), 2)
    sd.resample(resample_size, resample_size)
    sd.correct_offset()
    return sd, T


def extract_zbgt(sd):
    return sd.zero_bias_gate_trace()  # gatetrace is stil a Stability_Diagram Object


def main():
    dat_dir = correct_path_format(
        r'C:\Users\oums1095\projects\gnr_set\data\5.Temperature_Dataset\copy_justSD_Aug')
    fig_dir = correct_path_format(
        r"C:\Users\oums1095\projects\gnr_set\figures\fit_zbt")
    dset = QTLab_Dataset.find(dat_dir)
    lst_sd = []
    lst_T = []
    lst_zbgt = []
    lst_gt1mv = []
    lst_gt2mv = []
    lst_gt10mv = []

    def plot_gt(gt, T, title='gt_1mv_resampled', path=r"C:\Users\oums1095\projects\gnr_set\figures"):
        fig_dir = correct_path_format(path)
        fig = Figure()
        fig.add_subplot(Subplot_GVg(gt, title=f'{title}_{int(T)}_K'))
        fig.visualise(f'{fig_dir}/{title}/{title}_{int(T)}_K')

    for i in dset:
        sd, T = extract_sd_temp(i)
        zbgt = extract_zbgt(sd)
        # vs here in mv, this bc the extract_sd_temp function converts everything in mv
        gt_1mv = sd.gatetrace(vs=1e-3)
        gt_2mv = sd.gatetrace(vs=2e-3)
        gt_10mv = sd.gatetrace(vs=1e-2)
        lst_sd.append(sd)
        lst_T.append(T)
        lst_zbgt.append(zbgt)
        lst_gt1mv.append(gt_1mv)
        lst_gt2mv.append(gt_2mv)
        lst_gt10mv.append(gt_10mv)
        plot_gt(gt_1mv, T)
        plot_gt(gt_2mv, T, title='gt_2mv_resampled')
        plot_gt(gt_10mv, T, title='gt_10mv_resampled')


if __name__ == '__main__':
    main()
