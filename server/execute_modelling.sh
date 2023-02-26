#! /bin/bash
# @author: Pieter Barkema
# A bash script executed on the server side to start modelling.
#
# Variables:
# 1 = path to the project dir
# 2 = model name
# 3 = data type dir
# 4 = session id
# 5 = algorithm
# 6 = user email address

# Activate our virtual environment
cd /project_cephfs/3022051.01
module load "anaconda3/2021.05"
source activate remotepcn

# Start modelling
echo "Bash script activated..."
python /project_cephfs/3022051.01/test_scripts/server/transfer_normative_models_online.py $1 $2 $3 $4 $5 $6
