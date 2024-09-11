"""
RAPID
=====
Should only be used for rapid or longterm calculations
"""

import erfa
import numpy as np
import pandas as pd
import spiceypy as sp
from .time import jd2et, et2jd, guess_et_ver

KM2AU = 1 / 149597870.7

def get_sun_gcrs(et, abcorr):
    state, lt = sp.spkez(targ=10, et=et, ref='J2000', abcorr=abcorr, obs=399)
    p_sun_gcrs, _, _ = state[:3], state[3:], lt
    p_sun_gcrs = state[:3] * KM2AU
    return p_sun_gcrs


def gcrs_to_mean_equator(et, p_gcrs):
    tt = et2jd(et)
    epj = erfa.epj(2400000.5, tt-2400000.5)
    #r = erfa.ltp(epj) #without ICRS frame bias
    r = erfa.ltpb(epj) #with ICRS frame bias
    p_mean_equator = erfa.rxp(r, p_gcrs)
    return p_mean_equator


def dec_mean_sun(et):
    #tt1, tt2 = erfa.epj2jd(epj)
    #et = jd2et(tt1+tt2)
    p_sun_gcrs = get_sun_gcrs(et, abcorr='LT+S')
    p_sun_mean = gcrs_to_mean_equator(et, p_sun_gcrs)
    _, dec = erfa.c2s(p_sun_mean)
    return dec


def do_loop(et_guess, dt):
    #dt = 50 #t=35 for long time until B.C. 2000
    et_i = et_guess - (86400*dt)
    et_f = et_guess + (86400*dt)
    while (et_f - et_i) > 1e-3: #1e-6 for high precision
        rng = np.linspace(et_i, et_f, 3)
        dec = np.zeros((2,))
        for i, et in enumerate([rng[:2].mean(), rng[1:].mean()]):
            dec[i] = dec_mean_sun(et)
        if abs(dec[0]) < abs(dec[1]):
            et_f = (et_i + et_f) / 2
        else:
            et_i = (et_i + et_f) / 2
    et = np.interp(0, dec, np.array([rng[:2].mean(), rng[1:].mean()]))
    return et


def vernal_equinox(year, dt=100):
    et_guess = guess_et_ver(year)
    et_ver = do_loop(et_guess, dt)
    return et_ver


def from2000(n, back, dt):
    y0 = 6809764.971984705 #2000et
    year_length = 365.25*86400
    if back:
        year_length = -1 * year_length
    times = np.zeros((n,))
    times[0] = y0
    for i in range(n-1):
        y1 = do_loop(y0 + year_length, dt)
        times[i+1] = y1
        year_length = y1 - y0
        y0 = y1
    return times


##def from2000_backward(n, dt):
##    y0 = 6809764.971984705 #2000et
##    year_length = -365.25*86400
##    times = np.zeros((n,))
##    for i in range(n):
##        y1 = do_loop(y0 + year_length, dt)
##        times[i] = y1
##        year_length = y1 - y0
##        y0 = y1
##    return times




##def get_df(y1, y2, dt=100):
##    if y1 > y2:
##        y1, y2 = y2, y1
##    years = np.arange(y2, y1-1, -1)
##    tt = np.zeros((len(years),))
##    for i, y in enumerate(years):
##        tt[i] = et2jd(vernal_equinox(y, dt))
##    df = pd.DataFrame({'year':years, 'tt':tt})
##    #persian = years - 621
##    return df
    
