import numpy as np
from numpy.fft import fft2, ifft2, fftfreq
import matplotlib.pyplot as plt
from scipy.special import jn_zeros


#--------------------------------------------------------------------------------------------------
def plotting(x):

    fig = plt.figure()
    plt.plot(x)
    plt.show()

def plotting_image(image, D, R):

    cor_step_x = (len(image[0]) * D) / (R * 2)
    cor_step_y = (len(image) * D) / (R * 2)
    fig = plt.figure() 
    ax = fig.add_subplot(111)
    
    extent = [ -cor_step_x, cor_step_x, -cor_step_y, cor_step_y]

    imgplot = plt.imshow(image, cmap = 'hot', extent=extent)    

    #fig = plt.figure() 
    #ax = fig.add_subplot(111)
    
    #imgplot = plt.imshow(image)    	
    ax.grid(True)
    #imgplot.set_cmap('nipy_spectral')
    plt.colorbar()
    #plt.savefig('./The_model_{}r.png'.format(name), transparent=False, dpi=500, bbox_inches="tight")
    plt.show()
#--------------------------------------------------------------------------------------------------

pxSize = 0.01 # 1px = 1 cm

lsize = 2 ** 7 # in pxs
c = 3 * 10 ** 8 # in m/s
D = 3 # in m 
freq_base = 3 * 10**9 # in Hz


antenna = np.zeros(shape = (lsize, lsize))
size_ant = len(antenna)
hsize_ant = int(size_ant / 2)
R = c / (freq_base * D * pxSize) 
print(R)

#--------------------------------------------------------------------------------------------------

for i in range(size_ant):
    for j in range(size_ant):
        r = (i - hsize_ant) **2 + (j - hsize_ant)**2
        if( r < R ** 2 ):
            antenna[i][j] = 1 - (np.sqrt(r)/R)


plotting_image(antenna,D, R)
#plotting(antenna[hsize_ant])

sfreq = abs(fft2(antenna).real)
#plotting_image(sfreq.real)
freq = np.zeros_like(sfreq)


for i in range(size_ant):
    for j in range(size_ant):
        freq[i][j] = (sfreq[i - hsize_ant][j - hsize_ant])/sfreq.max()

R0 = hsize_ant - int(np.argwhere(freq[hsize_ant][0 : hsize_ant] >= 0.5)[0])

plotting_image(freq, 1, R0 )
