import numpy as np
import glob, os, antlib
import time as t

#paths-------------------------------------------------------------------------

# on server
# filenames = glob.glob('/mnt/badary/SRH/SRH0306/20210603/*.fit')

# on PC
folders = glob.glob("./data/*")
folders = sorted(folders, key=os.path.basename)

for folder in folders:

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

        ants20, freq, time20 = antlib.get_data_for_freq(filename)
        time.append(time20)
        ants.append(ants20)

    ants = np.reshape(ants, (len(filenames) * 20, 128))

    ants = np.swapaxes(np.array(ants), 0, 1)
    time = np.reshape(np.array(time), (len(filenames) * 20 ))

    # ants = antlib.remove_out_of_phase(ants, 0.01)
    ants = antlib.raise_graph(ants)

    foldername = 'antennas_uncall'

    antlib.save_fits_flux(ants, date, foldname = foldername)
    antlib.save_fits_time(time, date, foldname = foldername)