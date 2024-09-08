import numpy as np
import erfa
import spiceypy as sp


J2000 = 2451545

def et2jd(et):
    jd = J2000 + (et / 86400)
    return jd

def jd2et(jd):
    et = (jd - J2000) * 86400
    return et

def tt2et(tt):
    tt = format(tt, '.50f')# for very small numbers
    et = sp.str2et(f'JD {tt} TDT')
    return et

def et2tt(et):
    et1JD = et2jd(et - (86400 * 1))
    et2JD = et2jd(et + (86400 * 1))
    et1 = tt2et(et1JD)
    et2 = tt2et(et2JD)
    tt = np.interp(et, [et1, et2], [et1JD, et2JD])
    return tt

def tt2tdb(tt):
    et = tt2et(tt)
    tdb = et2jd(et)
    return tdb

def tdb2tt(tdb):
    et = jd2et(tdb)
    tt = et2tt(et)
    return tt


def sofa_time(t):
    utc1, utc2 = erfa.dtf2d('UTC', t.year, t.month, t.day, t.hour, t.minute, t.second + (t.microsecond / 1e6))
    tai1, tai2 = erfa.utctai(utc1, utc2)
    tt1, tt2 = erfa.taitt(tai1, tai2)
    return utc1, utc2, tt1, tt2
