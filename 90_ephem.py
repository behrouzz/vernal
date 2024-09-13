import pandas as pd
##from vernal.time import et2jd
import matplotlib.pyplot as plt
##import spiceypy as sp
import numpy as np
##import erfa


import ephem
#date= ephem.date((-59000,1,1))


tt = []


y1 = 1500
y2 = 2500
years = np.arange(y1, y2, 1)

d = ephem.date((y1,1,1))

for i in years:
    d = ephem.next_vernal_equinox(d)
    tt.append(d.real)

df = pd.DataFrame({'year':years, 'tt':tt})

df['d'] = df['tt'].diff()

fig, ax = plt.subplots()
ax.plot(df['year'].values, df['d'].values)
ax.ticklabel_format(useOffset=False)
plt.grid()
plt.show()
