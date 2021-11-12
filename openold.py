import numpy as np
import matplotlib.pyplot as plt
import glob, os, antlib
import time as t

#functions---------------------------------------------------------------------



#paths-------------------------------------------------------------------------

# on server
# filenames = glob.glob('/mnt/badary/SRH/SRH0306/20210603/*.fit')

# on PC
filenames = glob.glob('./dataold/20210603/*.fit')
# filenames = glob.glob('./data/20210801/*.fit')

filenames = sorted(filenames, key=os.path.basename)

date = filenames[0].split('/')[-1][4:-11]
print(date)

#------------------------------------------------------------------------------

ants = []
time = []

#------------------------------------------------------------------------------

for filename in filenames:

    ants20, freq, time20 = antlib.get_data_for_freq(filename)
    time.append(time20)
    ants.append(ants20)

ants = np.reshape(ants ,(len(filenames) * 20, 128))

ants = np.swapaxes(np.array(ants), 0, 1)
time = np.reshape(np.array(time), (len(filenames) * 20 ))


k=0
for i in range(len(ants)):
    ants[i] = antlib.remove_out_of_phase(ants[i], 0.1)

antlib.save_fits_flux(ants, date, foldname = f"{date}")
antlib.save_fits_time(time, date, foldname = f"{date}")


#plotting----------------------------------------------------------------------

'''
textsize = 16

plt.figure()

# plt.scatter(time, ants)
plt.plot(time, ant)
plt.title(f"RPC+LPC {date}, freq = {freq / 10 ** 6} MHz, antenna = {k}", size = textsize)

# plt.title(f"Integral flux RPC+LPC {date}, freq = {freq / 10 ** 6} MHz", size = textsize)
plt.tight_layout()
plt.axis([time[0] - 500, time[-1] + 500, 0, np.max(ant) * 1.1 ])
# plt.savefig(f'./pictures/{date}-antenna #{k}.png', transparent=False, dpi=100, bbox_inches="tight")
# plt.savefig(f'./pictures/{date}-inegral.png', transparent=False, dpi=500, bbox_inches="tight")
plt.show()
'''
