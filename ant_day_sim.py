from datetime import datetime, timedelta
import numpy as np
import astropy
from astropy.io import fits
import astropy.units as u
from astropy.coordinates import get_sun, EarthLocation, AltAz
import matplotlib.pyplot as plt
import antlib


#------------------------------------------------------------------------------

def get_hms(timeinsec):

    hours = int( timeinsec / 3600)
    minutes = int( (timeinsec - hours * 3600) / 60)
    seconds = int( timeinsec - hours * 3600 - minutes * 60 )

    return([hours, minutes, seconds])

#data--------------------------------------------------------------------------

path = './aver*/*.fits'

filenames = antlib.get_filenames(path)

print(filenames)
data_ants = []

for filename in [filenames[11],filenames[12],filenames[13]]:
    with fits.open(filename, memmap = True) as f:
                f.verify('silentfix')
                time_ant = f[0].data[0]
                data_ant = f[0].data[1]

    data_ant = np.array(data_ant / np.max(data_ant))
    data_ants.append(data_ant)

time_beg = get_hms(time_ant[0])
time_end = get_hms(time_ant[-1])

#Sun-simulation--------------------------------------------------------------------

time = astropy.time.Time(
    np.arange(  datetime( 2021, 8, 1, time_beg[0], time_beg[1], time_beg[2] ),
                datetime( 2021, 8, 1, time_end[0], time_end[1], time_end[2] ),
                timedelta(seconds = (time_ant[1] - time_ant[0]) )))

loc = EarthLocation(lat = 51.759 * u.deg, lon = 102.217 * u.deg ) 

altaz = AltAz(location = loc, obstime = time)
az  = get_sun(time).transform_to(altaz).az 
alt = get_sun(time).transform_to(altaz).alt 

az = az.degree
alt = alt.degree

#ant-params--------------------------------------------------------------------
a0 = 90 - 51.759
b0 = 90 - 102.217
print(a0, b0)
alpha = a0 
beta = b0 

loc_ant = EarthLocation(lat = (90 - alpha) * u.deg, lon = (90 - beta) * u.deg )
altaz_ant = AltAz(location = loc_ant, obstime = time)
az2  = get_sun(time).transform_to(altaz_ant).az 
alt2 = get_sun(time).transform_to(altaz_ant).alt 

az2 = az2.degree
alt2 = alt2.degree

#------------------------------------------------------------------------------

plt.figure()
plt.plot(time_ant[:-1], alt - alt)
for data_ant in data_ants:
    plt.plot(time_ant[:-1], data_ant[:-1] )
# plt.plot(time_ant[:-1], data_ant[:-1] * alt)
plt.show()

#------------------------------------------------------------------------------