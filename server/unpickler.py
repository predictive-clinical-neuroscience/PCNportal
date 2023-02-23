import pandas as pd
path=r""
x = pd.read_pickle("/project_cephfs/3022051.01/sessions/3839801196b2401f83576cce02fa2414/sitenum_ad.pkl")
y = x.to_numpy(dtype="int")
print(x)
# import matplotlib.pyplot as plt
# for i in range(10):
#     plt.clf()
#     t= x.iloc[:, i]
#     fig, ax = plt.subplots()
#     ax.hist(t)
#     plt.show()