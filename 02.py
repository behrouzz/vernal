import numpy as np
import vernal as ver
from vernal.time import et2tt
import spiceypy as sp
from iers import EOP
from iers.time import any2mjd

def tt2ut1(df, tt):
    mjd = tt - 2400000.5
    
    ut11 = df[df['mjd']<mjd]['mjd'].iloc[-1] + 2400000.5
    ut1_tai1 = df[df['mjd']<mjd]['ut1_tai'].iloc[-1]
    ut12 = df[df['mjd']>mjd]['mjd'].iloc[0] + 2400000.5
    ut1_tai2 = df[df['mjd']>mjd]['ut1_tai'].iloc[0]

    tai1 = ut11 - (ut1_tai1 / 86400)
    tai2 = ut12 - (ut1_tai2 / 86400)

    tt1 = tai1 + (32.184 / 86400)
    tt2 = tai2 + (32.184 / 86400)

    ut1 = np.interp(tt, [tt1, tt2], [ut11, ut12])

    return ut1


sp.furnsh('k_1600_2600.tm')
df = ver.get_df(400, back=True)
df['tt'] = df['et'].apply(lambda x: et2tt(x))
sp.kclear()



e = EOP(kind=4)
cnd = e.table['ut1_tai']!=99.99
tbl = e.table[cnd]

##tt = df['tt'].iloc[0]
##ut1 = tt2ut1(tbl, tt)



df['ut1'] = [tt2ut1(tbl, i) for i in df['tt']]

df = df[df['gregorian']>=1962]

import matplotlib.pyplot as plt
from astropy.time import Time
t = Time(df.tt.values, scale='tt', format='jd')

fig, ax = plt.subplots()
ax.plot(df['gregorian'].values, (df['tt'] - df['ut1']).values, c='b')
ax.plot(df['gregorian'].values, t.tt.value - t.ut1.value, c='r')
plt.show()
