import matplotlib.pyplot as plt
from astropy.time import Time
import numpy as np
from vernal.time import tt2tdb

jd0 = 2451258

tt = np.linspace(jd0, jd0+1000, 10000)

import spiceypy as sp
sp.furnsh('k_1600_2600.tm')
tdb_me = np.array([tt2tdb(i) for i in tt])
sp.kclear()


t = Time(tt, scale='tt', format='jd')
tdb = t.tdb.value


fig, ax = plt.subplots()
ax.scatter(range(len(tt)), tdb_me-tt, c='b', s=1, alpha=0.5)
ax.scatter(range(len(tt)), tdb-tt, c='r', s=1, alpha=0.5)
plt.show()
