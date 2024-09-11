import spiceypy as sp
import numpy as np
from vernal.time import et2jd
from vernal.rapid import vernal_equinox, from2000
import pandas as pd
#epj(dj1, dj2)
#epj2jd(epj)
#erfa.ltpb(epj)

#BASE = 'C:/Moi/_py/Astronomy/Solar System/kernels/'
BASE = 'C:/Users/H21/Desktop/Desktop/Behrouz/Astronomy/kernels/'
kernels = [
    'naif0012.tls', 'pck00010.tpc', 'earth_latest_high_prec.bpc',
    'de441_part-1.bsp', 'de441_part-2.bsp'
    ]
kernels = [BASE + i for i in kernels]

for k in kernels:
    sp.furnsh(k)

#df = get_df(17190, -13199, dt=150)

years = np.arange(2000, -13199, -1)

times = from2000(n=len(years), back=True, dt=150)
tt = et2jd(times)



df = pd.DataFrame({'year':years, 'tt':tt})
df.set_index('year').to_csv('vernal/data/pre_historic.csv')

sp.kclear()
