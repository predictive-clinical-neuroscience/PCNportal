import pandas as pd
import pcntoolkit
path=r""
x = pd.read_pickle("/project_cephfs/3022051.01/untested_models/Cerebellum/HBR_10MDTB-CerebellumFunc-linear_7K_2sites/Models/meta_data.md")
y = x.to_numpy(dtype="int")
print(x)
# import matplotlib.pyplot as plt
# for i in range(10):
#     plt.clf()
#     t= x.iloc[:, i]
#     fig, ax = plt.subplots()
#     ax.hist(t)
#     plt.show()