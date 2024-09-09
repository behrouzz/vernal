import vernal as ver
from vernal.time import et2tt, tt2ut1Arr
import spiceypy as sp


sp.furnsh('k_1600_2600.tm')
df = ver.get_df(400, back=True)
df['tt'] = df['et'].apply(lambda x: et2tt(x))
sp.kclear()

print(df)

print('==== Calculating UT1 ====')
df['ut1'] = tt2ut1Arr(df['tt'])
print(df)

###df = df[df['gregorian']>=1962]
##
##
##import matplotlib.pyplot as plt
##from astropy.time import Time
##t = Time(df.tt.values, scale='tt', format='jd')
##
##fig, ax = plt.subplots()
##ax.plot(df['gregorian'].values, (df['tt'] - df['ut1']).values, c='b')
##ax.plot(df['gregorian'].values, t.tt.value - t.ut1.value, c='r')
##plt.show()


