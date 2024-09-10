import vernal as ver
from vernal.time import tt2ut1
import spiceypy as sp


sp.furnsh('k_1600_2600.tm')
df = ver.get_df(200, back=True)
#a = ver.rapid_vernal_equinox(2024)
sp.kclear()

df['ut1'] = tt2ut1(df['tt'])
print(df)

#df = df[df['gregorian']>=1962]


##import matplotlib.pyplot as plt
##from astropy.time import Time
##t = Time(df.tt.values, scale='tt', format='jd')
##
##fig, ax = plt.subplots()
##ax.plot(df['gregorian'].values, (df['tt'] - df['ut1']).values, c='b')
##ax.plot(df['gregorian'].values, t.tt.value - t.ut1.value, c='r')
##plt.show()


