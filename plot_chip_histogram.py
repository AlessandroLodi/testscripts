import os
import numpy as np
from imports.dataclass import *
from imports.qtlab_data import *
from matplotlib.colors import to_rgba

# configuration
experiments = ["20190802", "20190806"]
folder_electroburn = ""
fig = Figure()
for experiment in experiments:
    # subfolders and pattern matching on the files
    # pattern = '.*?(?P<folder>{})\\.*?\d+_(?P<exp>[a-zA-Z0-9_]+)_(?P<type>[a-zA-Z0-9\-_]+?)_(?P<device>[a-zA-Z]+[0-9]+)\.(?:dat|csv|txt)'.format(folder_electroburn)
    pattern = "(?P<folder>.*)\\\d+_(?P<chip>[a-zA-Z0-9_]+)_(?P<device>[a-zA-Z0-9\-_]+?).*?_(?P<exp>[a-zA-Z]+).*?\.corrected\.(?:dat|csv|txt)".format(
        folder_electroburn
    )
    os.chdir(r"C:\\cygwin64\\home\\oums1095\\{}".format(experiment))

    # find all QTLab files in the folder and sort them newer to the front
    dset = QTLab_Dataset.find(pattern=pattern)
    dset = dset[np.argsort(dset["timestamp"])[::-1]]

    # select only the burn and IV data
    burnset = dset[dset["type"] == "burn"]

    # loop over the devices
    devices = np.unique(burnset["device"])
    v = []
    i = []
    for dev in devices:
        # select the device from the burn data, correct the axes (n is given as a second axis) and plot the burndata
        devset = burnset[burnset["device"] == dev]
        if not devset:
            continue
        dat = devset.load(QTLab_Data, axes=("Vsd", "n", "Isd"))[0]
        if not dat:
            continue
        dat.axes = ("Vsd", "Isd", "n")
        v.append(np.max(dat["Vsd"].values))
        i.append(np.max(dat["Isd"].values))
    dat = Data({"Vsd": np.array(v), "Isd": np.array(i)}, axes=("Vsd", "Isd"))
    fig.add_subplot(
        Subplot(
            dat,
            type="hist2d",
            bins=(np.linspace(0, 10.0, 50), np.linspace(0, 0.001, 50)),
            axis_labels=("$V_{max}$ (V)", "$I_{max}$ ({metric_prefix}A)"),
            title=experiment,
        )
    )
os.chdir(r"C:\Users\oums1095\Desktop")
fig.visualise("hists.png")

