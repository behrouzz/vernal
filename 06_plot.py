import spiceypy as sp
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from vernal.rapid import vernal_equinox

df1 = pd.read_csv('vernal/data/pre_historic.csv')
df2 = pd.read_csv('vernal/data/future.csv')

df1 = pd.DataFrame({
    'year': df1['year'][::-1].values[:-1],
    'tt': df1['tt'][::-1].values[:-1]
    })



df = pd.concat([df1, df2], axis=0, ignore_index=True)

df['d'] = df['tt'].diff()

fig, ax = plt.subplots()
ax.scatter(df['year'], df['d'], s=5)
ax.ticklabel_format(useOffset=False)
plt.grid()
plt.show()

#BASE = 'C:/Moi/_py/Astronomy/Solar System/kernels/'
BASE = 'C:/Users/H21/Desktop/Desktop/Behrouz/Astronomy/kernels/'
kernels = [
    'naif0012.tls', 'pck00010.tpc', 'earth_latest_high_prec.bpc',
    'de441_part-1.bsp', 'de441_part-2.bsp'
    ]
kernels = [BASE + i for i in kernels]

for k in kernels:
    sp.furnsh(k)

#year 2177 is less thn 364 days!
et1 = vernal_equinox(2176, dt=150)
et2 = vernal_equinox(2177, dt=150)
dt = (et2 - et1) / 86400
print(dt)


sp.kclear()
