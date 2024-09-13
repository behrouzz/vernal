import pandas as pd
import matplotlib.pyplot as plt

df1 = pd.read_csv('vernal/data/de441/spice_tete.csv')
df2 = pd.read_csv('vernal/data/de441/sofa_mean.csv')
df3 = pd.read_csv('vernal/data/de441/sofa_bpn.csv')



df = df1.copy()
df.columns = ['year', 'tdb_spice_tete']
df['tdb_sofa_mean'] = df2['tdb']
df['tdb_sofa_bpn'] = df3['tdb']

df['spice_sofa'] = df['tdb_spice_tete'] - df['tdb_sofa_bpn']
df['bpn_mean'] = df['tdb_sofa_bpn'] - df['tdb_sofa_mean']

df['d_spice_tete'] = df['tdb_spice_tete'].diff()
df['d_sofa_bpn'] = df['tdb_sofa_bpn'].diff()
df['d_sofa_mean'] = df['tdb_sofa_mean'].diff()

fig, ax = plt.subplots()
ax.plot(df['year'], df['spice_sofa'], c='b')
ax.plot(df['year'], df['bpn_mean'], c='r')
plt.grid()
plt.show()

fig, ax = plt.subplots(3,1)
ax[0].plot(df['year'], df['d_spice_tete']-365)
ax[1].plot(df['year'], df['d_sofa_bpn']-365)
ax[2].plot(df['year'], df['d_sofa_mean']-365)
plt.show()
