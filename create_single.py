import numpy as np
from astropy.io import fits
import glob, os, antlib
import matplotlib.pyplot as plt

filepath = "./data/20210603_flux_freq28.fits"
date = "20210603"

# arr = [2,4,5,6,7,8,9,10,19,20,23,28,30,33]
data = []

with fits.open(filepath) as f:
    f.verify('silentfix')
    time = f[0].data[0]
    data = f[0].data[1:]
    # for i in arr:
        # data.append( f[0].data[i])
data = np.array(data)

foldname =  'test_images'

antlib.makedir(foldname)

antlib.save_fits_raw(time, date, foldname = "to_send", add = "_t")

for i in range(len(data)):
    antlib.save_fits_raw(data[i], date, foldname = "to_send", add = f"_a{i}")

    # plt.figure()
    # plt.title(f'ant {i+1}')
    # plt.ylim(0,2)
    # plt.plot(time, data[i])
    # plt.savefig(f'./{foldname}/antenna_{i+1}.png', transparent=False, dpi=300, bbox_inches="tight")
    # plt.close()

# antlib.simple_plot(time, data, showall=True)
