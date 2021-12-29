import numpy as np
from astropy.io import fits
import glob, os, antlib
import matplotlib.pyplot as plt

folders = glob.glob("./data/*")
folders = sorted(folders, key=os.path.basename)

for folder in folders[0:1]:

    filenames = glob.glob(folder + '/*.fit')
    filenames = sorted(filenames, key=os.path.basename)

    date = filenames[0].split('/')[-1][4:-11]
    print(date)

    #------------------------------------------------------------------------------

    ants = []
    time = []

    #------------------------------------------------------------------------------
    # REDO make this loop in get_data_for_freq
    for filename in filenames:
        frequency = 0
        with fits.open(filename, memmap = True) as f:
            f.verify('silentfix')
            corrs = f[1].data[frequency]["AMP_RCP"] + f[1].data[0]["AMP_LCP"]
            freq = f[1].data[frequency]["FREQUENCY"]
            time = f[1].data[frequency]["TIME"]
            corrs = np.reshape(corrs, (20, 128))

np.swapaxes(corrs, 0, 1)

l=0

textsize = 16

plt.figure()
for corr in corrs:
    plt.plot(corr)
plt.show()
