**Author:** [Behrouz Safari](https://behrouzz.github.io/)<br/>


# vernal
*Calculating vernal equinox*




## Example

```python
import vernal as ver
from vernal.time import tt2ut1
import spiceypy as sp

sp.furnsh('k_1600_2600.tm')
df = ver.get_df(200, back=True)
sp.kclear()

df['ut1'] = tt2ut1(df['tt'])
print(df)
```

Output:

```
               et            tt  persian  gregorian           ut1
0   -2.474714e+07  2.451259e+06     1380       2001  2.451259e+06
1   -5.630429e+07  2.450893e+06     1379       2000  2.450893e+06
2   -8.786186e+07  2.450528e+06     1378       1999  2.450528e+06
3   -1.194234e+08  2.450163e+06     1377       1998  2.450163e+06
4   -1.509815e+08  2.449798e+06     1376       1997  2.449798e+06
..            ...           ...      ...        ...           ...
195 -6.178589e+09  2.380034e+06     1185       1806  2.380034e+06
196 -6.210147e+09  2.379668e+06     1184       1805  2.379668e+06
197 -6.241706e+09  2.379303e+06     1183       1804  2.379303e+06
198 -6.273264e+09  2.378938e+06     1182       1803  2.378938e+06
199 -6.304822e+09  2.378573e+06     1181       1802  2.378573e+06

[200 rows x 5 columns]
```