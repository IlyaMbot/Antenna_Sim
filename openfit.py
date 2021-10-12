import numpy as np
import matplotlib.pyplot as plt
import pathlib
from astropy.io import fits

directory = pathlib.Path("/home/conpucter/GitHub/try/DataSRH/2021/07")

imfile = directory / "mf_20210107_000302.fit"

f = fits.open(imfile)
f.verify('silentfix')

'''
for key in f[0].header:
    print(f"{key} - {f[0].header[key]}")
print("***")
'''
'''
for key in f[1].header:
    print(f"{key} - {f[1].header[key]}")
'''
data = f[1].data[0]

#freqs = [data[i][0] for i in range(len(data))] 
freq = data[0]
time = data[1]
ramps = data[2]
lamps = data[3]

ramps = np.reshape(6,20,128)

plt.plot(ramps)
plt.plot(lamps)
plt.show()