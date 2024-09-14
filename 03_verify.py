import pandas as pd
from vernal.rapid import verify
import spiceypy as sp


sp.furnsh('vernal/data/ker/historic_h21.tm')

rot_kind = 'sofa_bpn'

df = pd.read_csv(f'vernal/data/de441/{rot_kind}.csv')
df = df.head()

for i, v in df.iterrows():
    if not verify(v['tdb'], dt=1, rot_kind=rot_kind):
        print(v['year'])
        print('-'*50)

sp.kclear()
