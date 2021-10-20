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
    

def plotting_image(image, R = 1 , D = 1, save = False, grid_on = False, title = ''):
    '''
    Plots an image and normalize it on D and R,
    by default R = D = 1 and shows image size in pixels
    '''

    name = namestr(image)[0:3]
    cor_step_x = (len(image[0]) * D) / (R * 2)
    cor_step_y = (len(image) * D) / (R * 2)
    fig = plt.figure() 
    ax = fig.add_subplot(111)
    #print("xy ==",cor_step_x, cor_step_y)
    extent = [ -cor_step_x, cor_step_x, -cor_step_y, cor_step_y]

    plt.imshow(image, cmap = 'hot', extent = extent)    

    plt.colorbar()
    plt.title(title)
    ax.set_ylabel("Angle, [deg]", size = 16)
    ax.set_xlabel("Angle, [deg]", size = 16)
    if(grid_on == True):
    	ax.grid(True)
    
    if(save == True):
        plt.savefig(f'./The_model_{name}r.png', transparent = False, dpi = 500, bbox_inches = "tight")
        
    plt.show()
    
#--------------------------------------------------------------------------------------------------

pxSize = 0.01 # 1px = 1 cm
lsize = 2 ** 8

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
        r = (i - hsize_ant) ** 2 + (j - hsize_ant) ** 2
        if( r < R ** 2 ):
            antenna[i][j] = 1 - (np.sqrt(r)/R)

visibilityf = abs(fft2(antenna, s = [2 ** 8, 2 ** 8]).real)
visibilityf = fftshift(visibilityf)
visibilityf = visibilityf / np.max(visibilityf)

size_ant = len(visibilityf)
hsize_ant = int(size_ant / 2)


R0 = (hsize_ant - int(np.argwhere(visibilityf[hsize_ant][0 : hsize_ant] >= 0.5)[0]))


#--------------------------------------------------------------------------------------------------
# The Sun's matrix 

sun_matrix = np.zeros(shape = (size_ant * 3, size_ant * 3), dtype=np.float64)
im_size_sun = len(sun_matrix[0])
im_hsize_sun = int(im_size_sun / 2)
R_sun = (R0 * 0.53) # Sun's angular diameter

for i in range(im_size_sun):
    for j in range(im_size_sun):
        r = (i - im_hsize_sun) ** 2 + (j - im_hsize_sun) ** 2
        if( r < R_sun ** 2 ):
            sun_matrix[i][j] = 1
            #sun_matrix[i][j] = 0.5 + 0.5 * np.sin(r * np.pi / (2 * R_sun ** 2))

#--------------------------------------------------------------------------------------------------


traj = np.arange(im_hsize_sun - hsize_ant, im_hsize_sun, st)

flux = []

for k in range(len(traj)):
    flux.append(np.sum( sun_matrix[int(im_hsize_sun / 2) + k : size_ant + int(im_hsize_sun / 2) + k, 0 : size_ant ] * visibilityf ))

print(sun_matrix[int(im_hsize_sun / 2) + k : size_ant + int(im_hsize_sun / 2) + k, 0 : size_ant ] * visibilityf)
traj = (traj - traj[0]) / (R0)

print(flux)

'''
for k in traj:
    res = 0
    for i in range(size_ant):
        for j in range(size_ant):
            res += sun_matrix[ i + int(im_hsize_sun / 2) ][ j + k ] * visibilityf[i][j]
    result[num] += res
    num += 1

traj = (traj - traj[0]) / (R0)
'''

t2 = time.time_ns()
print("time =", (t2 - t1) / 10 ** 9)
'''
result = result / np.max(result)

plotting_image(antenna, R = R, grid_on = True, title = "Antenna corr")
plotting_image(visibilityf, R = R0 * 2, grid_on = True, title = "Visibility func")
plotting_image(sun_matrix, R = R0, grid_on = True, title = "The Sun")
plotting(traj, result)
'''