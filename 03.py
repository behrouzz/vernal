import spiceypy as sp

def guess_et_ver(y):
    """
    Guess an initial value for vernal equinox for given year

    Argument:
        y (int): Gregorian year
    Returns:
        et_guess (float): time of vernal equinox (et)
    """
    et2000ver = 6809764.971984705
    dy = y - 2000
    et_guess = et2000ver + (dy * 365.25 * 86400)
    return et_guess

sp.furnsh('k_1600_2600.tm')


for y in [*range(2000, -2100, -100)]:
    print(y)
    
    et_guess = guess_et_ver(y)
    print(et_guess)
    if y > 0:
        yyyy = str(y) + ' A.D. Mar 20 12:00:00 TDB'
    else:
        yyyy = str(abs(y)+1) + ' B.C. Mar 20 12:00:00 TDB'
    a = sp.str2et(yyyy)
    print(a)

    print((et_guess - a)/3600, 'hours')
    print('-'*70)

##a = sp.str2et('1 A.D. Mar 20 12:00:00 TDB')#-63075542400.0
##b = sp.str2et('0 A.D. Mar 20 12:00:00 TDB')#-63107078400.0
##c = sp.str2et('0 B.C. Mar 20 12:00:00 TDB')#-63075542400.0
##d = sp.str2et('1 B.C. Mar 20 12:00:00 TDB')#-63107078400.0


# NOTE:
# Initial guess can be deviated up to 31 days until year 2000 B.C

sp.kclear()


