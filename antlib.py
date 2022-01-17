from astropy.io import fits
import numpy as np
import os, glob
import matplotlib.pyplot as plt

#-----------------------------------------------------------------------------

def makedir(foldname):
    try:
        os.mkdir(f'./{foldname}')
        print(f"{foldname} is created")
    except OSError:
        pass

#-----------------------------------------------------------------------------

def print_keys(filename : str, i : int = 1):

    '''
    Function to print keys from header of the FITS file.

    Parameters
    ----------
    filename : str
        Path to the FITS file.
    i : int, optional
        Number of table's header. The default is 1.
    '''

    with fits.open(filename, memmap = False) as f:
        f.verify('silentfix')
        print(f'***\n{filename} is opened')
        for key in f[i].header:
            print(f"{key} - {f[i].header[key]}")
        print("***")

#-----------------------------------------------------------------------------

def get_data_for_freq(filenames : str, frequency : int = 0) -> [np.ndarray, np.ndarray, np.int32]:
    '''
    Get antennas' amplitudes of flux R+L, frequency in Hz,
    time of measurement in seconds (UT) from FITS files.

    Parameters
    ----------
    filename : str
        Path to the FITS files.
    frequency : int, optional
        Index of the frequency. The default is 0.
    '''

    amps = []
    time = []

    for filename in filenames:
        print(f"{filename} is opened")
        with fits.open( filename, memmap = False ) as f:

            f.verify('silentfix')

            amp     = f[1].data[ frequency ][ "AMP_RCP" ] + f[1].data[0][ "AMP_LCP" ]
            freq    = f[1].data[ frequency ][ "FREQUENCY" ]
            time20  = f[1].data[ frequency ][ "TIME" ]

        time.append( time20 )
        amps.append( np.reshape( amp, (20, 128) ) )

    amps    = np.reshape( np.array(amps), (len(filenames) * 20, 128) )
    amps    = np.swapaxes( amps, 0, 1)
    time    = np.reshape( np.array(time), (len(filenames) * 20 ) )

    return(amps, time, freq)


#-----------------------------------------------------------------------------

def normalize_d(data):
    '''
    data normalization function.
    Puts all values in range from 0(min) to 1(max).
    '''

    dmax = np.max(data)
    dmin = data[-1]
    data = (data - dmin)/(dmax - dmin)

    return(data)

#-----------------------------------------------------------------------------

def save_fits_flux(flux     : np.ndarray,
                   date     : str,
                   foldname : str = 'folder_name',
                   add      : str = ''
                   )  -> None:
    '''
    Save fits file of the antenna's flux with path ./foldname/ .

    Parameters
    ----------
    flux : np.ndarray

    date : str

    foldname : str
        The default is "folder_name".
    '''

    filename = f"{date}_DATA_R+L_AMP{add}.fits"
    dimant  = flux.shape[0]
    dimtime = flux.shape[1]

    makedir(foldname)

    hdu = fits.BinTableHDU.from_columns([
        fits.Column(name = 'DATA', format=f'{dimtime}K', dim = f'({dimant}, {dimtime})', array = flux)
        ])

    hdu.writeto(f'./{foldname}/{filename}', overwrite = True)
    print(f'{filename} is saved')

#-----------------------------------------------------------------------------

def save_fits_time(time     : np.ndarray,
                   date     : str,
                   foldname : str = 'folder_name',
                   add      : str = ''
                   ) -> None:
    '''
    Save fits file of the time with path ./folder_name/ .

    Parameters
    ----------
    time : np.ndarray

    date : str

    foldname : str
        The default is 'folder_name'.
    '''

    makedir(foldname)

    filename = f"{date}_TIME{add}.fits"

    hdu = fits.BinTableHDU.from_columns([
        fits.Column(name = 'TIME', format='D', array = time)
        ])
    hdu.writeto(f'./{foldname}/{filename}', overwrite = True)
    print(f'{date}_TIME.fits is saved')

#-----------------------------------------------------------------------------

def save_fits_raw(arr      : np.ndarray,
                  date     : str,
                  foldname : str = "folder_name",
                  add      : str = ""
                  ) -> None:

    arr = np.array(arr)

    filename = f"{date}_flux{add}.fits"

    makedir(foldname)

    hdu = fits.PrimaryHDU(arr)
    hdu.writeto(f'./{foldname}/{filename}', overwrite = True)
    print(f'{filename} is saved')

#-----------------------------------------------------------------------------

