import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
import glob, os, antlib
import time as t

#functions---------------------------------------------------------------------



#paths-------------------------------------------------------------------------
# on server
# filenames = glob.glob('/mnt/badary/SRH/SRH0306/20210603/*.fit')

# on PC
# filenames = glob.glob('./dataold/20210603/*.fit')

filenames = glob.glob('./data/20210801/*.fit')
filenames = sorted(filenames, key=os.path.basename)

date = filenames[0].split('/')[-1][4:-11]
print(date)


#------------------------------------------------------------------------------

ants = []
time = []

#------------------------------------------------------------------------------

t1 = t.time()
for filename in filenames:

    ants20, freq, time20 = antlib.get_data_for_freq(filename)
    time.append(time20)
    ants.append(ants20)
    
ants = np.reshape(ants ,(len(filenames) * 20, 128)) 

ants = np.swapaxes(np.array(ants), 0, 1)
time = np.reshape(np.array(time), (len(filenames) * 20 ))

print(f'Time = {t.time() - t1}')

#plotting----------------------------------------------------------------------


textsize = 16

ants = np.sum(ants, 0)
dants = np.diff(ants)

stops = np.argwhere( abs(dants) >= np.max(abs(dants)) * 0.9 )
stops = np.reshape( stops , (len(stops))) 

for i in range(len(stops) - 1):
    ants[stops[i] + 1 : stops[i + 1] + 1 ] -= ants[stops[i] + 1] - ants[stops[i]] 
    
ants = ants / np.max(ants)

plt.figure()

# plt.scatter(time, ants)
plt.plot(time, ants)
plt.title(f"Integral flux RPC+LPC {date}, freq = {freq / 10 ** 6} MHz", size = textsize)
plt.tight_layout()
plt.axis([time[0] - 500, time[-1] + 500, 0, 1.1 ])
plt.savefig(f'./pictures/{date}-inegral.png', transparent=False, dpi=500, bbox_inches="tight")
plt.show()


'''
for ant in ants:
    t1 = t.time()
    
    # ant = ant / np.average(ant)
    # ant = ant / np.max(ant)
    # dant = np.diff(ant)
    # dant = dant / np.max(dant)
    plt.figure()
    plt.plot( time, ant, label = f"antenna #{i}" )
    # plt.plot( time[:-1], dant, label = f"antenna #{i}" )
    # plt.scatter(time[:-2], dant, label = f"antenna #{i}")
    i += 1

    plt.title(f"RPC+LPC {date}, freq = {freq / 10 ** 6} MHz, antenna = {i}", size = textsize)
    # plt.legend()
    plt.tight_layout()
    # plt.savefig(f'./pictures/{date}-antenna #{i}.png', transparent=False, dpi=100, bbox_inches="tight")
    plt.show()
    print(f'Time_saving = {t.time() - t1}')
'''