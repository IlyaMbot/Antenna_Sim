import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import time
from numpy.fft import fft2, ifft2, fftshift


#--------------------------------------------------------------------------------------------------

def namestr(obj):
    # Returns name os the variable
    namespace = globals()
    res = [name for name in namespace if namespace[name] is obj]
    return(res[0])


def plotting(x, y = None):
    # Simply plots a graph

    fig = plt.figure() 
    ax = fig.add_subplot(111)
    ax.set_title("Flux-agnle dependancy", size = 20)
    try:
    	plt.plot(x,y)
    except:
    	print("xdata != ydata")
    	plt.plot(x)
    ax.set_xlabel("Angle, [deg]", size = 16)
    ax.set_ylabel("Intencity", size = 16)
    plt.show()
    

def plotting_image(image, R = 1 , D = 1, save = False, grid_on = False):
    '''
    Plots an image and normalize it on D and R,
    by default R = D = 1 and shows image size in pixels
    '''

    name = namestr(image)[0:3]
    units = ['', 'Angle, [deg]']
    
    if(name == 'ant'):
        unit = units[0]
    else:
        unit = units[1]
    
    
    cor_step_x = (len(image[0]) * D) / (R * 2)
    cor_step_y = (len(image) * D) / (R * 2)
    fig = plt.figure() 
    ax = fig.add_subplot(111)
    print("xy ==",cor_step_x, cor_step_y)
    extent = [ -cor_step_x, cor_step_x, -cor_step_y, cor_step_y]

    imgplot = plt.imshow(image, cmap = 'hot', extent=extent)    

    plt.colorbar()
    ax.set_ylabel(unit, size = 16)
    ax.set_xlabel(unit, size = 16)
    if(grid_on == True):
        ax.grid(True)
    
    if(save == True):
        plt.savefig('./The_model_{}r.png'.format(name), transparent=False, dpi=500, bbox_inches="tight")
        
    plt.show()
    
#--------------------------------------------------------------------------------------------------

pxSize = 0.01 # 1px = 1 cm
lsize = 2 ** 8
hlsize = 2 ** 7

c = 3 * 10 ** 8 # in m/s
D = 3 # in m 
freq_base = 3 * 10 ** 9 # in Hz

st = 1

t1 = time.time_ns()

#--------------------------------------------------------------------------------------------------
# making antenna's visibility function matrix

antenna = np.zeros(shape = (lsize, lsize), dtype=np.float64)
size_ant = len(antenna)
hsize_ant = int(size_ant / 2)
R = c / (freq_base * D * pxSize)

for i in range(size_ant):
    for j in range(size_ant):
        r = (i - hsize_ant) **2 + (j - hsize_ant)**2
        if( r < R ** 2 ):
            antenna[i][j] = 1 - (np.sqrt(r)/R)

sfreq = abs(fft2(antenna, s = [lsize, lsize]).real)
sfreq = fftshift(sfreq)
sfreq = sfreq / np.max(sfreq)

size_ant = len(sfreq)
hsize_ant = int(size_ant / 2)

R0 = hsize_ant - int(np.argwhere(sfreq[hsize_ant][0 : hsize_ant] >= 0.5)[0])


#--------------------------------------------------------------------------------------------------
# The Sun's matrix 
sky = np.zeros(shape = (size_ant, size_ant), dtype=np.float64)

R_sun = (R0 * 0.53) # Sun's angular diameter

X = np.arange(0, lsize).reshape(1, lsize) - lsize/2
Y = np.arange(0, lsize).reshape(lsize, 1) - lsize/2
x, y = np.meshgrid(X, Y)

r = np.sqrt(x**2 + y**2)
r[r > R_sun] = 0
sky_cos = abs(np.cos(r / ( R_sun))) 

#sun_mask = ((y - hlsize)**2 + (x - hlsize)**2) < R_sun**2


#--------------------------------------------------------------------------------------------------

'''
traj = np.arange(hlsize_sun - hsize_ant, hlsize_sun, st)
print(len(traj))
result = np.zeros_like(traj)
num = 0

for k in traj:
    res = 0
    for i in range(size_ant):
        for j in range(size_ant):
            res += sun_matrix[ i + int(im_hsize_sun/2) ][ j + k ] * sfreq[i][j]
    result[num] += res
    num += 1

traj = (traj - traj[0]) / (R0)

result = result / np.max(result)
'''

t2 = time.time_ns()
print( (t2 - t1) / 10**9)

#plotting_image(antenna, R = R, grid_on = True)
#plotting_image(sfreq, R = R0, grid_on = True)
plotting_image(sky_cos, R = R0, grid_on = True)
#plotting(traj, result)
