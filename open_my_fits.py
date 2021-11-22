from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt
import os, glob, antlib


filenames = glob.glob('./myfits/202108*.fits')
filenames = sorted(filenames, key=os.path.basename)



freq = 2.8
foldname = 'integral_profiles'

#------------------------------------------------------------------------------

time = np.arange(10, 36300, 5)

integral = np.zeros_like(time[:-1], dtype=('float64'))

for filename in filenames:
    date = filename.split('/')[-1][0:8]
    print(date)

    with fits.open(filename, memmap = True) as f:
        f.verify('silentfix')
        timedata = f[0].data[0]
        data = f[0].data


    data = antlib.remove_out_of_phase(data, 0.01)

    k = 0
    ant = []

    #bin-counting--------------------------------------------------------------

    for i in range( len( time ) - 1 ):
        databin = []
        for j in np.arange(k, len(timedata) - 1):
            if( timedata[j] < time[i + 1] ):
                databin.append( data[j] )
            else:
                k = j
                break

        if databin == []:
            databin = data[0]

        ant.append( np.average(databin) )

    #--------------------------------------------------------------------------

    integral += np.array(ant)

integral = integral / len(filenames)
time = time[:-1]


plt.figure()
plt.plot(time, integral)
plt.axis([time[0] - 500, time[-1] + 500, 0, np.max(integral) * 1.1 ])
plt.show()


'''
textsize = 16
plt.figure()
plt.plot(time, data)
plt.title(f"RPC+LPC {date}, freq = {freq} MHz, antenna = {l}", size = textsize)

# plt.title(f"Integral flux RPC+LPC {date}, freq = {freq / 10 ** 6} MHz", size = textsize)
plt.tight_layout()
plt.legend(fontsize = textsize * 2 / 3)
# plt.savefig(f'./{foldname}/{date}-antenna #{i + 1}.png', transparent=False, dpi=200, bbox_inches="tight")
plt.savefig(f'./threshold/threshold_levels_ant{l}.png', transparent=False, dpi=500, bbox_inches="tight")
plt.show()
'''