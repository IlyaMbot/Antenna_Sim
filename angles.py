from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt
import os, glob, antlib
import time as t


filenames = glob.glob('./aver*/*.fits')
filenames = sorted(filenames, key=os.path.basename)

for filename in filenames:
    
    time = []
    data = []

    with fits.open(filename, memmap = True) as f:
            f.verify('silentfix')
            time.append(f[0].data[0])
            data.append(f[0].data[1])
    
    time = np.array(time[0])
    data = np.array(data)
    print(time.shape , data.shape )
    antlib.simple_plot(time, data, showall = False)