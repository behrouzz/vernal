import pandas as pd
import spiceypy as sp
from vernal.rapid import df2000_to_year


sp.furnsh('vernal/data/ker/historic_h21.tm')


# spice_tete
# ----------------------------------------------------------
##df = df2000_to_year(-13198, dt=2, rot_kind='spice_tete')
##df.set_index('year').to_csv('vernal/data/de441/pre_spice_tete.csv')

##df = df2000_to_year(17189, dt=2, rot_kind='spice_tete')
##df.set_index('year').to_csv('vernal/data/de441/post_spice_tete.csv')

##df1 = pd.read_csv('vernal/data/de441/pre_spice_tete.csv')
##df2 = pd.read_csv('vernal/data/de441/post_spice_tete.csv')
##df = pd.concat([df1.iloc[:-1], df2], axis=0, ignore_index=True)
##df.set_index('year').to_csv('vernal/data/de441/spice_tete.csv')

# sofa_mean
# ----------------------------------------------------------
##df = df2000_to_year(-13198, dt=2, rot_kind='sofa_mean')
##df.set_index('year').to_csv('vernal/data/de441/pre_sofa_mean.csv')

##df = df2000_to_year(17189, dt=2, rot_kind='sofa_mean')
##df.set_index('year').to_csv('vernal/data/de441/post_sofa_mean.csv')

##df1 = pd.read_csv('vernal/data/de441/pre_sofa_mean.csv')
##df2 = pd.read_csv('vernal/data/de441/post_sofa_mean.csv')
##df = pd.concat([df1.iloc[:-1], df2], axis=0, ignore_index=True)
##df.set_index('year').to_csv('vernal/data/de441/sofa_mean.csv')

# sofa_tete
# ----------------------------------------------------------
##df = df2000_to_year(-13198, dt=2, rot_kind='sofa_bpn')
##df.set_index('year').to_csv('vernal/data/de441/pre_sofa_bpn.csv')

##df = df2000_to_year(17189, dt=2, rot_kind='sofa_bpn')
##df.set_index('year').to_csv('vernal/data/de441/post_sofa_bpn.csv')

##df1 = pd.read_csv('vernal/data/de441/pre_sofa_bpn.csv')
##df2 = pd.read_csv('vernal/data/de441/post_sofa_bpn.csv')
##df = pd.concat([df1.iloc[:-1], df2], axis=0, ignore_index=True)
##df.set_index('year').to_csv('vernal/data/de441/sofa_bpn.csv')

sp.kclear()
