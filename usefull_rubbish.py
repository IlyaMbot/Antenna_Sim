'''
from openold.py
for ant in ants:
    t1 = t.time()

    # ant = ant / np.average(ant)
    # ant = ant / np.max(ant)
    # dant = np.diff(ant)
    # dant = dant / np.max(dant)
    plt.figure()
    plt.plot( time, ant, label = f"antenna #{i}" )
    # plt.plot( time[:-1], dant, label = f"antenna #{i}" )
    # plt.scatter(time[:-2], dant, label = f"antenna #{i}")
    i += 1

    plt.title(f"RPC+LPC {date}, freq = {freq / 10 ** 6} MHz, antenna = {i}", size = textsize)
    # plt.legend()
    plt.tight_layout()
    # plt.savefig(f'./pictures/{date}-antenna #{i}.png', transparent=False, dpi=100, bbox_inches="tight")
    plt.show()
    print(f'Time_saving = {t.time() - t1}')
'''

#plotting----------------------------------------------------------------------

'''
textsize = 16

plt.figure()

# plt.scatter(time, ants)
plt.plot(time, ant)
plt.title(f"RPC+LPC {date}, freq = {freq / 10 ** 6} MHz, antenna = {k}", size = textsize)

# plt.title(f"Integral flux RPC+LPC {date}, freq = {freq / 10 ** 6} MHz", size = textsize)
plt.tight_layout()
plt.axis([time[0] - 500, time[-1] + 500, 0, np.max(ant) * 1.1 ])
# plt.savefig(f'./pictures/{date}-antenna #{k}.png', transparent=False, dpi=100, bbox_inches="tight")
# plt.savefig(f'./pictures/{date}-inegral.png', transparent=False, dpi=500, bbox_inches="tight")
plt.show()
'''