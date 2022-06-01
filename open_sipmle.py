from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt
import os, glob, antlib
import time as t

filenames = glob.glob('./data/202108/*.fits')
filenames = sorted(filenames, key=os.path.basename)

data = np.array([])

for filename in filenames:
    date = filename.split('/')[-1][0:8]
    print(date)

    with fits.open(filename, memmap = True) as f:
        f.verify('silentfix')
        data = f[0].data

time = data[0]
diff = np.average( np.diff(time) )

print(diff)