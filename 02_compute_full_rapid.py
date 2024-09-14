import pandas as pd
import spiceypy as sp
from vernal.rapid import df2000_to_year, refine
from vernal.time import jd2et, et2jd


sp.furnsh('vernal/data/ker/historic_h21.tm')

def refine_df(rot_kind):
    df = pd.read_csv(f'vernal/data/de441/{rot_kind}.csv')
    df['et_i'] = df['tdb'].apply(lambda x: jd2et(x))
    df['et_ref'] = df['et_i'].apply(lambda x: refine(x, rot_kind=rot_kind, dt=1800, n=20))
    del df['tdb']
    df['tdb'] = df['et_ref'].apply(lambda x: et2jd(x))
    return df[['year', 'tdb']]


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

# sofa_bpn
# ----------------------------------------------------------
##df = df2000_to_year(-13198, dt=2, rot_kind='sofa_bpn')
##df.set_index('year').to_csv('vernal/data/de441/pre_sofa_bpn.csv')

##df = df2000_to_year(17189, dt=2, rot_kind='sofa_bpn')
##df.set_index('year').to_csv('vernal/data/de441/post_sofa_bpn.csv')

##df1 = pd.read_csv('vernal/data/de441/pre_sofa_bpn.csv')
##df2 = pd.read_csv('vernal/data/de441/post_sofa_bpn.csv')
##df = pd.concat([df1.iloc[:-1], df2], axis=0, ignore_index=True)
##df.set_index('year').to_csv('vernal/data/de441/sofa_bpn.csv')

#====================================================================

# REFINE
# ======
##for rot_kind in ['spice_tete', 'sofa_mean', 'sofa_bpn']:
##    df = refine_df(rot_kind)
##    df.set_index('year').to_csv(f'vernal/data/de441/{rot_kind}.csv')
##    print(rot_kind, 'created!')

sp.kclear()
