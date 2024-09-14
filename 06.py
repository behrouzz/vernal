import pandas as pd
from vernal import get_table

df = get_table(y1=-5000, y2=3000, rot_kind='sofa_mean')
print(df)
