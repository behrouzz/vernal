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

##fig, ax = plt.subplots()
##ax.plot(df['year'].values, df['spice_sofa'].values, c='b')
##ax.plot(df['year'].values, df['bpn_mean'].values, c='r')
##plt.grid()
##plt.show()
##
##fig, ax = plt.subplots(3,1)
##ax[0].plot(df['year'].values, df['d_spice_tete'].values-365)
##ax[1].plot(df['year'].values, df['d_sofa_bpn'].values-365)
##ax[2].plot(df['year'].values, df['d_sofa_mean'].values-365)
##plt.show()


# 1500-2500
df = df[(df['year']>=1500) & (df['year']<=2500)]

kinds = ['sofa_bpn', 'spice_tete', 'sofa_mean']
rot_kind = kinds[2]

col = 'd_' + rot_kind

var_min = (df[col].max() - df[col].min()) * (24*60)
print(f'variation in minutes ({rot_kind}):', var_min)

length = (df[col].values-365) * 24
plt.plot(df['year'].values, length)
plt.grid()
plt.show()
