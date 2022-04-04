import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from numpy.fft import fft2, ifft2, fftfreq


lsize = 2**8
lsize_s = 3 * lsize


image = np.zeros(shape = (lsize, lsize))
size = len(image)
hsize = int(size / 2)

#image[hsize+5, hsize]  = 1
R = 5
D = 20
coords = np.array([[0,0],[1,0],[-1,0],[-2,0],[2,0],[0,1],[0,2],[0,3],[0,4]])
#coords = np.array([[0,0],[0,1.1],[0.9,-0.1],[0,2.1],[2,0.1]])
#coords = np.array([[0,0],[1,0],[-1,0],[0,1],[0,-1]])

coords = coords * D
print(coords)

for cor in coords:
	for i in range(size):
		for j in range(size):
			r = (i - hsize + cor[0] )**2 + (j - hsize + cor[1] )**2
			if( r <= R**2):
				image[i,j] = 1 - (np.sqrt(r)/R)
#--------------------------------------------------------------------------------------------------

sfreq = abs(fft2(image).real)
trans = np.zeros_like(sfreq)

for i in range(size):
    for j in range(size):
        trans[i][j] = sfreq[i - hsize][j - hsize]


fig = plt.figure()


plt.subplot(121)
imgplot = plt.imshow(image, cmap = 'hot')
plt.subplot(122)
imgplot = plt.imshow(trans, cmap = 'hot')

plt.tight_layout()
# plt.savefig('./RTelescope_model_{}ant_{}wplus.png'.format(len(coords), D), transparent=False, dpi=500, bbox_inches="tight")
plt.show()
