#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 14 16:29:33 2022

@author: piebar

Adapted from apply_normative_models.py and transfer_hbr_models.py.

The purpose of this script is to act as frontend for normative.transfer for all algorithms.
"""


def transfer_normative_models():
    import os, sys
    import numpy as np
    import pandas as pd
    import pickle
    import pcntoolkit as ptk
    sys.path.append("***REMOVED***/training_hbr_models/")
    from utilities import prepare_model_inputs, remove_bad_subjects, create_dummy_inputs
    import os, sys
    import pandas as pd
    import pickle
    import random
    # where the project dir lives
    root_dir = "***REMOVED***/"#sys.argv[1]
    # the name of the chosen model
    model_name= sys.argv[2]#"HBR_models_self_trained"#"HBR_HOM_linear_0.20"##
    data_type = sys.argv[3]#"ThickAvg"##
    session_id = sys.argv[4]#"session_id" + str(random.randint(100000,999999))##
    print(f'{session_id=}')
    alg = model_name.split("_")[0]
    print(f'{alg=}')
    email_address = sys.argv[6]#"pieterwbarkema@gmail.com" # #
    
    model_path = os.path.join(root_dir, "models", data_type, model_name, "Models")

    session_path = os.path.join(root_dir, "sessions", session_id) +"/"
    print(f'{session_path}')
    if not os.path.isdir(session_path):
                os.mkdir(session_path) 
    os.chdir(session_path)
    df_te = pd.read_pickle(os.path.join(session_path, "test.pkl"))#pd.read_csv("***REMOVED***/docs/OpenNeuroTransfer_te.csv") #
    df_ad= pd.read_pickle(os.path.join(session_path, "adapt.pkl"))#pd.read_csv("***REMOVED***/docs/OpenNeuroTransfer_tr.csv")#

    # site enumeration here:
    sites = np.unique(df_te['site'])
    df_te['sitenum'] = np.nan # create empty column first
    for i, s in enumerate(sites):
        df_te['sitenum'].loc[df_te['site'] == s] = int(i)
        #test_data['sitenum'] = test_data['sitenum'].astype(int)
    df_ad['sitenum'] = np.nan # create empty column first
    for i, s in enumerate(sites):
        df_ad['sitenum'].loc[df_ad['site'] == s] = int(i)
    #adaptation_data['sitenum'] = adaptation_data['sitenum'].astype(int)

    site_names = 'site_ids_82sites.txt'

    # could this be fed in by Dash?
    cols_cov = ['age', 'sex']
    # could this be fed in by Dash, dependent on input data?
    #idps = ['rh_MeanThickness_thickness']

    # load a set of site ids from this model. This must match the training data
    # get this for the new models?
    with open(os.path.join(root_dir,'docs', site_names)) as f:
        site_ids_tr = f.read().splitlines()

    # extract a list of unique site ids from the test set
    site_ids_te =  sorted(set(df_te['site'].to_list()))

    # Select idps here
    # load the list of idps for left and right hemispheres, plus subcortical regions
    with open(os.path.join(root_dir,'docs','phenotypes_lh.txt')) as f:
        idp_ids_lh = f.read().splitlines()
    with open(os.path.join(root_dir,'docs','phenotypes_rh.txt')) as f:
        idp_ids_rh = f.read().splitlines()
    with open(os.path.join(root_dir,'docs','phenotypes_lh.txt')) as f:
         idp_ids_sc = f.read().splitlines()
    # we choose here to process all idps
    idps = idp_ids_lh + idp_ids_rh + idp_ids_sc
    testing_sample = 10
    idps = idps[:testing_sample]
    print(f'{idps=}')
    # extract and save the response variables for the test set
    y_te = df_te[idps].to_numpy(dtype=float)
    resp_file_te = os.path.join(session_path, 'resp_te.pkl')
    with open(resp_file_te, 'wb') as file:
        pickle.dump(pd.DataFrame(y_te), file)

    # ok to use pandas instead of fileio?
    import pandas as pd 
    # blr specific arguments

    if alg == "BLR":
        from pcntoolkit.util.utils import create_design_matrix
            # create design matrix arguments; should these be mutable?
        # limits for cubic B-spline basis 
        xmin = -5 
        xmax = 110

        # NOTE: hardcoded way to get all site ids from training data, same as done in apply_norm
        # better way to do this?
        site_names = 'site_ids_82sites.txt'
        with open(os.path.join(root_dir,'docs', site_names)) as f:
            site_ids_tr = f.read().splitlines()
        x_te = create_design_matrix(df_te[cols_cov], 
                                        site_ids = df_te['site'],
                                        all_sites = site_ids_tr,
                                        basis = 'bspline', 
                                        xmin = xmin, 
                                        xmax = xmax)
    elif alg == "HBR":
        x_te = df_te[cols_cov].to_numpy(dtype=float)
    cov_file_te = os.path.join(session_path, 'cov_bspline_te.pkl')
    with open(cov_file_te, 'wb') as file:
        pickle.dump(pd.DataFrame(x_te), file)

    # Save the adaptation data, provide the test data directly.
    if all(elem in site_ids_tr for elem in site_ids_te):        
    # just make predictions
        yhat_te, s2_te, Z = ptk.normative.predict(cov_file_te, 
                                    alg=alg, 
                                    respfile=resp_file_te, 
                                    model_path=os.path.join(root_dir,'Models'))
    else:        
        cov_file_ad = os.path.join(session_path, 'cov_bspline_ad.pkl')
        resp_file_ad = os.path.join(session_path, 'resp_ad.pkl') 
        sitenum_file_te = os.path.join(session_path, 'sitenum_te.pkl')  
        sitenum_file_ad = os.path.join(session_path, 'sitenum_ad.pkl')
        output_path = os.path.join(session_path, 'Transfer/') 
        if alg == "BLR":
            x_ad = create_design_matrix(df_ad[cols_cov], 
                                            site_ids = df_ad['site'],
                                            all_sites = site_ids_tr,
                                            basis = 'bspline', 
                                            xmin = xmin, 
                                            xmax = xmax)
        elif alg == "HBR":
            x_ad = df_ad[cols_cov].to_numpy(dtype=float)
        # save the responses and cov for the adaptation data
        with open(cov_file_ad, 'wb') as file:
            pickle.dump(pd.DataFrame(x_ad), file)
        y_ad = df_ad[idps].to_numpy(dtype=float)
        print(f'{y_ad.shape=},{len(idps)=}')
        with open(resp_file_ad, 'wb') as file:
            pickle.dump(pd.DataFrame(y_ad), file)
        # save the site ids for the adaptation and test data
        # this has to be right format for both hbr and blr's design matrix
        # create design matrix requested site... hbr requests sitenum?
        site_num_ad = df_ad['sitenum']
        site_num_te = df_te['sitenum']
        #print(f'{site_num_ad=},{site_num_te=}')
        with open(sitenum_file_ad, 'wb') as file:
            pickle.dump(site_num_ad, file)
        with open(sitenum_file_te, 'wb') as file:
            pickle.dump(site_num_te, file)
        log_dir = os.path.join(session_path, 'logs/')
        outputsuffix = '_transfer'
        inputsuffix = 'fit'

        # parallelization
        batch_size = int(np.sqrt(testing_sample))
        print(f'{batch_size=}')
        memory = '4gb'
        duration = '2:00:00'
        outputsuffix = '_transfer'
        python_path = '/home/preclineu/piebar/.conda/envs/remotepcn/bin/python'
        ############################# Model & Data configs ############################

        model = model_name#'HBR_HOM' # 'HBR_HET' 'HBR_HOM'
        method = 'linear' # 'linear' 'polynomial' 'bspline'
        random_intercept = 'True'
        random_slope = 'True'
        random_noise = 'True'
        inscaler = 'None' 
        outscaler = 'None'

        ########################## Setting up the Paths and Model #####################

        job_name = model + '_'  + method 
        #processing_dir = path + job_name + '/'
        log_dir = session_path + '/log/'
        print(f'{log_dir}')
        
        if not os.path.isdir(log_dir):
            os.mkdir(log_dir) 
        if not os.path.isdir(output_path):
            os.mkdir(output_path) 
        if model in ['HBR_HOM']:    
            hetero_noise = 'False'
        else:
            hetero_noise = 'True'
        #normative_path = "/home/preclineu/piebar/transform_nm_tests/PCNtoolkit/pcntoolkit/normative.py"
        # how to deal with input data
        # howt o deal with model path
        measure = 'ThickAvg'
        # probably for estimation only, can be deleted?
        # data_path = '/project_cephfs/3022017.02/projects/lifespan_hbr/Data/'
        # with open(data_path + measure + '.pkl', 'rb') as file:
        #     df = pickle.load(file)
        
        count_jobsdone = "True" # create a file for each job completed, to count in await_jobs below
       # prepare_model_inputs(session_path, df)
        ptk.normative_parallel.execute_nm(session_path, python_path, 
                'Transfer_' + job_name, cov_file_ad, resp_file_ad, batch_size, memory, duration, func='transfer', 
                alg=alg, binary=True, trbefile=sitenum_file_ad, 
                model_type=method, random_intercept=random_intercept, 
                random_slope=random_slope, random_noise=random_noise, 
                hetero_noise=hetero_noise, savemodel='True', outputsuffix=outputsuffix,
                inputsuffix=inputsuffix, 
                n_samples='1000', inscaler=inscaler, outscaler=outscaler, 
                testcovfile_path=cov_file_te, testrespfile_path=resp_file_te,
                tsbefile = sitenum_file_te, output_path=output_path,
                model_path=model_path, log_path=log_dir,count_jobsdone=count_jobsdone)
#

        complete = False
        while complete == False:
            # dependjob goes here
            await_jobs(session_path, log_dir)
            print("Start collecting...")
            complete = ptk.normative_parallel.collect_nm(session_path, 'Transfer_' + job_name,
                                   func='transfer', collect=True, binary=True, 
                                   batch_size=batch_size, outputsuffix=outputsuffix)
            if complete == True:
                break
            print("Start rerunning...")
            ptk.normative_parallel.rerun_nm(session_path, log_dir, memory, duration, binary=True)
        # from package_and_send_dropbox import create_link
        

        # Sequential computing
        #print(f'{df_te.shape=}, {y_te.shape=}, {site_num_te.shape=}, {df_ad.shape=}, {y_ad.shape=}, {site_num_ad.shape=}')
        # yhat_te_transfer, s2_te_transfer, Z_transfer = ptk.normative.transfer(
        #                             covfile = cov_file_ad,
        #                             respfile= resp_file_ad,  # do we want to make test set/prediction mandatory?
        #                             tsbefile = sitenum_file_te,
        #                             trbefile = sitenum_file_ad,
        #                             model_path = model_path,
        #                             alg = alg,
        #                             log_path=log_dir,
        #                             binary=True,
        #                             #can retrieve this from the model dir probably
        #                             inputsuffix = inputsuffix, 
        #                             output_path=output_path,
        #                             testcov= cov_file_te,
        #                             testresp = resp_file_te,
        #                             outputsuffix=outputsuffix,
        #                             savemodel=True)
        from package_and_send_surfdrive import send_results
        send_results(session_id, email_address)
def await_jobs(session_path, log_dir):
    import os, time, glob
    jobs_done = False
    max_time = 1200
    sleep_time = 20
    elapsed_time = 0

    batch_dir = glob.glob(session_path + 'batch_*')
    # print(batch_dir)
    number_of_batches = len(batch_dir)
    while jobs_done == False:
        print(f'{number_of_batches=}, {jobs_done=}')
        # check if all jobs are completed
        done_count = len(glob.glob(log_dir + '*.jobsdone'))
        if done_count >= number_of_batches:
            break
        time.sleep(sleep_time)
        elapsed_time+=sleep_time
        # to stop infinite loops, i.e. erroneous computations
        if elapsed_time > max_time:
            break
    print("All", done_count, " out of ", number_of_batches, " jobs done!")
        #make sure to remove them in the loop

transfer_normative_models()
