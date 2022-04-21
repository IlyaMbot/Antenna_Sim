import numpy as np
import glob, os, antlib
from astropy.io import fits



#-----------------------------------------------------------------------------

def change_freq(filenames):

    for filename in filenames:
        
        print(f"{filename} is opened")

        with fits.open( filename, memmap = False, mode = "update" ) as f:

            f.verify('silentfix')
            base = [2800000, 3100000, 3500000, 4300000, 4900000, 5600000]

            freqs = f[1].data[ : ][ "FREQUENCY" ]
            print(freqs)
            for i in range(len(freqs)):
                f[1].data[ i ][ "FREQUENCY" ] = base[i]
            
            f.flush()

    pass

#-----------------------------------------------------------------------------

minutes_arr = np.arange(10,15)

# filenames = glob.glob(f"./sandbox_copies/srh_20210522T061017.fit")
filenames = glob.glob(f"./sandbox_copies/srh_20210522T05*.fit")

filenames = sorted(filenames, key=os.path.basename)

change_freq(filenames)