import os
import numpy as np
from pcntoolkit.normative_model.norm_utils import norm_init


model_path = '/project_cephfs/3022051.01/untested_models/Cerebellum_GenR/HBR_10MDTB-CerebellumFunc-linear_7K_2sites/Models'

for m in range(30):
    print(m)
    nm = norm_init(np.zeros((5,5)))
    model_name = os.path.join(model_path, 'NM_0_' + str(m) + '_fit.pkl')
    nm = nm.load(model_name)
    nm.hbr.configs['init'] = 'advi+adapt_diag'
    #nm.hbr.configs['init'] = 'jitter+adapt_diag'
    nm.save(model_name)