import numpy as np
import glob, os, antlib
from astropy.io import fits



#-----------------------------------------------------------------------------

def change_freq(filenames, frequency):

    for filename in filenames:
        
        print(f"{filename} is opened")

        with fits.open( filename, memmap = False ) as f:

            f.verify('silentfix')
            f.writeto()

            freq = f[1].data[ frequency ][ "FREQUENCY" ]

        fits.writeto( filename, )
        print(freq)

    pass

#-----------------------------------------------------------------------------

minutes_arr = np.arange(10,15)
filenames = []

for i in minutes_arr:
    fpaths = glob.glob(f"./data/event_*/srh_20210522T06{i}*")
    for fpath in fpaths:
        filenames.append( fpath )

filenames = sorted(filenames, key=os.path.basename)

change_freq(filenames, 0)


