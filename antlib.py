from astropy.io import fits
import numpy as np
import os

#-----------------------------------------------------------------------------

def print_keys(filename : "str", i : 'int' = 1):

    '''
    Function to print keys from header of the FITS file.

    Parameters
    ----------
    filename : "str"
        Path to the FITS file.
    i : 'int', optional
        Number of table's header. The default is 1.
    '''

    with fits.open(filename, memmap = True) as f:
        f.verify('silentfix')
        print(f'***\n{filename} is opened')
        for key in f[i].header:
            print(f"{key} - {f[i].header[key]}")
            print("***")

#-----------------------------------------------------------------------------

def get_data_for_freq(filename : "str", frequency : 'int' = 0):
    '''
    Get antennas' amplitudes R+L, frequency in Hz, time of measurement in seconds (UT) from FITS file.

    Parameters
    ----------
    filename : "str"
        Path to the FITS file.
    frequency : 'int', optional
        Index of the frequency. The default is 0.

    '''
    with fits.open(filename, memmap = True) as f:
        f.verify('silentfix')
        ants = f[1].data[frequency]["AMP_RCP"] + f[1].data[0]["AMP_LCP"]
        freq = f[1].data[frequency]["FREQUENCY"]
        time = f[1].data[frequency]["TIME"]
        ants = np.reshape(ants, (20, 128))
    return(ants, freq, time)

#-----------------------------------------------------------------------------

def normalize_d(data):
    '''
    Data normalization function.
    Puts all values in range from 0(min) to 1(max).
    '''
    dmax = np.max(data)
    dmin = data[-1]
    data = (data - dmin)/(dmax - dmin)
    return(data)

#-----------------------------------------------------------------------------

def save_fits_flux(flux: "numpy.ndarray", date: "str", foldname : "str" = 'folder_name'):
    '''
    Save fits file of the antenna's flux with path ./folder_name/ .

    Parameters
    ----------
    flux : "numpy.ndarray"

    date : "str"

    foldname : "str"
        The default is 'folder_name'.
    '''

    try:
        os.mkdir(f'./{foldname}')
        print(f"{foldname} is created")
    except OSError:
        pass

    dimant = flux.shape[0]
    dimtime = flux.shape[1]
    hdu = fits.BinTableHDU.from_columns([
        fits.Column(name = 'DATA', format=f'{dimtime}K', dim = '(dimant, dimtime)', array = flux)
        ])
    hdu.writeto(f'./{foldname}/R+L_AMP_{date}.fits', overwrite = True)
    print(f'R+L_AMP_{date}.fits is saved')

#-----------------------------------------------------------------------------

def save_fits_time(time: "numpy.ndarray", date: "str", foldname : "str" = 'folder_name',):
    '''
    Save fits file of the time with path ./folder_name/ .

    Parameters
    ----------
    time : "numpy.ndarray"

    date : "str"

    foldname : "str"
        The default is 'folder_name'.
    '''

    try:
        os.mkdir(f'./{foldname}')
        print(f"{foldname} is created")
    except OSError:
        pass

    hdu = fits.BinTableHDU.from_columns([
        fits.Column(name = 'TIME', format='D', array = time)
        ])
    hdu.writeto(f'./{foldname}/TIME_{date}.fits', overwrite = True)
    print(f'TIME_{date}.fits is saved')

def remove_out_of_phase(data: "numpy.ndarray", threshold : "float" = 1.0):
    '''
    Remove all out of phase values and make continious (trend-like) data.

    Parameters
    ----------
    data : "numpy.ndarray"

    threshold : "float", optional
         The default is 1.0.
    '''

    diffdata = np.diff(data)

    stops = np.argwhere(abs(diffdata) >= np.max(abs(diffdata)) * threshold)
    stops = np.reshape(stops , (len(stops)))

    for i in range(len(stops) - 1):
        data[stops[i] + 1 : stops[i + 1] + 1 ] -= data[stops[i] + 1] - data[stops[i]]
    data[stops[-1] + 1 : ] -= data[stops[-1] + 1] - data[stops[-1]]

    return(data)