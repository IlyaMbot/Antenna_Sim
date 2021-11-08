import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
import glob, os
import time as t

#functions---------------------------------------------------------------------

def print_keys(filename, i = 1):
    with fits.open(filename, memmap=True) as f:
        f.verify('silentfix')
        for key in f[i].header:
            print(f"{key} - {f[i].header[key]}")
            print("***")

def fits_open(filename):
    with fits.open(filename, memmap=True) as f:
        f.verify('silentfix')
        ants = f[1].data[0]["AMP_RCP"] + f[1].data[0]["AMP_LCP"]
        freq = f[1].data[0]["FREQUENCY"]
        time = f[1].data[0]["TIME"]
        ants = np.reshape(ants, (20, 128))

    return(ants, freq, time)

#paths-------------------------------------------------------------------------
# on server
# filenames = glob.glob('/mnt/badary/SRH/SRH0306/20210603/*.fit')

# on PC
filenames = glob.glob('./dataold/20210603/*.fit')
filenames = sorted(filenames, key=os.path.basename)

date = filenames[0].split('/')[-1][4:-11]
print(date)


#------------------------------------------------------------------------------

ants = []
time = []

#------------------------------------------------------------------------------

t1 = t.time()
for filename in filenames:

    ants20, freq, time20, obs = fits_open(filename)
    time.append(time20)
    ants.append(ants20)
    time_begin.append(obs)
    
ants = np.reshape(ants ,(len(filenames) * 20, 128)) 

ants = np.swapaxes(np.array(ants), 0, 1)
time = np.reshape(np.array(time), (len(filenames) * 20 ))

print(f'Time = {t.time() - t1}')

#plotting----------------------------------------------------------------------

i = 1
textsize = 16

for ant in ants[i:i+1]:
    t1 = t.time()
    
    # ant = ant / np.average(ant)
    # ant = ant / np.max(ant)
    dant = np.diff(ant)
    dant = dant / np.max(dant)
    print( time[ np.argwhere( dant > 0.5 ) ] )
    plt.figure()
    # plt.plot( time, ant, label = f"antenna #{i}" )
    plt.plot( time[:-1], dant, label = f"antenna #{i}" )
    # plt.scatter(time[:-2], dant, label = f"antenna #{i}")
    i += 1

    plt.title(f"RPC+LPC {date}, freq = {freq / 10 ** 6} MHz, antenna ={i}", size = textsize)
    # plt.legend()
    plt.tight_layout()
    # plt.savefig(f'./pictures/{date}-antenna #{i}.png', transparent=False, dpi=100, bbox_inches="tight")
    plt.show()
    print(f'Time_saving = {t.time() - t1}')

#------------------------------------------------------------------------------

'''
for key in f[1].header:
print(f"{key} - {f[1].header[key]}")
print("***")
'''
