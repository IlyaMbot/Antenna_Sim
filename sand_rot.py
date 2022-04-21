import numpy as np
import matplotlib.pyplot as plt


#functions--------------------------------------------------------------------------


def rotation(x0, y0, theta):
    
    x =   x0 * np.cos(theta) + y0 * np.sin(theta)
    y = - x0 * np.sin(theta) + y0 * np.cos(theta)

    return(x, y)


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


#data--------------------------------------------------------------------------

alpha = 10
beta = 10

x = np.linspace(-0.5, 0.5, 1000)
y = np.cos(x * np.pi)

x2, y2 = rotation(x, y, beta * np.pi / 180 )

amp = abs(y - y2)

boxsize = 1


plt.figure(figsize=(13, 6))

plt.subplot(121)
plt.xlim(-boxsize, boxsize)
plt.ylim(-boxsize + 0.5, boxsize + 0.5)
plt.axhline(y = 0, linestyle = "--", color = "black")
plt.axvline(x = 0, linestyle = "--", color = "black")
plt.plot(x, y)
plt.plot(x2,y2)

plt.subplot(122)
plt.xlim(-0.6, 0.6)
plt.ylim(0, 0.1)
plt.plot(x, amp)

plt.show()