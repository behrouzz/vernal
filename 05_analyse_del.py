import pandas as pd
from vernal.rapid import dec_true_sun, do_loop
from vernal.time import jd2et, et2jd
import spiceypy as sp
import numpy as np
import matplotlib.pyplot as plt


df1 = pd.read_csv('vernal/data/de441/spice_tete.csv')
df2 = pd.read_csv('vernal/data/de441/sofa_mean.csv')
df3 = pd.read_csv('vernal/data/de441/sofa_bpn.csv')



df = df1.copy()

sp.furnsh('vernal/data/ker/historic.tm')

tdb = df.loc[df['year']==2461, 'tdb'].iloc[0]

dec_ = dec_true_sun(jd2et(tdb), 'spice_tete')

et1 = jd2et(tdb) - 1800
et2 = jd2et(tdb) + 1800

ets = np.linspace(et1, et2, 100)

dec = np.zeros((len(ets),))
for i, et in enumerate(ets):
    dec[i] = dec_true_sun(et, 'spice_tete')


coefs = np.polyfit(ets, dec, 1)
et0 = np.roots(coefs)

fig, ax = plt.subplots()
ax.scatter(ets, dec, c='b', s=1)
ax.scatter([et0], [0], c='r', s=20)
ax.scatter([jd2et(tdb)], [dec_], c='g', s=20)
plt.grid()
plt.show()

sp.kclear()
