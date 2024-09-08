import vernal as ver
import spiceypy as sp

sp.furnsh('k_1600_2600.tm')
df = ver.get_df(100, back=True)
sp.kclear()

