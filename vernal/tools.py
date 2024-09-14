import numpy as np

dc_season = {
    1: 'spring',
    2: 'summer',
    3: 'autumn',
    4: 'winter',
    5: 'march equinox',
    6: 'september equinox',
    7: 'june solstice',
    8: 'december solstice'
    }


def do_loop(et_guess, func_true_sun, dt):
    et_i = et_guess - (86400*dt)
    et_f = et_guess + (86400*dt)
    dec1 = func_true_sun(et_i)
    dec2 = func_true_sun(et_f)
    if dec1 > dec2:
        raise Exception('Bad initial et_guess!')
    elif abs(dec1) < abs(dec2):
        et_f = (et_i + et_f) / 2
    else:
        et_i = (et_i + et_f) / 2
        
    while True:
        dec1 = func_true_sun(et_i)
        dec2 = func_true_sun(et_f)
        if (et_f - et_i) < 1e-3:
            break
        if dec1 > dec2:
            raise Exception('Bad initial et_guess!')
        elif abs(dec1) < abs(dec2):
            et_f = (et_i + et_f) / 2
        else:
            et_i = (et_i + et_f) / 2
    et = np.interp(0, [dec1, dec2], [et_i, et_f])
    return et


def do_get_season(et, func_true_sun):
    #dec = dec_true_sun(et, 'sofa_bpn')
    dec = func_true_sun(et)
    if dec > 0:
        seasons = set([1, 2])
    elif dec < 0:
        seasons = set([3, 4])
    else:
        seasons = set([5, 6]) #1far or 1mehr
        
    #dec1 = dec_true_sun(et-5, 'sofa_bpn')
    #dec2 = dec_true_sun(et+5, 'sofa_bpn')
    dec1 = func_true_sun(et-5)
    dec2 = func_true_sun(et+5)
    if dec1 < dec2:
        season = set([1, 4]) & seasons
    elif dec1 > dec2:
        season = set([2, 3]) & seasons
    else:
        season = set([7, 8]) & seasons #1tir or 1dey 
    return season


def do_verify(et, func_true_sun, dt):
    verified = False
    et1 = et - dt
    et2 = et + dt
    dec1 = func_true_sun(et1)
    dec2 = func_true_sun(et2)
    if (dec1 < 0) and (dec2 > 0):
        verified = True
    return verified
