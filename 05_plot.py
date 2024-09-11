import spiceypy as sp
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from vernal.rapid import vernal_equinox

df1 = pd.read_csv('vernal/data/pre_historic_TETEp1976n1980.csv')
df2 = pd.read_csv('vernal/data/future_TETEp1976n1980.csv')
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


sp.furnsh('vernal/data/ker/historic.tm')

#year 2177 is less thn 364 days!
et1 = vernal_equinox(2176, dt=150, true_equator=True)
et2 = vernal_equinox(2177, dt=150, true_equator=True)
dt = (et2 - et1) / 86400
print(et1)
print(et2)
print(dt)


sp.kclear()
