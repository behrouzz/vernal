"""
RAPID
=====
Should only be used for rapid or longterm calculations

Uses three kinds of rotation matrix:
 - 'spice_tete'
 - 'sofa_mean'
 - 'sofa_bpn'
"""

import erfa
import numpy as np
import pandas as pd
import spiceypy as sp
from .time import jd2et, et2jd, guess_et_ver
from .tools import *

KM2AU = 1 / 149597870.7




def pos_sun_gcrs(et):
    state, _ = sp.spkez(targ=10, et=et, ref='J2000', abcorr='LT+S', obs=399)
    return state[:3]


def rotmat(et, rot_kind):
    if rot_kind=='spice_tete':
        r = sp.sxform('J2000', 'TETE', et)[:3,:3]
    elif rot_kind=='sofa_mean':
        tt = et2jd(et)
        epj = erfa.epj(2400000.5, tt-2400000.5)
        r = erfa.ltpb(epj) #with ICRS frame bias
    elif rot_kind=='sofa_bpn':
        tt = et2jd(et)
        r = erfa.pnm06a(2400000.5, tt-2400000.5)
    else:
        raise Exception('Not valid values for rot_kind!')
    return r


def dec_true_sun(et, rot_kind):
    r = rotmat(et, rot_kind)
    p_sun_gcrs = pos_sun_gcrs(et)
    p_sun_true = np.matmul(r, p_sun_gcrs)
    _, dec = erfa.c2s(p_sun_true)
    return dec


def verify(tdb, dt, rot_kind):
    et = jd2et(tdb)
    f = lambda et: dec_true_sun(et, rot_kind)
    return do_verify(et, f, dt)

def loop(et_guess, dt, rot_kind):
    f = lambda et: dec_true_sun(et, rot_kind)
    return do_loop(et_guess, f, dt)


##def do_loop(et_guess, dt, rot_kind):
##    et_i = et_guess - (86400*dt)
##    et_f = et_guess + (86400*dt)
##    dec1 = dec_true_sun(et_i, rot_kind)
##    dec2 = dec_true_sun(et_f, rot_kind)
##    if dec1 > dec2:
##        raise Exception('Bad initial et_guess!')
##    elif abs(dec1) < abs(dec2):
##        et_f = (et_i + et_f) / 2
##    else:
##        et_i = (et_i + et_f) / 2
##        
##    while True:
##        dec1 = dec_true_sun(et_i, rot_kind)
##        dec2 = dec_true_sun(et_f, rot_kind)
##        if (et_f - et_i) < 1e-3:
##            break
##        if dec1 > dec2:
##            raise Exception('Bad initial et_guess!')
##        elif abs(dec1) < abs(dec2):
##            et_f = (et_i + et_f) / 2
##        else:
##            et_i = (et_i + et_f) / 2
##    et = np.interp(0, [dec1, dec2], [et_i, et_f])
##    return et


def refine(et, rot_kind, dt=1800, n=100):
    et1 = et - dt
    et2 = et + dt
    ets = np.linspace(et1, et2, n)
    dec = np.zeros((len(ets),))
    for i, et_ in enumerate(ets):
        dec[i] = dec_true_sun(et_, rot_kind)
    coefs = np.polyfit(ets, dec, 1)
    return np.roots(coefs)[0]


def from2000_to_year(n, back, dt, rot_kind):
    y0 = 6809764.971984705 #2000et
    year_length = 365.25*86400
    if back:
        year_length = -1 * year_length
    times = np.zeros((n,))
    times[0] = y0
    for i in range(n-1):
        y1 = loop(y0 + year_length, dt, rot_kind)
        times[i+1] = y1
        year_length = y1 - y0
        y0 = y1
        print(i+1)
    return times


def df2000_to_year(year, dt, rot_kind):
    if year <= 2000:
        y1 = year
        y2 = 2000
        back = True
    else:
        y1 = 2000
        y2 = year
        back = False

    years = np.arange(y1, y2+1, 1)
    times = from2000_to_year(n=len(years), back=back, dt=dt, rot_kind=rot_kind)
    tdb = et2jd(times)
    if back:
        years = years[::-1]
    df = pd.DataFrame({'year':years, 'tdb':tdb})
    df.sort_values('year', ignore_index=True, inplace=True)
    return df

#not very useful
def vernal_equinox_of_year(year, dt, rot_kind):
    et_guess = guess_et_ver(year)
    et_ver = loop(et_guess, dt, rot_kind)
    return et_ver

    
