import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
import glob, os
import time as t

folders = glob.glob('./data/202108*')
folders = sorted(folders, key=os.path.basename)

for folder in folders[1:2]:
    t1 = t.time()

    filenames = glob.glob(folder + '/*.fit')
    filenames = sorted(filenames, key=os.path.basename)

#------------------------------------------------------------------------------

    ramps = []
    lamps = []
    ants = []
    time = []

#------------------------------------------------------------------------------

    for filename in filenames[0:1]:
        f = fits.open(filename)
        f.verify('silentfix')
        f.info()

        date = f[0].header["date-obs"]
        # data = f[1].data[0]["AMP_RCP"] + f[1].data[0]["AMP_LCP"]

        ants.append(f[1].data[0]["AMP_RCP"] + f[1].data[0]["AMP_LCP"])

        freq = f[1].data[0]["FREQUENCY"]
        time.append(f[1].data[0]["TIME"])


    ants = np.array(ants)
    ants = np.reshape(ants, (20 * len(filenames), 128))

    time = np.reshape(np.array(time), ( len(filenames) * 20 ))

    t2 = t.time()
    print(t2-t1)

    i = 50

    # ant = ant / np.average(ant)
    # ants[i] = ants[i] / np.max(ant)
    # dant = np.diff(ant)
    plt.plot(time, ants[:,i], label = f"antenna #{i}")
    # plt.plot(time[:-1], dant, label = f"antenna #{i}")
    # plt.scatter(time[:-2], dant, label = f"antenna #{i}")

textsize = 16

plt.title(f"RPC+LPC {date}, freq = {freq} Hz, Ant#{i}", size = textsize)
# plt.legend()
plt.show()
