import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
import glob, os
import time as t

# on server
# filenames = glob.glob('/mnt/badary/SRH/SRH0306/20210603/*.fit')

# on PC
filenames = glob.glob('./dataold/20210603/*.fit')


filenames = sorted(filenames, key=os.path.basename)

date = filenames[0].split('/')[3][4:-11]
print(date)
t1 = t.time()
#------------------------------------------------------------------------------

ramp = []
lamps = []
ants = []
time = []

#------------------------------------------------------------------------------

for filename in filenames:
    f = fits.open(filename)
    f.verify('silentfix')
     
    data = f[1].data[0]["AMP_RCP"] + f[1].data[0]["AMP_LCP"] 
    freq = f[1].data[0]["FREQUENCY"]
    time.append(f[1].data[0]["TIME"])
        
    data = np.reshape(data, (20, 128))
    for i in range(20):
        ants.append(data[i, :])
    f.close()
        

ants = np.swapaxes(np.array(ants), 0, 1)
time = np.reshape(np.array(time), ( len(filenames) * 20 ))

i = 1
for ant in ants[:20]:
    # ant = ant / np.average(ant)
    # ant = ant / np.max(ant)
    # dant = np.diff(ant)
    plt.plot(time, ant, label = f"antenna #{i}")
    # plt.plot(time[:-1], dant, label = f"antenna #{i}")
    # plt.scatter(time[:-2], dant, label = f"antenna #{i}")
    i += 1

print(f'time = {t.time - t1}')
textsize = 16
    
plt.title(f"RPC+LPC {date}, freq = {freq} MHz", size = textsize)
# plt.legend()
plt.show()

#------------------------------------------------------------------------------


'''
for key in f[0].header:
    print(f"{key} - {f[0].header[key]}")
print("***")
'''
'''
#freqs = [data[i][0] for i in range(len(data))]

data = f[1].data[0]["AMP_RCP"]

freq = data["FREQUENCY"]

ramps = data["AMP_RCP"]
lamps = data["AMP_LCP"]
'''
