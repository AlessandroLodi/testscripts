import os
import numpy as np
from imports.dataclass import *
from imports.qtlab_data import *
from matplotlib.colors import to_rgba
try: from imports.simmons import simmons
except:
    from imports.physics_models_p import *
    simmons = physics_models.simmons

# configuration
folder_electroburn = 'eburn'
folder_molps = 'mol spinvalvekeith'

chipPiece = 'TR'
# subfolders and pattern matching on the files
match = '{}|{}'.format(folder_molps, folder_electroburn)
pattern = '.*?(?P<folder>{}).*?\d+_(?P<exp>[a-zA-Z0-9_]+)_(?P<type>[a-zA-Z0-9\-_]+?)_(?P<device>[a-zA-Z]+[0-9]+)\.(?:dat|csv|txt)'.format(match)
os.chdir(r'E:\2020\AL_LG01')


# find all QTLab files in the folder and sort them newer to the front
dset = QTLab_Dataset.find(pattern=pattern)
dset = dset[np.argsort(dset['timestamp'])[::-1]]

print(dset)

# select only the burn and IV data
# burnset = dset[dset['type'] == 'burn']
# burnset = burnset[burnset['folder'] == folder_electroburn]
# ivset = dset[dset['type'] == 'IV']
ivsvgset = dset[dset['type'] == 'IVsVg']
# ivsvgset_post = ivsvgset[ivsvgset['folder'] == folder_chippiece]
# ivsvgset_pre = ivsvgset[ivsvgset['folder'] == folder_electroburn]

ivsvgset = dset[dset['type'] == 'IVsVg']
# ivsvgset_avg = dset[dset['type'] == 'IVsVg-avg']
# print(ivsvgset)
ivsvgset_post = ivsvgset[ivsvgset['folder'] == folder_molps]
ivsvgset_pre = ivsvgset[ivsvgset['folder'] == folder_electroburn]
# loop over the devices
devices = np.unique(ivsvgset_post['device'])
print(devices)
avgG_prearray =  []
avgG_postarray = []
finalDevs = []
for dev in devices:
    devset = ivsvgset_pre[ivsvgset_pre['device']==dev]
    if not devset: continue
    dat = devset.load(QTLab_Data)[0]
    stab = devset.load(Stability_Diagram)

    if not dat: continue
    dat.axes = ('Vsd','Vg','n','Isd')
    Vsd = dat['Vsd'].values
    Vg = dat['Vg'].values
    Isd = 1e9*dat['Isd'].values
    G = Isd[np.abs(Isd>0.000001)]/Vsd[np.abs(Isd>0.000001)]
    avgG_pre = np.sum(np.sqrt(np.power(G,2)))/len(G)

    devset = ivsvgset_post[ivsvgset_post['device']==dev]
    if not devset: continue
    dat = devset.load(QTLab_Data)[0]
    if not dat: continue
    dat.axes = ('Vsd','Vg','n','Isd')
    Vsd = dat['Vsd'].values
    Vg = dat['Vg'].values
    Isd = 1e9*dat['Isd'].values
    G = Isd[np.abs(Isd>0.000001)]/Vsd[np.abs(Isd>0.000001)]
    avgG_post = np.sum(np.sqrt(np.power(G,2)))/len(G)
    avgG_postarray.append(avgG_post)
    avgG_prearray.append(avgG_pre)
    finalDevs.append(dev)
d = {'device':finalDevs, 'G_post':avgG_postarray, 'G_pre':avgG_prearray}
df = pd.DataFrame(data=d)
print(df)
# df.to_csv('Dataplotoutput.csv', index=False)
# max = 10*max(np.median(avgG_postarray),np.median(avgG_prearray))
max = 200
print(max)
x = np.arange(0,max)
y = x
fig,ax = plt.subplots(figsize=(6,4))
ax.scatter(avgG_prearray, avgG_postarray)
ax.plot(x,y, lineStyle = ':')
ax.set_xlabel('RMS conductance before molecular deposition (nS)')
ax.set_ylabel('RMS conductance after molecular deposition (nS)')
ax.set_xlim([-2,max])
ax.set_ylim([-2, max])
ratios = []
numLower = 0
numHigher = 0
bondedDevices = ('a7','a14','a16','a27','a28','b8','b25','c12','c21','c23','c31','d3','d7','d31','d33','e17','f23','f32','g4','g10','g14','h23','i6','i7','i16','i17','i20','i35','j8','j15','j17','j21','j23','j29','j36','j37','j38','k1','k2','k20','m7','m11','m14','m23','m26','n9','n10','n16','n23','n34','n35','o4','o6','o27','p1','p6','p34','p38','q3','q5','q12','q13','q20','q28','r32','r37','s31','t14','t21','t36','u12','v11','v22','w9','w16')
devicesOfInterest = ('c31','f32','g14','h23','i17','i20','i35','j8','j17','j21','k20','p34','q20','q28','r37','t21','t36','v22','w9')
QDdevice = ('c31','f32','g14','h23','i17','i20','i35','j8','j17','j21','k20','p34','q20','q28','r37','t21','t36','v22','w9')
for index,row in df.iterrows():#
    try:
        # if row['device'] in bondedDevices:
        #     markerColor = 'y'
        #     ax.scatter(row['G_pre'], row['G_post'], color=markerColor)
        #     numHigher += 1
        if row['G_pre'] > row['G_post']:
            markerColor = 'r'
            ax.scatter(row['G_pre'], row['G_post'], color=markerColor)
            numLower +=1
        else:
            markerColor = 'b'
            ax.scatter(row['G_pre'], row['G_post'], color=markerColor)
            numHigher += 1
            # ax.annotate(row['device'], (row['G_pre'], row['G_post']))
        ratio = row['G_post']/row['G_pre']
        if ratio < 50:
            ratios.append(ratio)
    except:
        pass
# plt.hist(ratios, bins=80)
# plt.show()
# raise SystemExit

print(numLower)
plt.annotate(numLower, (max, 0.5*max), fontsize = 12, color = 'r')
plt.annotate(numHigher, (0.5*max, max), fontsize = 12, color = 'b')
plt.suptitle('TbDy dimer, 3$\mu$M in toluene')
print(numHigher)
plt.show()