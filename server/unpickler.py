import pandas as pd
path=r"/project_cephfs/3022051.01/sessions/test_session_99ec5c53c62f48f7894b9b585cbaad2b/Z_transfer.pkl"
x = pd.read_pickle(path)
#print(x.0)
import matplotlib.pyplot as plt
for i in range(10):
    plt.clf()
    t= x.iloc[:, i]
    fig, ax = plt.subplots()
    ax.hist(t)
    plt.show()