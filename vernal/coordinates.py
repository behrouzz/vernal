import erfa
import numpy as np
import spiceypy as sp
from .time import et2tt, tt2ut1

KM2AU = 1 / 149597870.7
KMpS2AUpD = 0.0005775483273639937


def true_sun_spice_inner(et):
    rotmat = sp.sxform('J2000', 'TETE', et)[:3,:3]
    pos, _ = sp.spkez(10, et, 'J2000', 'LT+S', 399)
    sunJ2000 = pos[:3] #GCRS
    sun = np.matmul(rotmat, sunJ2000)
    ra, dec = erfa.c2s(sun)
    return dec


def get_earth(et):
    """
    Heliocentric and Barycentric position-velocity of Earth
    """
    
    state, lt = sp.spkez(targ=10, et=et, ref='J2000', abcorr='NONE', obs=0)
    pb_sun, vb_sun, lt_sun = state[:3], state[3:], lt

    state, lt = sp.spkez(targ=399, et=et, ref='J2000', abcorr='NONE', obs=10)
    ph_ear, vh_ear, lth_ear = state[:3]*KM2AU, state[3:]*KMpS2AUpD, lt

    state, lt = sp.spkez(targ=399, et=et, ref='J2000', abcorr='NONE', obs=0)
    pb_ear, vb_ear, ltb_ear = state[:3]*KM2AU, state[3:]*KMpS2AUpD, lt

    # Return results adapted to SOFA epv00 format
    pvh = np.array([ph_ear, vh_ear])
    pvb = np.array([pb_ear, vb_ear])

    return pvh, pvb


def apply_aberration(et, p_gcrs):
    pvh, pvb = get_earth(et)
    v = pvb[1] / erfa.DC
    em = np.sum(pvh[0]**2) ** 0.5
    bm1 = np.sqrt(1 - np.sum(v**2))
    p_gcrs_ab = erfa.ab(p_gcrs, v, em, bm1)
    return p_gcrs_ab


def polar_motion_matrix(xp, yp):
    pom = erfa.ir()
    pom = erfa.ry(-xp, pom)
    pom = erfa.rx(-yp, pom)
    return pom


def get_sun_gcrs(et, abcorr='LT+S'):
    if abcorr.lower()=='sofa':
        abcorr = 'NONE'
        ab = True
    else:
        ab = False
    state, lt = sp.spkez(targ=10, et=et, ref='J2000', abcorr=abcorr, obs=399)
    p_sun_gcrs, _, lt_sun_gcrs = state[:3], state[3:], lt
    p_sun_gcrs *= KM2AU
    if ab:
        p_sun_gcrs = apply_aberration(et, p_sun_gcrs)
    return p_sun_gcrs, lt_sun_gcrs


def gcrs_to_true_equator(tt, pos_gcrs, utc, eop=None, polar_motion=True):
    x, y = erfa.xy06(tt, 0.0)
    if eop is not None:
        dc = eop.get_eop(utc)
        xp = dc['px'] * erfa.DAS2R
        yp = dc['py'] * erfa.DAS2R
        dx = dc['dx'] * erfa.DMAS2R
        dy = dc['dy'] * erfa.DMAS2R
        x += dx
        y += dy
    else:
        x, y = 0, 0 #deghat: eshtebah!
    s = erfa.s06(tt, 0.0, x, y)
    bpn = erfa.c2ixys(x, y, s) #givec CIRS
    if polar_motion and (eop is not None):
        pom = polar_motion_matrix(xp, yp)
        r = erfa.rxr(pom, bpn)
    else:
        r = bpn
    pos_true_equator = erfa.rxp(r, pos_gcrs)
    return pos_true_equator


def true_sun(et, delta_df, eop):
    tt = et2tt(et)
    p_sun_gcrs, _ = get_sun_gcrs(et, abcorr='LT+S')
    ut1 = tt2ut1(tt, delta_df)
    p_sun_true = gcrs_to_true_equator(tt, p_sun_gcrs, ut1, eop, polar_motion=True)
    _, dec, _ = erfa.p2s(p_sun_true)
    return dec
