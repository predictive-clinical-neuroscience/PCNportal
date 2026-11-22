"""Run one PCNtoolkit 1.x transfer locally from CSV files, without the website or the cluster.

Uses the same code as the portal backend (transfer_normative_models_online.py),
but runs in this process and writes to a folder of your choice.

Example (from the repo root, in the pcnportal-ptk-1.4.0 env):
    python server/transfer_local.py ^
        --model  C:/Users/<you>/Downloads/meas-thickness_atlas-DES_alg-BLRw_model ^
        --adapt  client/docs/OpenNeuroTransfer_ct_ad.csv ^
        --test   client/docs/OpenNeuroTransfer_ct_te.csv ^
        --out    local_runs/openneuro_DES_BLR
"""

import argparse
import os
import sys
import time

import pandas as pd
from pcntoolkit.util.runner import Runner

from transfer_normative_models_online import DataError, run_transfer

if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--model", required=True, help="Folder that contains model/normative_model.json")
    p.add_argument("--adapt", required=True, help="Adaptation (transfer) CSV")
    p.add_argument("--test", required=True, help="Test CSV")
    p.add_argument("--out", required=True, help="Output folder for the transferred model and results")
    args = p.parse_args()

    t0 = time.time()
    try:
        run_transfer(
            os.path.abspath(args.model),
            pd.read_csv(args.adapt),
            pd.read_csv(args.test),
            os.path.abspath(args.out),
            runner_for=lambda n_regions: Runner(parallelize=False),
        )
    except DataError as e:
        sys.exit(f"Data check failed:\n{e}")
    print(f"Done in {time.time() - t0:.0f}s. Output written to: {os.path.abspath(args.out)}")
