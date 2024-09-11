import spiceypy as sp
import numpy as np
from vernal.time import et2jd
from vernal.rapid import from2000
import pandas as pd


sp.furnsh('vernal/data/ker/historic.tm')

years = np.arange(2000, 17190, 1)

times = from2000(n=len(years), back=False, dt=150, true_equator=True)
tt = et2jd(times)

df = pd.DataFrame({'year':years, 'tt':tt})
df.set_index('year').to_csv('vernal/data/future_TETEp1976n1980.csv')

sp.kclear()
