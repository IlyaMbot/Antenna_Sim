import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def namestr(obj):
    namespace = globals()
    res = [name for name in namespace if namespace[name] is obj]
    return(res[0])


def plotting_image(image, R, *args, **kwargs):

    name = namestr(image)[0:3]
    cor_step = 2**8 * 32 / (2*R)
    step = 5.12
    fig = plt.figure() 
    ax = fig.add_subplot(111)
    
    extent = [ -cor_step, cor_step, -cor_step, cor_step]

    imgplot = plt.imshow(image, extent=extent)    	
    ax.grid(True)
    #imgplot.set_cmap('nipy_spectral')
    #plt.colorbar.ColorbarBase(cmap='nipy_spectral')
    plt.colorbar()
    #plt.savefig('./The_model_{}r.png'.format(name), transparent=False, dpi=500, bbox_inches="tight")
    plt.show()

def plotting(x, y, *args, **kwargs):
    angles = np.arange(0, 360, 30)

    fig = plt.figure()
    ax = fig.add_subplot(projection='polar')
    ax.set_rorigin(0)
    ax.set_theta_zero_location(loc = "N")
    ax.set_thetagrids(angles)
    plt.polar(x, y)
    ax.grid(True)
    
    #plt.savefig('./2D_diag.png', transparent=False, dpi=500, bbox_inches="tight")
    plt.show()

lsize = 2**9

ant_matrix = np.zeros(shape = (lsize, lsize))
im_size_1 = len(ant_matrix)
R = 50
for i in range(im_size_1):
    for j in range(im_size_1):
        #ant_matrix[i][j] = np.sinc( np.arctan( ( (i - lsize/2) **2 + (j - lsize/2)**2 ) / R**2 ) ) 
        ant_matrix[i][j] = abs( np.sinc( np.arctan( ( (i - lsize/2) **2 + (j - lsize/2)**2 ) / R**2 )) )

sun_matrix = np.zeros(shape = (lsize, lsize))
im_size = len(sun_matrix)
R_sun = 100
for i in range(im_size):
    for j in range(im_size):
        r = (i - lsize/2) **2 + (j - lsize/2)**2
        if( r < R_sun**2 ):
            #sun_matrix[i][j] = 1
            sun_matrix[i][j] = np.cos(r * np.pi / (2 * R_sun**2))


time = np.arange(-np.pi, np.pi, 2*np.pi/500)
diagram = abs(np.sinc(time))

#plotting(time, diagram)
plotting_image(ant_matrix, R_sun)
plotting_image(sun_matrix, R_sun)
