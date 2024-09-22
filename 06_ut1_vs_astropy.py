import numpy as np
import pandas as pd
from vernal import get_table
from vernal.time import tt2ut1, tdb2tt
from iers import historic_ut1_tt
import matplotlib.pyplot as plt

df = get_table(y1=1980, y2=2000, rot_kind='sofa_mean')
delta_df = historic_ut1_tt()


# if considering difference between TT and TDB
consid_tt_tdb = False
if consid_tt_tdb:
    import spiceypy as sp
    sp.furnsh('vernal/data/ker/historic.tm')
    df['tt'] = df['tdb'].apply(lambda x: tdb2tt(x))
    df['ut1'] = tt2ut1(df['tt'].values, delta_df)
    df['d'] = df['tt'] - df['ut1']
    sp.kclear()
else:
    df['ut1'] = tt2ut1(df['tdb'].values, delta_df)
    df['d'] = df['tdb'] - df['ut1']

# astropy
from astropy.time import Time
t = Time(df['tdb'].values, scale='tdb', format='jd')
d_astropy = t.value - t.ut1.value

fig, ax = plt.subplots()
ax.plot(df['year'].values, df['d'].values, c='b')
ax.plot(df['year'].values, d_astropy, c='r')
ax = plt.gca()
ax.grid(True)
plt.show()


df['ut1_astropy'] = t.ut1.value
df['d_me_ast'] = (df['ut1'] - df['ut1_astropy']) * 86400
plt.plot(df['year'].values, df['d_me_ast'].values)
plt.grid(True)
plt.show()

# astropy deos not support UT1 before 1960
