import os
import numpy as np
from imports.qtlab_data import *
from imports.dataclass import *
from matplotlib.colors import to_rgba
from matplotlib.colors import LinearSegmentedColormap


def correct_path_format(path: str):
    """
    Paste the path you copy from windows into this function. It replace the single backslash with the double.
    Needs an r in from of the string.
    """
    lpath = path.split('\\')
    return '\\'.join(lpath)


def find():
    dat_dir = correct_path_format(
        r'C:\Users\oums1095\projects\gnr_set\data\5.Temperature_Dataset\copy_justSD_Aug')
    os.chdir(dat_dir)
    # find the data
    dset = QTLab_Dataset.find()
    return dset


def load():
    dset = find()
    data = dset[-3].load(Stability_Diagram,
                         axes=("Vg", "T", "Vsd", "Isd", "t"))
    sd = data[0]  # the SD is a pandas dataframe that is the first item
    T = sd['T'].values.mean()  # sd is a Pandas df so retrieve the numpy object
    print(f">>Stability diagram measure at {round(T,2)} K")
    sd["Vsd"] *= 1e-3  # the methods want to work in V and not mV
    sd.resample(256, 256)
    sd.correct_offset()  # subtract a (quasi)-zero-bias gate trace
    zbgt = sd.zero_bias_gate_trace()  # gatetrace is stil a Stability_Diagram Object
    return sd, zbgt, T


def plot(sd, zbgt, T, save=False, name='prova/adesso'):
    fig_dir = correct_path_format(
        r"C:\Users\oums1095\projects\gnr_set\figures\fit_zbt")
    fig = Figure()
    # fig.add_subplot(Subplot_IVsVg(
    #     sd, title=f"sd_{round(T,2)}_K", cmap='plasma'))  # plot SD
    # plot conductance SD
    fig.add_subplot(Subplot_GVsVg(
        sd, title=f"sd_{round(T,2)}_K", cmap="plasma"))
    # plot gatetrace
    fig.add_subplot(Subplot_GVg(
        zbgt, title=f"zbgt_{round(T,2)}_K", cmap='plasma'))
    if save:
        os.chdir(fig_dir)
        fig.visualise(name)


def main():
    # find()
    sd, zbgt, T = load()
    plot(sd, zbgt, T, save=True, name='diocane/nonfunziona')


if __name__ == '__main__':
    main()
