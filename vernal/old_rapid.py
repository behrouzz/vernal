"""
RAPID
=====
Should only be used for rapid or longterm calculations
"""

import erfa
import numpy as np
import spiceypy as sp
from .time import jd2et

KM2AU = 1 / 149597870.7

def get_sun_gcrs(et, abcorr='LT'):
    state, lt = sp.spkez(targ=10, et=et, ref='J2000', abcorr=abcorr, obs=399)
    p_sun_gcrs, _, _ = state[:3], state[3:], lt
    p_sun_gcrs = state[:3] * KM2AU
    return p_sun_gcrs


def gcrs_to_mean_equator(epj, p_gcrs):
    #r = erfa.ltp(epj) #without ICRS frame bias
    r = erfa.ltpb(epj) #with ICRS frame bias
    p_mean_equator = erfa.rxp(r, p_gcrs)
    return p_mean_equator


def mean_sun(epj):
    tt1, tt2 = erfa.epj2jd(epj)
    et = jd2et(tt1+tt2)
    p_sun_gcrs = get_sun_gcrs(et, abcorr='LT')
    p_sun_mean = gcrs_to_mean_equator(epj, p_sun_gcrs)
    _, dec = erfa.c2s(p_sun_mean)
    return dec


def do_loop(year):
    epj = year + 0.216 #about 20 March instead of 1 Jan
    dt = 0.1 #0.1 = 45 days
    ep_i = epj - dt
    ep_f = epj + dt
    while (ep_f - ep_i) > 3.2e-8: #1 sec
        rng = np.linspace(ep_i, ep_f, 3)
        dec = np.zeros((2,))
        for i, ep in enumerate([rng[:2].mean(), rng[1:].mean()]):
            dec[i] = mean_sun(ep)
        if abs(dec[0]) < abs(dec[1]):
            ep_f = (ep_i + ep_f) / 2
        else:
            ep_i = (ep_i + ep_f) / 2
    ep = np.interp(0, dec, np.array([rng[:2].mean(), rng[1:].mean()]))
    tt1, tt2 = erfa.epj2jd(ep)
    return tt1 + tt2
