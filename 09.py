# length of year 2177 is less than 364 days!

import pandas as pd
import matplotlib.pyplot as plt
import spiceypy as sp
from vernal.rapid import df2000_to_year
from vernal.time import et2jd, jd2et
import numpy as np

sp.furnsh('vernal/data/ker/historic.tm')

##et1 = 5560947369.450127
##et2 = 5592388111.848206


year = 2188
df = df2000_to_year(2005, dt=10, rot_kind='spice_tete')
df['d'] = df['tt'].diff()
print(df)

sp.kclear()
