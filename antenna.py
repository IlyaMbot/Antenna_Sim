import numpy as np
from numpy.fft import fft2, ifft2, fftfreq
import matplotlib.pyplot as plt


#--------------------------------------------------------------------------------------------------
def plotting(x):

    fig = plt.figure()
    plt.plot(x)
    plt.show()

def plotting_image(image):

    cor_step_x = len(image[0]) * 16 / (2*R)
    cor_step_y = len(image) * 16 / (2*R)
    fig = plt.figure() 
    ax = fig.add_subplot(111)
    
    extent = [ -cor_step_x, cor_step_x, -cor_step_y, cor_step_y]

    imgplot = plt.imshow(image, extent=extent)    

    #fig = plt.figure() 
    #ax = fig.add_subplot(111)
    
    #imgplot = plt.imshow(image)    	
    ax.grid(True)
    #imgplot.set_cmap('nipy_spectral')
    plt.colorbar()
    #plt.savefig('./The_model_{}r.png'.format(name), transparent=False, dpi=500, bbox_inches="tight")
    plt.show()
#--------------------------------------------------------------------------------------------------

lsize = 2 ** 9
c = 3 * 10 ** 8
D = 3
freq_base = 3 * 10**9


antenna = np.zeros(shape = (lsize, lsize))
size_ant = len(antenna)
hsize_ant = int(size_ant / 2)
R = c / (freq_base * D) * 100
print(R)

#--------------------------------------------------------------------------------------------------

for i in range(size_ant):
    for j in range(size_ant):
        r = (i - hsize_ant) **2 + (j - hsize_ant)**2
        if( r < R ** 2 ):
            antenna[i][j] = 1 - (np.sqrt(r)/R)

plotting_image(antenna)
#plotting(antenna[hsize_ant])

sfreq = abs(fft2(antenna).real)
#plotting_image(sfreq.real)
freq = np.zeros_like(sfreq)

for i in range(size_ant):
    for j in range(size_ant):
        freq[i][j] = sfreq[i - hsize_ant][j - hsize_ant]

plotting_image(freq)