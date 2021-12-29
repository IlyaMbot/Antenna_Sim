import numpy as np
import glob, os, antlib
import matplotlib.pyplot as plt

#paths-------------------------------------------------------------------------

# on server
folders = glob.glob('/mnt/badary/SRH/SRH0306/202108*') 

# on PC
#folders = glob.glob("./data/*")
folders = sorted(folders, key=os.path.basename)

total = []
times = []

for folder in folders:

    filenames = glob.glob(folder + '/*.fit')
    filenames = sorted(filenames, key=os.path.basename)


    date = filenames[0].split('/')[-1][4:-11]
    print(date)
    ants, time, freq = antlib.get_data_for_freq(filenames, 5)
    data = np.append( np.array([time]), ants, axis = 0)

    antlib.save_fits_raw( data, date, foldname = 'data', add = f'_freq{ freq / 10 ** 5 }' )
    # antlib.save_fits_raw( time, date, foldname = 'myfits', add = '_time' )



