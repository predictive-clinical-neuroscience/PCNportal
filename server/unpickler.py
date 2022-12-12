import pandas as pd
path="***REMOVED***/sessions/67700178ffb844f891891c63e10924e9/Z_transfer.pkl"
x = pd.read_pickle(path)
#print(x.0)
import matplotlib.pyplot as plt
for i in range(10):
    plt.clf()
    t= x.iloc[:, i]
    fig, ax = plt.subplots()
    ax.hist(t)
    plt.show()