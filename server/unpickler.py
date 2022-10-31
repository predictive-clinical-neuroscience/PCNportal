import pandas as pd
path="/project_cephfs/3022051.01/sessions/7f56f51ac9c0475cbe0b15fb1721c7c9/sitenum_te.pkl"
x = pd.read_pickle(path)
print(x.head(n=100))