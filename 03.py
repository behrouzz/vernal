import vernal as ver
from vernal.time import et2tt, tt2ut1
import spiceypy as sp
import matplotlib.pyplot as plt
import numpy as np


sp.furnsh('k_1600_2600.tm')
df = ver.get_df(20, back=True)
df['tt'] = df['et'].apply(lambda x: et2tt(x))
sp.kclear()


from astropy.time import Time
t = Time(df['tt'].values, scale='tt', format='jd')

fig, ax = plt.subplots()
ax.scatter(df['gregorian'], df['TDBjd'] - df['tt'], c='b')
ax.scatter(df['gregorian'], t.tdb.value - t.tt.value, c='r')
plt.show()


#df['tdb_tt'] = (df['TDBjd'] - df['tt'])

