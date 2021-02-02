import os
import numpy as np
from imports.dataclass import *
from imports.qtlab_data import *
from matplotlib.colors import to_rgba

# configuration
experiment='TL_300_5'
folder_electroburn = 'eburn'
folder_chippiece = ''

# subfolders and pattern matching on the files
match = '{}|{}'.format(folder_chippiece, folder_electroburn) if folder_chippiece else folder_electroburn
if not folder_electroburn: match = folder_chippiece
pattern = '.*?(?P<folder>{}).*?\d+_(?P<exp>[a-zA-Z0-9_]+)_(?P<type>[a-zA-Z0-9\-_]+?)_(?P<device>[a-zA-Z]+[0-9]+)\.(?:dat|csv|txt)'.format(match)

#change the directory to point to your data

os.chdir(r'C:\Users\Inst\Desktop\probestationdata\{}'.format(experiment))
#os.chdir(r'C:\Bart\{}'.format(experiment))
# clear the output file
with open('output{}.csv'.format(folder_chippiece), 'w') as f:
    f.write('\t'.join(['dev','A','phi','alpha','d','R2','Resistance','Max Breakpoint V'])+'\n')

# find all QTLab files in the folder and sort them newer to the front
dset = QTLab_Dataset.find(pattern=pattern)
dset = dset[np.argsort(dset['timestamp'])[::-1]]


# select only the burn and IV data
if folder_electroburn:
    burnset = dset[dset['type'] == 'burn']
    burnset = burnset[burnset['folder'] == folder_electroburn]
ivset = dset[dset['type'] == 'iv']
ivgset = dset[dset['type'] == 'IVg']
ivsvgset = dset[dset['type'] == 'IVsVg']
print(ivset)
print(ivgset) #new
print(ivsvgset) #new
if folder_chippiece:
    ivset = ivset[ivset['folder'] == folder_chippiece]
else:
    ivset = ivset[ivset['folder'] == folder_electroburn]

# loop over the devices
devices = np.unique(ivset['device'])
for dev in devices:
    fig = Figure()
    # select the device from the burn data, correct the axes (n is given as a second axis) and plot the burndata
    if folder_electroburn:
        # except: data = None
        # if not data or not data[0]: continue
        # data[1]['Vg']*=12.5
        # fig.add_subplot(Subplot_IVsVg(data[1], title='Before eburn'))
        devset = burnset[burnset['device']==dev]
        if not devset: continue
        dat = devset.load(QTLab_Data)[0]
        if not dat: continue
        dat.axes = ('Vsd','Isd','n')
        v = np.max(dat['Vsd'].values)
        fig.add_subplot(Subplot_IV(dat)) #new
    else:
        v = 0

    # select the device from the IV data and load (the newest is entry [0] because we sorted by timestamp reversed
    devset = ivset[ivset['device']==dev]
    dat = devset.load(QTLab_Data)[0]
    print(dat)
    dat['Isd']*=1e9  # set the current to nA because computers don't like 1e-9 values, this is corrected on the subplot by the scale_factor_y=1e-9 kwarg
    #avg = QTLab_Data.average_cycles(dat)  # average the cycles in the IV trace and save on a different variable
    #avg.cycle_to_trace()  # also flatten the averaged cycles
    print(dat)
    #print(avg)

    # fit the IV trace to a simple exponential first
    params,r2,fit = dat.fit(
        lambda x,a,b,c: a*(np.exp(b*x)-np.exp(c*x)),
        p0=(1,1,0.5),)
    fit.plot_settings(linewidth=1,color='grey',label='exponential fit')
    print('>> Exponential fit ({:.2g},{:.2g},{:.2g}) R^2: {:.2g}'.format(*params,r2))
    if r2 > 0.95:
        # get the zero bias resistance from the exponential fit
        a,b,c = params
        a/=1e9
        r = 1/(a*b-a*c)
        # perform a simmons fit on a smaller portion of the averaged data (20 points is sufficient)
        params, r2, fit = dat.fit(
            physics_models.simmons,
            p0 = {'A': 4.226, 'phi': 0.107, 'alpha': 0.2, 'd': 1.5},
            bounds = {
                'A': [-1,10],
                'phi': [0, 3],
                'alpha': [-1,1],
                'd': [0, 4],
            }
        )
        print('>> Simmons fit ({:.2g},{:.2g},{:.2g},{:.2g}) R^2: {:.2g}'.format(*params,r2))
        fit.plot_settings(linewidth=1,color='black',label='Simmons fit')
    else:
        params = [0 for _ in range(len(params)+1)]
        r2 = 0

    # get the resistance of the junction by a linear fit of the IV trace
    try:
        a, b = np.polyfit(dat['Vsd'].values, dat['Isd'].values / 1e9, 1)
        r = abs(1 / a)
    except:
        r = 0
    # set the plot settings for the data and add a subplot
    dat.plot_settings(linewidth=0.5, color=to_rgba('C0', 0.6), label='raw data')
    #avg.plot_settings(linewidth=1, color='C1', label='averaged data')
    fig.add_subplot(Subplot_IV(dat,fit,legend=True,scale_factor_y=1e-9)) # new
    d = ivsvgset[ivsvgset['device'] == dev]  # new
    try:
        data = d.load(Stability_Diagram)
    except:
        data = None
    if not data or not data[0]: continue
    data[0]['Vg'] *= 12.5
    fig.add_subplot(Subplot_IVsVg(data[0], title='After eburn'))
    print('>> Plotting device {}'.format(dev))
    if folder_chippiece:
        fig.visualise('figures/{}/{}_{}.png'.format(folder_chippiece, experiment, dev))
    else:
        fig.visualise('figures/{}_{}.png'.format(experiment, dev))

    # save values to an output file:
    with open('output{}.csv'.format(folder_chippiece), 'a') as f:
        f.write('\t'.join(list(map(str,[dev, *params, r2, r, v])))+'\n')

