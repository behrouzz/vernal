import numpy as np
import pandas as pd
from iers import EOP, historic_ut1_tt
from .coordinates import true_sun
from .time import et2tt, et2jd, guess_et_ver


def do_loop(et_guess, delta_df, eop):
    dt = 5 #t=35 for long time until B.C. 2000
    et_i = et_guess - (86400*dt)
    et_f = et_guess + (86400*dt)
    while (et_f - et_i) > 1e-3: #1e-6 for high precision
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


def find_eop_kind(mjd):
    eop_kind = 1
    if (mjd <= 41684) and (eop_kind==1):
        eop_kind = 2
    elif (mjd <= 37665) and (eop_kind==2):
        eop_kind = 3
    elif (mjd <= -4703.268) and (eop_kind==3):
        eop_kind = 0
    return eop_kind


def rapid_vernal_equinox(year):
    delta_df = historic_ut1_tt()
    et_guess = guess_et_ver(year)
    mjd_guess = et2jd(et_guess) - 2400000.5
    k = find_eop_kind(mjd_guess)
    eop = EOP(k)
    et = do_loop(et_guess, delta_df, eop)
    return et


def go(n, back, delta_df=None, eop=None):
    if delta_df is None:
        delta_df = historic_ut1_tt()
    if eop is None:
        eop = EOP()
    eop_kind = 1
    y0 = 6809764.971984705 #2000et
    year_length = 365.25*86400
    if back:
        year_length *= -1
    times = np.zeros((n,))
    for i in range(n):
        if (y0 <= 41684 + 2400000.5) and (eop_kind==1):
            eop = EOP(2)
            eop_kind = 2
        elif (y0 <= 37665 + 2400000.5) and (eop_kind==2):
            eop = EOP(3)
            eop_kind = 3
        elif (y0 <= -4703.268 + 2400000.5) and (eop_kind==3):
            eop = None
            eop_kind = 0
        y1 = do_loop(y0 + year_length, delta_df, eop)
        times[i] = y1
        year_length = y1 - y0
        y0 = y1
    return times


def get_df(n, back=True):
    #1380=2001
    times = go(n, back=back)
    df = pd.DataFrame({'et':times})
    df['tt'] = df['et'].apply(lambda x: et2tt(x))
    if back:
        df['persian'] = np.arange(1380, 1380-len(df), -1)
    else:
        df['persian'] = np.arange(1380, 1380+len(df), 1)
    df['gregorian'] = df['persian'] + 621
    return df
