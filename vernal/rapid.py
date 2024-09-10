"""
RAPID
=====
Should only be used for rapid or longterm calculations
"""

import erfa
import spiceypy as sp

KM2AU = 1 / 149597870.7

def get_sun_gcrs(et, abcorr='LT'):
    state, lt = sp.spkez(targ=10, et=et, ref='J2000', abcorr=abcorr, obs=399)
    p_sun_gcrs, _, _ = state[:3], state[3:], lt
    p_sun_gcrs = state[:3] * KM2AU
    return p_sun_gcrs


def gcrs_to_mean_equator(epj, p_gcrs):
    r = erfa.ltpb(epj)
    p_mean_equator = erfa.rxp(r, p_gcrs)
    return p_mean_equator
