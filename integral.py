from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt
import os, glob, antlib
import time as t

plt.rcParams.update({'figure.max_open_warning': 0})

filenames = glob.glob('./data/*.fits')
#filenames = glob.glob('./myfits/202108*.fits')
filenames = sorted(filenames, key=os.path.basename)


freq = 2.8
foldname = 'integral_each_day'

#------------------------------------------------------------------------------

antlib.makedir(foldname)

for filename in filenames:
    date = filename.split('/')[-1][0:8]
    print(date)

    with fits.open(filename, memmap = True) as f:
        f.verify('silentfix')
        time = f[0].data[0]
        data = f[0].data[1:]

    #print(data.shape)
    #data = antlib.remove_out_of_phase(data, 0.1)
    #print(data.shape)
    
    result = np.sum(data, axis = 0) / data.shape[0]
    result = result / np.average(result)

    textsize = 16
    plt.figure()

    plt.plot(time, result)
    plt.ylim(0, 2)

    plt.title(f"Integral flux, RPC+LPC {date}, freq = {freq} MHz", size = textsize)

    #plt.title(f"Integral flux RPC+LPC {date}, freq = {freq / 10 ** 6} MHz", size = textsize)
    plt.xlabel("Time, s", size = 16)
    plt.ylabel("Flux, [average val.]", size = 16)
    plt.tight_layout()
    plt.savefig(f'./{foldname}/integral_for_{date}.png', transparent=False, dpi=300, bbox_inches="tight")
