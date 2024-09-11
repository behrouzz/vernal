# length of year 2177 is less than 364 days!

import pandas as pd
import matplotlib.pyplot as plt
import spiceypy as sp
from vernal.rapid import do_loop

sp.furnsh('vernal/data/ker/historic.tm')

et1 = 5560947369.450127
et2 = 5592388111.848206

kinds = ['spice_tete', 'sofa_bpn', 'sofa_mean']

for rot_kind in kinds:
    ver1 = do_loop(et1, dt=150, rot_kind=rot_kind)
    ver2 = do_loop(et2, dt=150, rot_kind=rot_kind)
    dt = (ver2 - ver1) / 86400
    print(rot_kind, dt)

sp.kclear()
