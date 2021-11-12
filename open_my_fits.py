from astropy.io import fits
from astropy.table import Table
import numpy as np
import matplotlib.pyplot as plt
import os, glob



filenames = glob.glob('./20210603/*.fits')
filenames = sorted(filenames, key=os.path.basename)

with fits.open(filenames[0], memmap = True) as f:
    f.verify('silentfix')
    f.info()
    data = f[1].data["DATA"]

print(data)

with fits.open(filenames[1], memmap = True) as f:
    f.verify('silentfix')
    f.info()
    time = f[1].data["TIME"]

for ant in data:
    plt.plot(time, ant)

plt.show()
