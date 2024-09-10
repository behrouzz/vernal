import numpy as np
import pandas as pd
from iers import EOP, historic_ut1_tt
from .coordinates import true_sun
from .time import et2jd


def do_loop(et_guess, delta_df, eop):
    et_i = et_guess - (86400*5)
    et_f = et_guess + (86400*5)
    while (et_f - et_i) > 1e-3:
        rng = np.linspace(et_i, et_f, 3)
        dec = np.zeros((2,))
        for i, et in enumerate([rng[:2].mean(), rng[1:].mean()]):
            dec[i] = true_sun(et, delta_df, eop)
        if abs(dec[0]) < abs(dec[1]):
            et_f = (et_i + et_f) / 2
        else:
            et_i = (et_i + et_f) / 2
    et = np.interp(0, dec, np.array([rng[:2].mean(), rng[1:].mean()]))
    return et


def go(n, back, delta_df=None, eop=None):
    if delta_df is None:
        delta_df = historic_ut1_tt()
    if eop is None:
        eop = EOP() #deghat baraye qadimi ha*******
    y0 = 6809764.971984705 #2000
    year_length = 365.25*86400
    if back:
        year_length *= -1
    times = np.zeros((n,))
    for i in range(n):
        y1 = do_loop(y0 + year_length, delta_df, eop)
        times[i] = y1
        year_length = y1 - y0
        y0 = y1
    return times


def get_df(n, back=True):
    #1380=2001
    times = go(n, back=back)
    df = pd.DataFrame({'et':times})
    df['TDBjd'] = df['et'].apply(lambda x: et2jd(x))
    if back:
        df['persian'] = np.arange(1380, 1380-len(df), -1)
    else:
        df['persian'] = np.arange(1380, 1380+len(df), 1)
    df['gregorian'] = df['persian'] + 621
    #df['diff'] = df['et'].diff() - (365*86400)
    return df
