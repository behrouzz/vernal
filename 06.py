import pandas as pd
from vernal import initial_guess





##def vernal_equinox_of_year(year):
##    df = pd.read_csv('data/de441/sofa_bpn.csv')
##    if len(df[df['year']==year]) != 1:
##        raise Exception('Valid years: from -13198 to 17189')
##    tdb = df.loc[df['year']==year, 'tdb'].iloc[0]
##    return tdb

year = 5000
a = initial_guess(year)
