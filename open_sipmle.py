from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt
import os, glob, antlib
import time as t

filenames = glob.glob('./result_*/*.fits')
filenames = sorted(filenames, key=os.path.basename)

data = np.array([])

for filename in filenames:
    date = filename.split('/')[-1][0:8]
    print(date)

    with fits.open(filename, memmap = True) as f:
        f.verify('silentfix')
        data = f[0].data

time = data[0]
data = antlib.remove_out_of_phase(data[1:], 1)

data = np.sum(data, 0)

plt.figure()
plt.plot(time, data)
plt.show()
