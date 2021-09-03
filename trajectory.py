import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import time


#--------------------------------------------------------------------------------------------------
def namestr(obj):
    namespace = globals()
    res = [name for name in namespace if namespace[name] is obj]
    return(res[0])

def plotting_image(image, R, *args, **kwargs):

    name = namestr(image)[0:3]
    cor_step_x = len(image[0]) * 16 / (2*R)
    cor_step_y = len(image) * 16 / (2*R)
    fig = plt.figure()
    ax = fig.add_subplot(111)

    extent = [ -cor_step_x, cor_step_x, -cor_step_y, cor_step_y]

    imgplot = plt.imshow(image, extent=extent)
    #ax.grid(True)
    #imgplot.set_cmap('nipy_spectral')
    #plt.colorbar.ColorbarBase(cmap='nipy_spectral')
    #plt.colorbar()
    #plt.savefig('./The_model_{}r.png'.format(name), transparent=False, dpi=500, bbox_inches="tight")
    plt.show()
#--------------------------------------------------------------------------------------------------

lsize = 2**8
lsize_s = 3 * lsize

perc = 20
perc_a = 20

st = 10

t1 = time.time_ns()

#--------------------------------------------------------------------------------------------------

sun_matrix = np.zeros(shape = (lsize_s, lsize_s))
im_size_sun = len(sun_matrix[0])
im_hsize_sun = int(im_size_sun / 2)
R_sun = (perc * im_size_sun / 200)

ant_matrix = np.zeros(shape = (lsize, lsize))
im_size_ant = len(ant_matrix)
im_hsize_ant = int(im_size_ant / 2)
R = perc_a * R_sun / 100

#--------------------------------------------------------------------------------------------------

for i in range(im_size_ant):
    for j in range(im_size_ant):
        ant_matrix[i][j] = abs( np.sinc( np.arctan( ( (i - lsize/2) **2 + (j - lsize/2)**2 ) / R**2 )) )

#--------------------------------------------------------------------------------------------------

for i in range(im_size_sun):
    for j in range(im_size_sun):
        r = (i - lsize_s / 2) **2 + (j - lsize_s / 2)**2
        if( r < R_sun**2 ):
            #sun_matrix[i][j] = 1
            sun_matrix[i][j] = np.cos(r * np.pi / (2 * R_sun**2))

#--------------------------------------------------------------------------------------------------


traj = np.arange(0, im_size_sun - im_size_ant, st)
result = np.zeros_like(traj)
num = 0

for k in traj:
    res = 0
    for i in range(im_size_ant):
        for j in range(im_size_ant):
            res += sun_matrix[ i + im_hsize_sun ][ j + k ] * ant_matrix[i][j]
    result[num] += res
    num += 1

'''
CUT = sun_matrix[0:512][0 : im_size_ant][0:512]
print(len(CUT), len(CUT[0]))
print(CUT)
print((im_hsize_sun - im_hsize_ant), (im_hsize_sun + im_hsize_ant), im_size_ant)
plotting_image(CUT, R_sun)

for k in traj:
    res_mat = sun_matrix[im_hsize_sun - im_hsize_ant : im_hsize_sun + im_hsize_ant][0 + k : im_size_ant + k ] * ant_matrix
    #print(im_size_ant + k )
    result[num] = np.sum(res_mat)
    num += 1
'''

t2 = time.time_ns()
print( (t2 - t1) / 10**9)

result = result / np.max(result)
fig = plt.figure()
ax = fig.add_subplot(111)
plt.plot(result)
ax.set_title('"Time" profile, {}% of Sun\'s R'.format(perc_a), size = 25)
print('he')
plt.show()

plotting_image(sun_matrix, R_sun)
plotting_image(ant_matrix, R_sun)
