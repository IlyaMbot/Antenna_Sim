from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt
import os, glob, antlib


filenames = glob.glob('./myfits/202108*.fits')
filenames = sorted(filenames, key=os.path.basename)



freq = 2.8
foldname = 'integral_profiles'

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
    res = []
    time_r = np.arange(10, 36300, 5)

    for i in range(len(all_datas)):
        all_datas[i][l] = antlib.remove_out_of_phase(all_datas[i][l], 0.05)
        res.append(antlib.make_regulare(all_datas[i][l], all_times[i], time_r))

    res = np.array(res)
    aver = np.sum(res, axis = 0) / (res.shape[0])
    aver = aver / np.average(aver)

    foldname = "for_each_antenna"

    try:
        os.mkdir( f"./{foldname}" )
        print( f"{foldname} is created" )
    except OSError:
        pass

    textsize = 16
    plt.figure()

    for i in range(len(res)):
        # plt.plot(all_times[i], all_datas[i][l])
        # plt.plot(time_r[:-1], res[i])
        plt.plot(time_r[:-1], aver)
    plt.ylim(0, 2)

    plt.title(f"RPC+LPC {date}, freq = {freq} MHz, antenna = {l}", size = textsize)

    plt.title(f"Integral flux RPC+LPC {date}, freq = {freq / 10 ** 6} MHz", size = textsize)
    plt.tight_layout()
    # plt.legend(fontsize = textsize * 2 / 3)
    plt.savefig(f'./{foldname}/antenna #{l}.png', transparent=False, dpi=300, bbox_inches="tight")
    # plt.show()
