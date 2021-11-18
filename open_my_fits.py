from astropy.io import fits
from astropy.table import Table
import numpy as np
import matplotlib.pyplot as plt
import os, glob

def open_my(filename, k = 0):

    with fits.open(filename[k * 2], memmap = True) as f:
        f.verify('silentfix')
        data = f[1].data["DATA"]

    with fits.open(filename[k * 2 + 1], memmap = True) as f:
        f.verify('silentfix')
        time = f[1].data["TIME"]

        return(data, time)


filenames = glob.glob('./antennas_call/*.fits')
filenames2 = glob.glob('./antennas_uncall/*.fits')
# filenames = glob.glob('./antennas_uncall/*.fits')
filenames = sorted(filenames, key=os.path.basename)
filenames2 = sorted(filenames2, key=os.path.basename)

date = filenames[0].split('/')[-1][:8]
print(date)

freq = 2.8
foldname = 'comparing'

data1, time = open_my(filenames)
data2, _ = open_my(filenames2)
'''
try:
    os.mkdir(f'./{foldname}')
    print(f"{foldname} is created")
except OSError:
    pass


for i in range(len(data1)):

    textsize = 16

    plt.ioff()
    plt.figure()

    # plt.scatter(time, ants)
    plt.plot(time, data2[i], label = 'uncalibrated')
    plt.plot(time, data1[i], label = 'calibrated')

    plt.title(f"RPC+LPC {date}, freq = {freq} MHz, antenna = {i + 1}", size = textsize)

    # plt.title(f"Integral flux RPC+LPC {date}, freq = {freq / 10 ** 6} MHz", size = textsize)
    plt.legend(fontsize = textsize*2/3)
    plt.tight_layout()
    plt.axis([time[0] - 500, time[-1] + 500, 0, np.max(data2[i] + data1[i] )  * 1.0 ])
    plt.savefig(f'./{foldname}/{date}-antenna #{i + 1}.png', transparent=False, dpi=200, bbox_inches="tight")
    # plt.savefig(f'./pictures/{date}-inegral.png', transparent=False, dpi=500, bbox_inches="tight")
    # plt.show()
    plt.close()


'''
l=0

textsize = 16

plt.figure()

plt.plot(time, data2[l], label = 'uncalibrated')

plt.title(f"RPC+LPC {date}, freq = {freq} MHz, antenna = {l + 1}", size = textsize)

# plt.title(f"Integral flux RPC+LPC {date}, freq = {freq / 10 ** 6} MHz", size = textsize)
plt.tight_layout()
# plt.savefig(f'./{foldname}/{date}-antenna #{i + 1}.png', transparent=False, dpi=200, bbox_inches="tight")
# plt.savefig(f'./pictures/{date}-inegral.png', transparent=False, dpi=500, bbox_inches="tight")
plt.show()

