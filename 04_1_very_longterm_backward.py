import pandas as pd
import spiceypy as sp
from vernal.rapid import df2000_to_year


sp.furnsh('vernal/data/ker/historic.tm')


# spice_tete
# ----------
##df = df2000_to_year(-13198, dt=2, rot_kind='spice_tete')
##df.set_index('year').to_csv('vernal/data/pre_spice_tete.csv')

df = df2000_to_year(17189, dt=2, rot_kind='spice_tete')
df.set_index('year').to_csv('vernal/data/post_spice_tete.csv')

# sofa_mean
# ----------


# sofa_tete
# ----------


sp.kclear()
