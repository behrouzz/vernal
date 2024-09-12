# length of year 2177 is less than 364 days!

import pandas as pd
import matplotlib.pyplot as plt
import spiceypy as sp
from vernal.rapid import df2000_to_year
from vernal.time import et2jd, jd2et
import numpy as np

sp.furnsh('vernal/data/ker/historic.tm')


df = df2000_to_year(2099, dt=2, rot_kind='spice_tete')
df.columns = ['year', 'tt_spice_tete']
df2 = df2000_to_year(2099, dt=2, rot_kind='sofa_mean')
df3 = df2000_to_year(2099, dt=2, rot_kind='sofa_bpn')

df['tt_sofa_mean'] = df2['tt']
df['tt_sofa_bpn'] = df3['tt']

df['d_tete_mean'] = df['tt_spice_tete'] - df['tt_sofa_mean']
df['d_sofa_spice'] = df['tt_spice_tete'] - df['tt_sofa_bpn']

fig, ax = plt.subplots()
#ax.scatter(df['year'], df['d_tete_mean'], s=5)
ax.scatter(df['year'], df['d_sofa_spice'], s=5)
ax.ticklabel_format(useOffset=False)
plt.grid()
plt.show()

sp.kclear()
