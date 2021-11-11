from astropy.io import fits
from astropy.table import Table
import numpy as np



data2 = np.linspace(0, 2500, 2500)
data1 = np.sin(data2 / 100) * 1000 + 1000
data3 = np.random.random_integers(0, 10, 2500)


hdu = fits.BinTableHDU.from_columns([
    fits.Column(name = 'DATA', format='I', array= data1),
    fits.Column(name = 'TIME', format='I', array= data2),
    fits.Column(name = 'WEIGHTS', format='B', array= data3)
    ])

hdu.writeto('test.fits')

