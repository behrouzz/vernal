import vernal as ver
from vernal.time import et2tt
import spiceypy as sp
from iers import EOP
from iers.time import any2mjd

sp.furnsh('k_1600_2600.tm')
df = ver.get_df(100, back=True)
df['tt'] = df['et'].apply(lambda x: et2tt(x))
sp.kclear()



e = EOP(kind=3)
cnd = e.table['ut1_tai']!=99.99
tbl = e.table[cnd]
tbl['jd'] = tbl['mjd'] + 2400000.5

#ut1_tai = np.interp(mjd, df['mjd'], df['ut1_tai'])
