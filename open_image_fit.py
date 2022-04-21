from astropy.io import fits
import matplotlib.colors as colors
import numpy as np
import matplotlib.pyplot as plt
import os, glob, antlib

filenames = glob.glob('./sandbox*/pictures/061627RL/*.fits')
filenames = sorted(filenames, key=os.path.basename)

img = np.array([[],[]])

i = 0

with fits.open(filenames[i], memmap = True) as f:
        f.verify('silentfix')
        imgL = f[0].data

with fits.open(filenames[i + 1], memmap = True) as f:
        f.verify('silentfix')
        imgR = f[0].data

# imgL[abs(imgL) > 1 ] = 0
# imgR[abs(imgR) > 1 ] = 0

ysize = 6

plt.figure(figsize=(ysize * 2.1, ysize))
plt.subplot(121)
plt.imshow(imgL, norm = colors.SymLogNorm(linthresh=0.0001, linscale=0.0001, vmin = imgL.min(), vmax = imgL.max(), base=10))
plt.subplot(122)
plt.imshow(imgR, norm = colors.SymLogNorm(linthresh=0.3, linscale=0.3, vmin = imgL.min(), vmax = imgL.max(), base=10))
plt.tight_layout()

plt.figure(figsize=(ysize * 2.1, ysize))
plt.title("R")
plt.subplot(121)
plt.plot( np.sum(imgR, 0) )
plt.subplot(122)
plt.plot( np.sum(imgR, 1) )
plt.tight_layout()

plt.figure(figsize=(ysize * 2.1, ysize))
plt.title("L")
plt.subplot(121)
plt.plot( np.sum(imgL, 0) )
plt.subplot(122)
plt.plot( np.sum(imgL, 1) )
plt.tight_layout()

plt.show()
