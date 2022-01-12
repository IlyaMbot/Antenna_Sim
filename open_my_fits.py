from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt
import os, glob, antlib
import time as t

plt.rcParams.update({'figure.max_open_warning': 0})

# filenames = glob.glob('./data/*0.fits')
filenames = glob.glob('./data/202108/*0.fits')
filenames = sorted(filenames, key=os.path.basename)


freq = 5.6
foldname = 'integral_profiles56'

#------------------------------------------------------------------------------

l = 1

all_datas = []
all_times = []

for filename in filenames:
    date = filename.split('/')[-1][0:8]
    print(date)

    with fits.open(filename, memmap = True) as f:
        f.verify('silentfix')
        all_times.append(f[0].data[0])
        all_datas.append(f[0].data)

for l in range(1,129):
    avers = []
    time_r = np.arange(10, 36300, 5)

    t1 = t.time()

    for i in range(len(all_datas)):

        a = antlib.make_regulare(all_datas[i][l], all_times[i], time_r)
        avers.append(np.array(a))

    avers = np.array(avers)
    aver = np.sum(avers, axis = 0)
    aver = antlib.remove_out_of_phase(aver, 0.01)[0]

    antlib.makedir(foldname)

    textsize = 16
    plt.figure()

    view = 0

    if view == 0:

        plt.plot(time_r[:-1], aver)
        plt.ylim(0, 2 * np.mean(aver))

        plt.title(f"RPC+LPC {date}, freq = {freq} MHz, antenna = {l}", size = textsize)
        plt.xlabel("Time, s", size = 16)
        plt.ylabel("Flux, [average val.]", size = 16)
        plt.tight_layout()
        plt.savefig(f'./{foldname}/antenna_{l}.png', transparent=False, dpi=300, bbox_inches="tight")

    elif view == 1:
        for i in range(len(avers)):
            plt.plot(time_r[:-1], avers[i]/ np.mean(avers[i]), color = 'blue')
        plt.plot(time_r[:-1], aver, color = 'red', linewidth = 5)
        plt.ylim(0, 2 * np.mean(aver))

        plt.title(f"RPC+LPC {date}, freq = {freq} MHz, antenna = {l}", size = textsize)
        plt.xlabel("Time, s", size = 16)
        plt.ylabel("Flux, [average val.]", size = 16)
        plt.tight_layout()
        plt.savefig(f'./{foldname}/antenna_{l}_all_days.png', transparent=False, dpi=300, bbox_inches="tight")

    print(f'one ant = {t.time() - t1}')