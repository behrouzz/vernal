import numpy as np
import pandas as pd
from vernal import get_table
from vernal.time import tt2ut1, tdb2tt
from vernal.precise import dec_true_sun
from iers import EOP, historic_ut1_tt
import matplotlib.pyplot as plt


delta_df = historic_ut1_tt()

import spiceypy as sp

sp.furnsh('vernal/data/ker/historic.tm')

y1, y2 = 1990, 2000

df = get_table(y1=y1, y2=y2, rot_kind='sofa_mean')
df['per'] = df['year'] - 621
df['ut1'] = tt2ut1(df['tdb'].values)
df['ut1ir'] = df['ut1']  + (3.5/24)
sp.kclear()


df['am_pm'] = ''
df.loc[(df['ut1ir'] % 1) <= 0.5, 'am_pm'] = 'PM'
df.loc[(df['ut1ir'] % 1) > 0.5, 'am_pm'] = 'AM'

##from astropy.time import Time
##t = df['ut1ir'].iloc[-1]
##t = Time(t, scale='ut1', format='jd')

"""
if fraction < 0.5: vernal in afternoon
if fraction > 0.5: vernal in morning
"""
