import numpy as np
import pandas as pd
from vernal import get_table
from vernal.time import tt2ut1, tdb2tt
from vernal.precise import dec_true_sun
from iers import EOP, historic_ut1_tt
import matplotlib.pyplot as plt


delta_df = historic_ut1_tt()

import spiceypy as sp

sp.furnsh('vernal/data/ker/historic.tm')

y = 17189

df = get_table(y1=y, y2=y, rot_kind='sofa_mean')

tdb_guess = df['tdb'].iloc[0]


#def refine(et, rot_kind, dt=1800, n=100):
tt = tdb_guess
n = 50
dt = 1.5
#dt = 1
tt1 = tt - dt
tt2 = tt + dt
tts = np.linspace(tt1, tt2, n)
dec = np.zeros((len(tts),))
for i, tt_ in enumerate(tts):
    dec[i] = dec_true_sun(tt_, 'mean', delta_df, eop=None)
coefs = np.polyfit(tts, dec, 1)
tt_ver = np.roots(coefs)[0]
#return np.roots(coefs)[0]


for i in dec:
    print(i)


print(tdb_guess)
print(tt_ver)
print((tdb_guess - tt_ver)*86400)

fig, ax = plt.subplots()
ax.scatter(tts, dec, s=1)
ax.scatter(tt_ver, 0, s=5, c='r')
plt.grid(True)
plt.show()

sp.kclear()

