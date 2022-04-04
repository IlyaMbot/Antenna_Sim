from datetime import datetime, timedelta
import numpy as np
import astropy
import astropy.units as u
from astropy.coordinates import get_sun, EarthLocation, AltAz
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit as cf

#functions----------------------------------------------------------------------

def sin_sun(x, A, k, b):
    return( A * np.sin(k * x) + b )

#Sun-simulation--------------------------------------------------------------------

time = astropy.time.Time(
    np.arange(  datetime( 2021, 8, 1, 0, 0, 0 ),
                datetime( 2021, 8, 3, 0, 0, 0 ),
                timedelta(seconds = 4 )))

loc = EarthLocation(lat = 51.759 * u.deg, lon = 102.217 * u.deg ) 

altaz = AltAz(location = loc, obstime = time)
az  = get_sun(time).transform_to(altaz).az 
alt = get_sun(time).transform_to(altaz).alt 

az = az.degree
alt = alt.degree

# parms, _ = cf(sin_sun, time,  )

a = -0.65 
b =  0.65
alt2 = np.linspace( a, b, len(alt) )

time = np.array(time)

texsize = 16
plt.figure()
plt.title("Trajectory" ,size = texsize)
plt.xlabel('Time', size = texsize)
plt.ylabel('Altitude difference', size = texsize)
plt.plot(alt, color = 'blue', linewidth = 4, label = "Sun")
plt.plot(alt2 + alt , color = 'orange', linewidth = 4, label = "Ant")
plt.legend()
plt.tight_layout()
plt.show()

#------------------------------------------------------------------------------