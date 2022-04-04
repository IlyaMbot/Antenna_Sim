import numpy as np
import glob, os, antlib

#paths-------------------------------------------------------------------------

# on server
# folders = glob.glob('/mnt/badary/SRH/SRH0306/202108*')

# on PC
folders = glob.glob("./data/event_*")
folders = sorted(folders, key=os.path.basename)

total = []
times = []

for folder in folders:

    filenames = glob.glob(folder + '/*.fit')
    filenames = sorted(filenames, key=os.path.basename)

    date = filenames[0].split('/')[-1][4:-11]
    print(date)
    ants, time, freq = antlib.get_data_for_freq(filenames, 0)
    data = np.append( np.array([time]), ants, axis = 0)

    antlib.save_fits_raw( data, date, foldname = 'result_event', add = f'_freq{ int(freq / 10 ** 5) }' )
