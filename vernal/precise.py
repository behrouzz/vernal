"""
PRECISE
=======
Should only be used for rapid or longterm calculations

Uses two kinds of rotation matrix:
 - 'sofa_mean'
 - 'sofa_bpn'
"""

import erfa
import numpy as np
import pandas as pd
import spiceypy as sp
from .time import jd2et, et2jd, guess_et_ver, tt2et
from .tools import *

KM2AU = 1 / 149597870.7


def pos_sun_gcrs(et):
    state, _ = sp.spkez(targ=10, et=et, ref='J2000', abcorr='LT+S', obs=399)
    return state[:3]


##def rotmat(tt, rot_kind):
##    if rot_kind=='sofa_mean':
##        #tt = et2jd(et) #should think!
##        epj = erfa.epj(2400000.5, tt-2400000.5)
##        r = erfa.ltpb(epj) #with ICRS frame bias
##    elif rot_kind=='sofa_bpn':
##        r = erfa.pnm06a(2400000.5, tt-2400000.5)
##    else:
##        raise Exception('Not valid values for rot_kind!')
##    return r


def polar_motion_matrix(xp, yp):
    pom = erfa.ir()
    pom = erfa.ry(-xp, pom)
    pom = erfa.rx(-yp, pom)
    return pom


def gcrs_to_mean_equator(tt, p_gcrs):
    tt1, tt2 = 2400000.5, tt-2400000.5
    r = erfa.pmat06(tt1, tt2)
    p_mean_equator = erfa.rxp(r, p_gcrs)
    return p_mean_equator


def gcrs_to_true_equator(tt, p_gcrs, ut, eop=None, polar_motion=True):
    tt1, tt2 = 2400000.5, tt-2400000.5
    x, y = erfa.xy06(tt1, tt2)
    if eop is not None:
        dc = eop.get_eop(ut)
        xp = dc['px'] * erfa.DAS2R
        yp = dc['py'] * erfa.DAS2R
        dx = dc['dx'] * erfa.DMAS2R
        dy = dc['dy'] * erfa.DMAS2R
        x += dx
        y += dy
    s = erfa.s06(tt1, tt2, x, y)
    bpn = erfa.c2ixys(x, y, s) #givec CIRS
    if polar_motion and (eop is not None):
        pom = polar_motion_matrix(xp, yp)
        r = erfa.rxr(pom, bpn)
    else:
        r = bpn
    p_true_equator = erfa.rxp(r, p_gcrs)
    return p_true_equator


def dec_true_sun(tt, rot_kind, delta_df, eop=None):
    et = tt2et(tt)
    p_sun_gcrs = pos_sun_gcrs(et)
    if 'mean' in rot_kind.lower():
        p_sun_true = gcrs_to_mean_equator(tt, p_sun_gcrs)
    elif 'tete' in rot_kind.lower():
        ut1 = tt2ut1(tt, delta_df)
        p_sun_true = gcrs_to_true_equator(tt, p_sun_gcrs, ut1, eop, polar_motion=True)
    _, dec = erfa.c2s(p_sun_true)
    return dec

##
##def verify(tdb, dt, rot_kind):
##    et = jd2et(tdb)
##    f = lambda et: dec_true_sun(et, rot_kind)
##    return do_verify(et, f, dt)
##
##def loop(et_guess, dt, rot_kind):
##    f = lambda et: dec_true_sun(et, rot_kind)
##    return do_loop(et_guess, f, dt)
##
##
##def refine(et, rot_kind, dt=1800, n=100):
##    et1 = et - dt
##    et2 = et + dt
##    ets = np.linspace(et1, et2, n)
##    dec = np.zeros((len(ets),))
##    for i, et_ in enumerate(ets):
##        dec[i] = dec_true_sun(et_, rot_kind)
##    coefs = np.polyfit(ets, dec, 1)
##    return np.roots(coefs)[0]

    
