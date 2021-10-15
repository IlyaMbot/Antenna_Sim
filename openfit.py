import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
import glob, os


filenames = glob.glob('/home/conpucter/GitHub/try/DataSRH/2021/07/*.fit')
filenames = sorted(filenames, key=os.path.basename)

date = filenames[0][-19:-11]

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
        
    data = np.reshape(data, (20, 48))
    for i in range(20):
        ants.append(data[i, :])
        

ants = np.swapaxes(np.array(ants), 0, 1)

time = np.reshape(np.array(time), (3760))

i = 1
for ant in ants[:20]:
    #ant = ant / np.average(ant)
    dant = abs(np.diff(ant))
    plt.plot(time, ant, label = f"antenna #{i}")
#    plt.scatter(time[:-1], dant, label = f"antenna #{i}")
    i += 1
    
plt.title(f"RPC {date}, freq = {freq}")
#plt.legend()
plt.show()

#------------------------------------------------------------------------------

'''
for key in f[0].header:
    print(f"{key} - {f[0].header[key]}")
print("***")
'''

#freqs = [data[i][0] for i in range(len(data))]

data = f[1].data[0]["AMP_RCP"]

freq = data["FREQUENCY"]

ramps = data["AMP_RCP"]
lamps = data["AMP_LCP"]

