import pandas as pd
from vernal.rapid import dec_true_sun
from vernal.time import jd2et, et2jd
import spiceypy as sp

def is_wrong(tdb, rot_kind, dt):
    problem = False
    et1 = jd2et(tdb) - dt
    et2 = jd2et(tdb) + dt
    dec1 = dec_true_sun(et1, rot_kind)
    dec2 = dec_true_sun(et2, rot_kind)
    if (dec1 > 0) or (dec2 < 0):
        problem = True
        print(tdb)
        print([dec1, dec2])
    return problem


sp.furnsh('vernal/data/ker/historic.tm')

rot_kind = 'sofa_bpn'

df = pd.read_csv(f'vernal/data/de441/{rot_kind}.csv')

for i, v in df.iterrows():
    if is_wrong(v['tdb'], rot_kind, dt=1):
        print(v['year'])
        print('-'*50)


sp.kclear()
