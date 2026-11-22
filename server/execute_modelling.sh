#! /bin/bash
# Original author: Pieter Barkema
# Started by the website (through sbatch) to run one transfer on the cluster.
#
# Arguments:
# 1 = path to the project dir
# 2 = model name
# 3 = data type dir
# 4 = session id
# 5 = model directory
# 6 = user email address
# 7 = python env, relative to the project dir

set -e

PROJECTDIR=$1
SCRIPTDIR=$(dirname "$0")
PYTHON_ENV=$7
# The Slurm jobs that PCNtoolkit's Runner starts load the same module.
ANACONDA_MODULE="anaconda3/2021.05"

cd "$PROJECTDIR"
module load "$ANACONDA_MODULE"
source activate "${PROJECTDIR}/${PYTHON_ENV}"

echo "Bash script activated..."
python -u "${SCRIPTDIR}/transfer_normative_models_online.py" "$1" "$2" "$3" "$4" "$5" "$6" \
    --preamble "module load $ANACONDA_MODULE"
