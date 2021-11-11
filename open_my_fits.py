from astropy.io import fits
from astropy.table import Table
import numpy as np
import matplotlib.pyplot as plt


with fits.open('test.fits', memmap = True) as f:
    f.verify('silentfix')
    f.info()
    data = f[1].data["DATA"]
    time = f[1].data["TIME"]
    weights = f[1].data["WEIGHTS"]

# data = data * weights

plt.plot(time, data)
plt.show()
