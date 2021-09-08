import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from numpy.fft import fft2, ifft2, fftfreq


#imgSunCol = mpimg.imread('Sunfond.png')
size = 101
imgSun = np.zeros(shape = (size, size))

size = len(imgSun)
hsize = int(size / 2)

'''
for row in imgSunCol:
	ImRow = []
	for pixel in row:
		ImRow.append(pixel[0] + pixel[1] + pixel[2])	
	imgSun.append(ImRow)
'''

R = 10
for i in range(size):
    for j in range(size):
        imgSun[i][j] = np.exp(-( (i - hsize)**2 + (j - hsize)**2) /(np.pi * R))



sfreq = abs(fft2(imgSun).real)
trans = np.zeros_like(sfreq)

for i in range(size):
    for j in range(size):
        trans[i][j] = sfreq[i - hsize][j - hsize]


'''
image = np.zeros(shape = (size, size))

R = 5
D = 20
#coords = np.array([[0,0],[1,0],[-1,0],[-2,0],[2,0],[0,1],[0,2],[0,3],[0,4]])
#coords = np.array([[0,0],[1,0],[-1,0],[0,1],[0,-1]])
coords = np.array([[0,0]])
coords = coords * D

for cor in coords:
	for i in range(size):
		for j in range(size):
			r = (i - hsize + cor[0] )**2 + (j - hsize + cor[1] )**2
			if( r <= R**2):
				image[i,j] = 1 - (np.sqrt(r)/R)
#--------------------------------------------------------------------------------------------------
'''

fig = plt.figure()

extent = [ -hsize, hsize, -hsize, hsize]

plt.subplot(121)
imgplot = plt.imshow(imgSun, cmap = 'hot', extent=extent)
plt.grid(True)
plt.subplot(122)
imgplot = plt.imshow(trans, cmap = 'hot', extent=extent)
plt.grid(True)

plt.tight_layout()
#plt.savefig('./RTelescope_model_{}ant_{}wplus.png'.format(len(coords), D), transparent=False, dpi=500, bbox_inches="tight")

plt.show()
