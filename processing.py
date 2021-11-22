import numpy as np
import glob, os, antlib
import matplotlib.pyplot as plt

#paths-------------------------------------------------------------------------

# on server
# filenames = glob.glob('/mnt/badary/SRH/SRH0306/20210603/*.fit')

# on PC
folders = glob.glob("./data/*")
folders = sorted(folders, key=os.path.basename)

total = []
times = []

for folder in folders[0:1]:

    filenames = glob.glob(folder + '/*.fit')
    filenames = sorted(filenames, key=os.path.basename)


    date = filenames[0].split('/')[-1][4:-11]
    print(date)

    ants, time, freq = antlib.get_data_for_freq(filenames)
    data = np.append( np.array([time]), ants, axis = 0)

    antlib.save_fits_raw( data, date, foldname = 'myfits', add = '_all' )
    # antlib.save_fits_raw( time, date, foldname = 'myfits', add = '_time' )



