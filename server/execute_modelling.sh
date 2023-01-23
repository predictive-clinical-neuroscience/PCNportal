#! /bin/bash
# 1 = path to the project dir
# 2 = model name
# 3 = data type dir
# 4 = session id
# 5 = algorithm
# 6 = user email address

# Activate our virtual environment.
# Activate pcntoolkit devel environment, preferred syntax above conda activate
cd ***REMOVED***
module load "anaconda3/2021.05"
source activate remotepcn
# Ensure working directory is our project.
#cd ***REMOVED*** 
echo "Bash script activated..."
python ***REMOVED***/***REMOVED***/transfer_normative_models_online.py $1 $2 $3 $4 $5 $6