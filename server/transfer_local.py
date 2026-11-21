"""Run one PCNtoolkit 1.x transfer locally, without the website or the cluster.

This is the core of what the new transfer orchestrator will do:
load a pretrained model -> transfer it to the user's adaptation data ->
predict on the user's test data -> write Z-scores, centiles, metrics and the
transferred model to disk.

Example (from the repo root, in the pcnportal-ptk-1.4.0 env):
    python server/transfer_local.py ^
        --model  C:/Users/<you>/Downloads/meas-thickness_atlas-DES_alg-BLRw_model ^
        --adapt  client/docs/fcon1000_tr.csv ^
        --test   client/docs/fcon1000_te.csv ^
        --out    local_runs/fcon1000_DES_BLR
"""

import argparse
import json
import os
import sys
import time

import pandas as pd
from pcntoolkit import NormativeModel, NormData

from data_checks import check_batch_effect_groups

# The portal's demo data codes sex as 0/1; the v1 models use "F"/"M".
# PCN convention: 0 = female, 1 = male.
SEX_MAP = {0: "F", 1: "M", "0": "F", "1": "M"}


def read_model_metadata(model_dir: str) -> dict:
    with open(os.path.join(model_dir, "model", "normative_model.json"), encoding="utf-8") as f:
        return json.load(f)


def model_response_vars(model_dir: str) -> list:
    """Each region has its own subfolder with regression_model.json."""
    root = os.path.join(model_dir, "model")
    return sorted(d for d in os.listdir(root) if os.path.isdir(os.path.join(root, d)))


def read_user_csv(path: str, meta: dict) -> pd.DataFrame:
    df = pd.read_csv(path)
    required = meta["covariates"] + list(meta["unique_batch_effects"].keys())
    missing_cols = [c for c in required if c not in df.columns]
    if missing_cols:
        sys.exit(f"{path}: missing required columns {missing_cols}")
    return df


def to_norm_data(df: pd.DataFrame, name: str, meta: dict, model_rvs: list, subject_col: str) -> NormData:
    df = df.copy()
    covariates = meta["covariates"]
    batch_effects = list(meta["unique_batch_effects"].keys())

    # Response variables = model regions that are present in the user's file.
    response_vars = [rv for rv in model_rvs if rv in df.columns]
    print(f"[{name}] {len(df)} subjects, {len(response_vars)}/{len(model_rvs)} model regions found")

    if "sex" in batch_effects:
        df["sex"] = df["sex"].map(lambda v: SEX_MAP.get(v, v))
    if "site" in batch_effects:
        df["site"] = df["site"].astype(str)

    return NormData.from_dataframe(
        name=name,
        dataframe=df,
        covariates=covariates,
        batch_effects=batch_effects,
        response_vars=response_vars,
        subject_ids=subject_col if subject_col in df.columns else None,
    )


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--model", required=True, help="Folder that contains model/normative_model.json")
    p.add_argument("--adapt", required=True, help="Adaptation (transfer) CSV")
    p.add_argument("--test", required=True, help="Test CSV")
    p.add_argument("--out", required=True, help="Output folder for the transferred model and results")
    p.add_argument("--subject-col", default="sub_id", help="Column with subject IDs (default: sub_id)")
    args = p.parse_args()

    model_dir = os.path.abspath(args.model)
    out_dir = os.path.abspath(args.out)
    meta = read_model_metadata(model_dir)
    model_rvs = model_response_vars(model_dir)
    print(f"Model: {os.path.basename(model_dir)} (fit with PCNtoolkit {meta.get('ptk_version')})")
    print(f"Covariates: {meta['covariates']} | batch effects: {list(meta['unique_batch_effects'])}")

    adapt_df = read_user_csv(args.adapt, meta)
    test_df = read_user_csv(args.test, meta)

    problems = check_batch_effect_groups(adapt_df, test_df, list(meta["unique_batch_effects"]))
    if problems:
        sys.exit("Data check failed:\n  " + "\n  ".join(problems))

    adapt = to_norm_data(adapt_df, "adapt", meta, model_rvs, args.subject_col)
    test = to_norm_data(test_df, "test", meta, model_rvs, args.subject_col)

    t0 = time.time()
    model = NormativeModel.load(model_dir)
    transferred = model.transfer(adapt, save_dir=out_dir)
    print(f"Transfer done in {time.time() - t0:.0f}s")

    t0 = time.time()
    transferred.predict(test)
    print(f"Predict done in {time.time() - t0:.0f}s")
    print(f"Output written to: {out_dir}")
