import erfa
import spiceypy as sp
import numpy as np
from vernal.time import jd2et
from vernal.rapid import get_sun_gcrs, gcrs_to_mean_equator

#epj(dj1, dj2)
#epj2jd(epj)
#erfa.ltpb(epj)

BASE = 'C:/Moi/_py/Astronomy/Solar System/kernels/'
#BASE = 'C:/Users/H21/Desktop/Desktop/Behrouz/Astronomy/kernels/'
kernels = [
    'naif0012.tls', 'pck00010.tpc', 'earth_latest_high_prec.bpc',
    'de441_part-1.bsp', 'de441_part-2.bsp'
    ]
kernels = [BASE + i for i in kernels]

for k in kernels:
    sp.furnsh(k)

for y in [*range(2000, -13000, -100)]:
    epj = y + 0.216 #about 20 March instead of 1 Jan
    tt1, tt2 = erfa.epj2jd(epj)
    et = jd2et(tt1+tt2)
    sun_gcrs = get_sun_gcrs(et, abcorr='LT')
    mean_sun = gcrs_to_mean_equator(epj, sun_gcrs)
    _, dec = erfa.c2s(mean_sun)
    print(y, dec*erfa.DR2D)
    


sp.kclear()
