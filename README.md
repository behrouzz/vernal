**Author:** [Behrouz Safari](https://behrouzz.github.io/)<br/>


# vernal
*Calculating vernal equinox*




## Example

```python
import vernal as ver
import spiceypy as sp

sp.furnsh('k_1600_2600.tm')
df = ver.get_df(100, back=True)
sp.kclear()

print(df)
```

Output:

```
              et         TDBjd  persian  gregorian          diff
0  -2.474715e+07  2.451259e+06     1380       2001           NaN
1  -5.630429e+07  2.450893e+06     1379       2000 -6.309314e+07
2  -8.786185e+07  2.450528e+06     1378       1999 -6.309357e+07
3  -1.194190e+08  2.450163e+06     1377       1998 -6.309312e+07
4  -1.509759e+08  2.449798e+06     1376       1997 -6.309292e+07
..           ...           ...      ...        ...           ...
95 -3.022657e+09  2.416561e+06     1285       1906 -6.309350e+07
96 -3.054214e+09  2.416195e+06     1284       1905 -6.309269e+07
97 -3.085771e+09  2.415830e+06     1283       1904 -6.309343e+07
98 -3.117329e+09  2.415465e+06     1282       1903 -6.309325e+07
99 -3.148885e+09  2.415100e+06     1281       1902 -6.309264e+07

[100 rows x 5 columns]
```