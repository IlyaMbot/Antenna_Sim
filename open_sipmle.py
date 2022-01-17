from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt
import os, glob, antlib
import time as t

filenames = glob.glob('./to_send/*.fits')
filenames = sorted(filenames, key=os.path.basename)


data = []

for filename in filenames:
    date = filename.split('/')[-1][0:8]
    print(date)

    with fits.open(filename, memmap = True) as f:
        f.verify('silentfix')
        data.append(f[0].data)

for d in data[:-1]:
    plt.plot(data[-1], d/ np.max(d))
plt.show()
