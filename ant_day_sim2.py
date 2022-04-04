from datetime import datetime, timedelta
import numpy as np
import astropy
from astropy.io import fits
import astropy.units as u
from astropy.coordinates import get_sun, EarthLocation, AltAz
import matplotlib.pyplot as plt
import antlib


#functions----------------------------------------------------------------------

def get_hms(timeinsec):

    hours = int( timeinsec / 3600)
    minutes = int( (timeinsec - hours * 3600) / 60)
    seconds = int( timeinsec - hours * 3600 - minutes * 60 )

    return([hours, minutes, seconds])

response = np.load('model56.npy')

def find_flux(value):
    global response
    idx = (np.abs(response[0] - value)).argmin()
    return( response[1, idx] )

#data--------------------------------------------------------------------------

path = './aver*/*.fits'

filenames = antlib.get_filenames(path)

data_ants = []
num = 23

for filename in [filenames[num]]:
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
'''
a0 = 90 - 51.759
b0 = 90 - 102.217
ot = 1

alpha = a0 + ot
beta = b0 - 0.05
print(alpha, beta)
loc_ant = EarthLocation(lat = (90 - alpha) * u.deg, lon = (90 - beta) * u.deg )
altaz_ant = AltAz(location = loc_ant, obstime = time)
az2  = get_sun(time).transform_to(altaz_ant).az 
alt2 = get_sun(time).transform_to(altaz_ant).alt 

az2 = az2.degree
alt2 = alt2.degree

alt = np.array(alt)
alt2 = np.array(alt2) - ot

'''
a = -0.65 
b =  0.65
alt = np.zeros_like(alt)
alt2 = np.linspace( a, b, len(alt) )
angle = np.arctan( (b - a) / len(alt))
print(angle)


#------------------------------------------------------------------------------

flux_mod = np.zeros_like(alt)

for i in range(len(alt)):
    flux_mod[i] = find_flux(abs(alt2[i] - alt[i] ))
#------------------------------------------------------------------------------

texsize = 16
plt.figure()

plt.subplot(121)
plt.title("Trajectory" ,size = texsize)
# plt.title(f"antenna {num + 1} simulation, $\\alpha$ = {alpha}, $\\beta$ = {beta}", size = 16)
plt.ylim(-2,2)
plt.xlabel('Time', size = texsize)
plt.ylabel('Altitude difference', size = texsize)
plt.plot(time_ant[:-1], np.zeros_like(alt), color = 'blue', linewidth = 4, label = "Sun")
plt.plot(time_ant[:-1], alt2 , color = 'orange', linewidth = 4, label = "Ant")
# plt.plot(time_ant[:-1], alt, color = 'blue', linewidth = 4, label = "Sun")
# plt.plot(time_ant[:-1], alt2 + alt , color = 'orange', linewidth = 4, label = "Ant")
plt.legend()

plt.subplot(122)
plt.title("Flux" ,size = texsize)
plt.xlabel('Time', size = texsize)
plt.ylabel('Flux normalized', size = texsize)
plt.ylim(0,1.1)
plt.plot(time_ant[:-1], flux_mod)
plt.plot(time_ant[:-1], data_ant[:-1])
'''
i=1
for data_ant in data_ants: 
    plt.plot(time_ant[:-1], data_ant[:-1], color = (i/len(data_ants), 0, 0) )
    i+=1
# plt.plot(time_ant[:-1], data_ant[:-1] * alt)
'''
plt.tight_layout()
# plt.savefig(f'./Sim.png', transparent = False, dpi = 300, bbox_inches = "tight")
plt.show()

#------------------------------------------------------------------------------