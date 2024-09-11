import numpy as np
import erfa
import spiceypy as sp
from iers import historic_ut1_tt


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

def et2tt(et): #should think about 1
    tt1 = et2jd(et - 1)
    tt2 = et2jd(et + 1)
    et1 = tt2et(tt1)
    et2 = tt2et(tt2)
    tt = np.interp(et, [et1, et2], [tt1, tt2])
    return tt

def tt2tdb(tt):
    et = tt2et(tt)
    tdb = et2jd(et)
    return tdb

def tdb2tt(tdb):
    et = jd2et(tdb)
    tt = et2tt(et)
    return tt


def tt2ut1(tt, delta_df=None):
    if delta_df is None:
        delta_df = historic_ut1_tt()
    elif 'ut1_tt' not in delta_df.columns:
        delta_df['ut1_tt'] = delta_df['ut1_tai'] - 32.184
    delta_df['tt'] = delta_df['mjd'] - (delta_df['ut1_tt']/86400)
    ttMJD = tt - 2400000.5
    ut1Mjd = np.interp(ttMJD, delta_df['tt'], delta_df['mjd'])
    ut1 = ut1Mjd + 2400000.5
    return ut1


##def guess_et_ver(y):
##    et2000ver = 6809769.449749
##    dy = y - 2000
##    et_guess = et2000ver + (dy * 365.25 * 86400)
##    return et_guess


def guess_et_ver(y):
    """
    Guess an initial value for vernal equinox for given year

    Argument:
        y (int): Gregorian year
    Returns:
        et_guess (float): time of vernal equinox (et)
    """
    if y > 7000:
        et0 = 4277836.203775127
        dy = y - 7000
    elif y < -7000:
        et0 = -835554.3652559691
        dy = y + 7000
    else:
        et0 = 6809769.449749
        dy = y - 2000
    et_guess = et0 + (dy * 365.25 * 86400)
    return et_guess



def sofa_time(t):
    utc1, utc2 = erfa.dtf2d('UTC', t.year, t.month, t.day, t.hour, t.minute, t.second + (t.microsecond / 1e6))
    tai1, tai2 = erfa.utctai(utc1, utc2)
    tt1, tt2 = erfa.taitt(tai1, tai2)
    return utc1, utc2, tt1, tt2
