from datetime import datetime, timedelta
import numpy as np
import astropy
from astropy.io import fits
import astropy.units as u
from astropy.coordinates import get_sun, EarthLocation, AltAz
import matplotlib.pyplot as plt
import antlib


#functions----------------------------------------------------------------------

def get_hms(timeinsec: int) -> list:
    '''
    Split time in seconds into hours, minutes and seconds
    '''

    hours = int( timeinsec / 3600 )
    minutes = int( (timeinsec - hours * 3600) / 60 )
    seconds = int( timeinsec - hours * 3600 - minutes * 60 )

    return([hours, minutes, seconds])


def find_flux(alt_a : np.ndarray, alt_s : np.ndarray = None) -> np.ndarray:
    '''
    Find the flux for the difference of alt_a (antenna's altitude) and alt_s (Sun's altitude)
    if alt_s = None it is assumed that alt_a is difference by default
    '''

    if( type(alt_s) == None ):
        alt_a = np.array(alt_a)
        diff = abs(alt_a)        
    else:
        alt_a = np.array(alt_a)
        alt_s = np.array(alt_s)
        diff = abs(alt_a - alt_s)

    response = np.load('model56.npy')

    flux = np.zeros_like(diff)
    
    for i in range(len(diff)):
        idx = (np.abs(response[0] - diff[i])).argmin()
        flux[i] = response[1, idx]
    
    return(flux)

def rotation(x0, y0, theta):
    
    x =   x0 * np.cos(theta) + y0 * np.sin(theta)
    y = - x0 * np.sin(theta) + y0 * np.cos(theta)

    return(x, y)

#data--------------------------------------------------------------------------

path = './aver*/*.fits'

filenames = antlib.get_filenames(path)

data_ants = []
num = 23

#load the flux from antenas
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
                timedelta(seconds = ( time_ant[1] - time_ant[0] ) )
                ) )

loc = EarthLocation(lat = 51.759 * u.deg, lon = 102.217 * u.deg) 

altaz = AltAz(location = loc, obstime = time)
az  = get_sun(time).transform_to(altaz).az 
alt = get_sun(time).transform_to(altaz).alt 

az = az.degree
alt = alt.degree

#ant-params--------------------------------------------------------------------

# axis' tilts relative to the ecliptics
a0 = 90 - 51.759 
b0 = 90 - 102.217

'''
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


alpha = 1 * np.pi / 180 # in grad
beta  = 0 * np.pi / 180 # in grad

lon = len(alt) / 2 * ( np.sin(beta) + 1 )

a = np.arctan(alpha) * lon * np.sin( ( beta + np.pi / 2 ) / 2 * np.pi)
b = np.arctan(alpha) * lon * np.cos( ( beta + np.pi / 2 ) / 2 )
print(a,b)
alt = np.zeros_like(alt)
alt2 = np.linspace( a, b, len(alt) )
print(alt2)

angle = np.arctan( (b - a) / len(alt) )
print(angle)

#------------------------------------------------------------------------------

flux_mod = find_flux( alt, alt2 )
#graph-plot--------------------------------------------------------------------

texsize = 16
plt.figure()

plt.subplot(121)
plt.title("Trajectory" ,size = texsize)
# plt.title(f"antenna {num + 1} simulation, $\\alpha$ = {alpha}, $\\beta$ = {beta}", size = 16)
plt.ylim(-2,2)
plt.xlabel('Time', size = texsize)
plt.ylabel('Altitude difference', size = texsize)
plt.plot(time_ant[:-1], np.zeros_like(alt), color = 'blue', linewidth = 4, label = "Sun")
plt.plot(time_ant[:-1], alt2, color = 'orange', linewidth = 4, label = "Ant")
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