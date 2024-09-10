import vernal as ver
from vernal.time import et2tt, tt2ut1
from vernal.coordinates import get_sun_gcrs, polar_motion_matrix
import spiceypy as sp
import erfa
from iers import EOP, historic_ut1_tt
from datetime import datetime, timedelta
import numpy as np


def gcrs_to_tete_p76n80(tt, pos_gcrs):
    r = erfa.pnm80(tt, 0)
    pos_true_equator = erfa.rxp(r, pos_gcrs)
    return pos_true_equator


def gcrs_to_tete_p76n80_pm(tt, pos_gcrs, eop):
    r = erfa.pnm80(tt, 0)

    dc = eop.get_eop(tt)
    xp = dc['px'] * erfa.DAS2R
    yp = dc['py'] * erfa.DAS2R

    pom = polar_motion_matrix(xp, yp)
    r = erfa.rxr(pom, r)

    pos_true_equator = erfa.rxp(r, pos_gcrs)
    return pos_true_equator

#gcrs_to_true_equator_p06n00
def gcrs_to_true_equator(utc, tt, pos_gcrs, eop=None, polar_motion=True):
    x, y = erfa.xy06(tt, 0.0)
    if eop is not None:
        dc = eop.get_eop(utc)
        xp = dc['px'] * erfa.DAS2R
        yp = dc['py'] * erfa.DAS2R
        dx = dc['dx'] * erfa.DMAS2R
        dy = dc['dy'] * erfa.DMAS2R
        x += dx
        y += dy
    else:
        x, y = 0, 0
    s = erfa.s06(tt, 0.0, x, y)
    bpn = erfa.c2ixys(x, y, s) #givec CIRS
    if polar_motion and (eop is not None):
        pom = polar_motion_matrix(xp, yp)
        r = erfa.rxr(pom, bpn)
    else:
        r = bpn
    pos_true_equator = erfa.rxp(r, pos_gcrs)
    return pos_true_equator



sp.furnsh('k_1600_2600.tm')


df = ver.get_df(10, back=True)
df['tt'] = df['et'].apply(lambda x: et2tt(x))
df['ut1'] = tt2ut1(df['tt'])

et = df['et'].iloc[0]
ut1 = df['ut1'].iloc[0]

delta_df = historic_ut1_tt()

dt = 400
rng = np.linspace(et-dt, et+dt, 1000)


eop = EOP()

dec = np.zeros((len(rng),))
lt = np.zeros((len(rng),))

for i, et in enumerate(rng):
    tt = et2tt(et)
    p_sun_gcrs, lt[i] = get_sun_gcrs(et, abcorr='LT+S')
    ut1 = tt2ut1(tt, delta_df)
    #p_sun_true = gcrs_to_true_equator(ut1, tt, p_sun_gcrs, eop, polar_motion=False)
    p_sun_true = gcrs_to_tete_p76n80(tt, p_sun_gcrs) #mov
    #p_sun_true = gcrs_to_tete_p76n80_pm(tt, p_sun_gcrs, eop) #mov
    _, dec[i], _ = erfa.p2s(p_sun_true)

sp.kclear()
 

et_ver = np.interp(0, dec, rng)
lt_ver = np.interp(et_ver, rng, lt)
#et_ver = et_ver + lt_ver

print(df.et.iloc[0])
print(et_ver)
d = format(df.et.iloc[0] - et_ver, '.50f')
print(d)


"""
This file shows that if we use these lines:
    rotmat = sp.sxform('J2000', 'TETE', et)[:3,:3]
    pos, _ = sp.spkez(10, et, 'J2000', 'LT+S', 399)
The SPICE will use IAU 1976 precession and 1980 nutation and also it does not
take into account polar motion.
"""





