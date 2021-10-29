import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
import glob, os
import time as t

#functions-----------------------------------------------------------

def fits_open(filename):
    with fits.open(filename, memmap=False) as f:
        f.verify('silentfix')
        data = []
        ants = f[1].data[0]["AMP_RCP"] + f[1].data[0]["AMP_LCP"]
        freq = f[1].data[0]["FREQUENCY"]
        time = f[1].data[0]["TIME"]
        ants = np.reshape(ants, (20, 128))
        for i in range(20):
            data.append(ants[i, :])

    return(data, freq, time)

#---------------------------------------------------------------------

filenames = glob.glob('/mnt/badary/SRH/SRH0306/20210603/*.fit')
filenames = sorted(filenames, key=os.path.basename)

date = filenames[0].split('/')[-1][4:-11]
print(date)

print(len(filenames))

#------------------------------------------------------------------------------

ramp = []
lamps = []
ants = []
time = []

#------------------------------------------------------------------------------

t1 = t.time()
for filename in filenames:

    ants, freq, time20 = fits_open(filename)
    time.append(time20)


ants = np.swapaxes(np.array(ants), 0, 1)
time = np.reshape(np.array(time), (len(filenames) * 20 ))

print(f'Time = {t.time() - t1} ')


i = 1
textsize = 16

for ant in ants:
    # ant = ant / np.average(ant)
    # ant = ant / np.max(ant)
    # dant = np.diff(ant)
    plt.plot(time, ant, label = f"antenna #{i}")
    # plt.plot(time[:-1], dant, label = f"antenna #{i}")
    # plt.scatter(time[:-2], dant, label = f"antenna #{i}")
    i += 1

    plt.title(f"RPC+LPC {date}, freq = {freq} MHz", size = textsize)
    # plt.legend()
    plt.tight_layout()
    plt.savefig(f'./{date}-antenna #{i}.png', transparent=False, dpi=500, bbox_inches="tight")

#------------------------------------------------------------------------------



'''
#freqs = [data[i][0] for i in range(len(data))]

data = f[1].data[0]["AMP_RCP"]

freq = data["FREQUENCY"]

ramps = data["AMP_RCP"]
lamps = data["AMP_LCP"]
'''


'''
for key in f[1].header:
print(f"{key} - {f[1].header[key]}")
print("***")
'''
