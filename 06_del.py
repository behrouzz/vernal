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
df12 = pd.concat([df1, df2], axis=0, ignore_index=True)
df12['d'] = df12['tt'].diff()


df3 = pd.read_csv('vernal/data/pre_historic.csv')
df4 = pd.read_csv('vernal/data/future.csv')
df3 = pd.DataFrame({
    'year': df3['year'][::-1].values[:-1],
    'tt': df3['tt'][::-1].values[:-1]
    })
df34 = pd.concat([df3, df4], axis=0, ignore_index=True)
df34['d'] = df34['tt'].diff()


fig, ax = plt.subplots(2,1)
ax[0].scatter(df34['year'], df34['d'], s=5, c='r')
ax[1].scatter(df12['year'], df12['d'], s=5, c='b')
ax[0].ticklabel_format(useOffset=False)
ax[1].ticklabel_format(useOffset=False)
plt.show()


d_tt = df12['tt'] - df34['tt']
d_d = df12['d'] - df34['d']


df = pd.DataFrame({
    'year': df12['year'].values,
    'd_tt': (df12['tt'] - df34['tt']).values,
    'd_d': (df12['d'] - df34['d']).values
    })


##fig, ax = plt.subplots()
##ax.scatter(df['year'], df['d_d'], s=5)
##ax.ticklabel_format(useOffset=False)
##plt.grid()
##plt.show()
