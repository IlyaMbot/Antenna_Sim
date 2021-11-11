from astropy.io import fits
import numpy as np

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

def save_fits_flux(flux: "numpy.ndarray", date: "str"):
    '''
    Save fits file of the antenna's flux.

    Parameters
    ----------
    flux : numpy array

    date : str
    '''
    l = flux.shape[0]
    hdu = fits.BinTableHDU.from_columns([
        fits.Column(name = 'DATA', format=f'{l}K', dim =(l, len(flux[0])), array = flux)
        ])
    hdu.writeto(f'R+L_AMP_{date}.fits')
    print(f'R+L_AMP_{date}.fits is saved')

#-----------------------------------------------------------------------------

def save_fits_time(time: "numpy.ndarray", date):
    '''
    Save fits file of the time.

    Parameters
    ----------
    time : numpy array

    date : str
    '''
    hdu = fits.BinTableHDU.from_columns([
        fits.Column(name = 'TIME', format='D', array = time)
        ])
    hdu.writeto(f'TIME_{date}.fits')
    print(f'TIME_{date}.fits is saved')
