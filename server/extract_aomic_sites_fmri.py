import pandas as pd
import numpy as np
x=pd.read_csv("/project_cephfs/3022017.02/projects/hansav/Run4/data/control_metadata.csv")

AOMIC= x.loc[x['dataset']=="AOMIC_PIOP2"]
print(AOMIC.head(n=5))

AOMIC.to_csv("***REMOVED***/docs/fmri_data/AOMIC_covs")