def remove_out_of_phase(arrays : np.ndarray, threshold : float = 1.0) -> np.ndarray:
    '''
    Remove all out of phase values and make continious (trend-like) data.

    Parameters
    ----------
    arr : np.ndarray

    threshold : "float", optional
         The default is 1.0.
    '''
    if len(arrays.shape) == 1:
        arrays = np.array([arrays])

    for arr in arrays:

        diffdata = np.diff(arr)

        outs = np.argwhere(abs(diffdata) >= np.max(abs(diffdata)) * threshold)
        outs = np.reshape(outs , (len(outs)))

        for i in range(outs.shape[0] - 1):
            arr[outs[i] + 1 : outs[i + 1] + 1 ] -= arr[outs[i] + 1] - arr[outs[i]]

        arr[outs[-1] + 1 : ] -= arr[outs[-1] + 1] - arr[outs[-1]]

    return(arrays)

#-----------------------------------------------------------------------------

def raise_negative_graph(arr : np.ndarray) -> np.ndarray:

    for i in range(len(arr)):
        m = np.min(arr[i])

        if( m < 0 ):
            arr[i] -= m

    return(arr)

#-----------------------------------------------------------------------------

def make_regulare(data, time, time_r):

    data_r = []
    k = 0

    for i in range( len( time_r ) - 1 ):
        databin = []

        for j in np.arange(k, len(time) - 1):
            if( time[j] < time_r[i + 1] ):
                databin.append( data[j] )
            else:
                k = j
                break

        if databin == []:
            databin = data[j - 1]

        data_r.append( np.average(databin) )

    return(data_r)

#------------------------------------------------------------------------------

def simple_plot(time, data, showall = False):

    if( showall == False ):
        for d in data:
            plt.figure()
            plt.ylim(0, 2 * np.mean(d))
            plt.plot(time, d)
            plt.show()
    else:
        plt.figure()
        plt.ylim( 0, 1.01 * np.max(data) )
        for d in data:
            plt.plot(time, d)
        plt.show()

#------------------------------------------------------------------------------

def get_filenames(path) -> list:

    filenames = glob.glob(path)
    filenames = sorted(filenames, key=os.path.basename)
    
    return(filenames)


'''
def plot_average(time = None, data , view: int = 0):
    return(data)
    """

    Parameters
    ----------
    
    view : int
        The default is 0 
            options: 
            0 = only average
            1 = all antenas + overplot average
    """

    view = 0

    if view == 0:
        
        plt.plot(time_r[:-1], aver)
        plt.ylim(0, 2 * np.mean(aver))

        plt.title(f"RPC+LPC {date}, freq = {freq} MHz, antenna = {l}", size = textsize)
        plt.xlabel("Time, s", size = 16)
        plt.ylabel("Flux, [average val.]", size = 16)
        plt.tight_layout()
        plt.savefig(f'./{foldname}/antenna_{l}.png', transparent=False, dpi=300, bbox_inches="tight")

    elif view == 1:
        for i in range(len(avers)):
            plt.plot(time_r[:-1], avers[i]/ np.mean(avers[i]), color = 'blue')
        plt.plot(time_r[:-1], aver, color = 'red', linewidth = 5)
        plt.ylim(0, 2 * np.mean(aver))

        plt.title(f"RPC+LPC {date}, freq = {freq} MHz, antenna = {l}", size = textsize)
        plt.xlabel("Time, s", size = 16)
        plt.ylabel("Flux, [average val.]", size = 16)
        plt.tight_layout()
        plt.savefig(f'./{foldname}/antenna_{l}_all_days.png', transparent=False, dpi=300, bbox_inches="tight")
'''

'''
import matplotlib.pyplot as plt

l = 1000
step = 5

datas = np.array([
    [ np.sin(i* np.pi/100)*300 + abs(np.random.rand() * 300) + 6000 for i in range(l) ],
    [ np.sin(i* np.pi/100)*300 + abs(np.random.rand() * 300) + 6000 for i in range(l) ],
    [ np.sin(i* np.pi/100)*300 + abs(np.random.rand() * 300) + 6000 for i in range(l) ],
    [ np.sin(i* np.pi/100)*300 + abs(np.random.rand() * 300) + 6000 for i in range(l) ],
    [ np.sin(i* np.pi/100)*300 + abs(np.random.rand() * 300) + 6000 for i in range(l) ]])

time = np.array(sorted([ i + np.random.rand()*6 for i in range(0,l)]))

result, time2 = make_regulare(datas, time, end = time.max(), step = 10)

plt.figure()
for data in datas:
    plt.plot(time, data)
plt.plot(time2, result, linewidth = 5)
plt.show()
'''
