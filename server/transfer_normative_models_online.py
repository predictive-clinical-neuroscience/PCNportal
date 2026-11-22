#!/usr/bin/env python3
"""Transfer a pretrained PCNtoolkit 1.x model to a user's data (PCNportal backend).

The website uploads adapt.pkl and test.pkl to <projectdir>/sessions/<session_id>/
and starts this script through execute_modelling.sh. This script:

1. loads the user's data and the chosen model,
2. checks the data (required columns, batch-effect groups, sex labels),
3. runs Runner.transfer_predict, which splits the regions into Slurm jobs,
   waits for them, retries failures and merges the results,
4. sends the results to the user (package_and_send_surfdrive.py).

Output goes to <session>/transfer/ (model/, results/, plots/).

Cluster (called by execute_modelling.sh):
    python transfer_normative_models_online.py PROJECTDIR MODEL DATA_TYPE SESSION_ID MODEL_DIR EMAIL

Local (no Slurm, no email), with the same session layout:
    python transfer_normative_models_online.py PROJECTDIR MODEL DATA_TYPE SESSION_ID MODEL_DIR EMAIL --local
"""

import argparse
import json
import math
import os
import sys
from functools import partial
from typing import Callable

import pandas as pd
from pcntoolkit import NormativeModel, NormData
from pcntoolkit.util.runner import Runner

from data_checks import check_batch_effect_groups

# The portal's data codes sex as 0/1 (0 = female, 1 = male); v1 models use "F"/"M".
SEX_LABELS = {0: "F", 1: "M", "0": "F", "1": "M"}


class DataError(Exception):
    """User data cannot be used with this model. The message is meant for the user."""


def read_model_metadata(model_dir: str) -> dict:
    with open(os.path.join(model_dir, "model", "normative_model.json"), encoding="utf-8") as f:
        return json.load(f)


def model_response_vars(model_dir: str) -> list:
    """Each region has its own subfolder with regression_model.json."""
    root = os.path.join(model_dir, "model")
    return sorted(d for d in os.listdir(root) if os.path.isdir(os.path.join(root, d)))


def prepare_data(adapt_df: pd.DataFrame, test_df: pd.DataFrame, meta: dict, model_rvs: list,
                 subject_col: str = "sub_id") -> tuple:
    """Validate the user's data and turn it into NormData for the model."""
    covariates = meta["covariates"]
    batch_effects = list(meta["unique_batch_effects"])

    for name, df in (("adaptation", adapt_df), ("test", test_df)):
        missing = [c for c in covariates + batch_effects if c not in df.columns]
        if missing:
            raise DataError(f"Your {name} data is missing the required columns: {', '.join(missing)}.")

    map_sex = "sex" in batch_effects and set(meta["unique_batch_effects"]["sex"]) == {"F", "M"}
    if map_sex:
        for name, df in (("adaptation", adapt_df), ("test", test_df)):
            unknown = sorted(set(df["sex"].astype(str)) - {"0", "1", "F", "M"})
            if unknown:
                raise DataError(f"Your {name} data has unknown sex values {unknown}; use 0 (female) or 1 (male).")

    problems = check_batch_effect_groups(adapt_df, test_df, batch_effects)
    if problems:
        raise DataError("\n".join(problems))

    # Regions must be in the model and in both files, so every job gets the same regions.
    response_vars = [rv for rv in model_rvs if rv in adapt_df.columns and rv in test_df.columns]
    if not response_vars:
        raise DataError("None of the regions in your data match this model.")

    adapt_df, test_df = adapt_df.copy(), test_df.copy()
    if map_sex:
        for df in (adapt_df, test_df):
            df["sex"] = df["sex"].map(lambda v: SEX_LABELS.get(v, v))
    for df in (adapt_df, test_df):
        for be in batch_effects:
            df[be] = df[be].astype(str)

    def to_norm_data(df, name):
        return NormData.from_dataframe(
            name=name,
            dataframe=df,
            covariates=covariates,
            batch_effects=batch_effects,
            response_vars=response_vars,
            subject_ids=subject_col if subject_col in df.columns else None,
        )

    print(f"Data OK: {len(adapt_df)} adaptation and {len(test_df)} test subjects, "
          f"{len(response_vars)}/{len(model_rvs)} model regions")
    return to_norm_data(adapt_df, "adapt"), to_norm_data(test_df, "test")


def run_transfer(model_dir: str, adapt_df: pd.DataFrame, test_df: pd.DataFrame, out_dir: str,
                 runner_for: Callable[[int], Runner]) -> NormativeModel:
    """Load the model, check and prepare the data, transfer and predict. Results go to out_dir.

    runner_for(n_regions) builds the Runner once we know how many regions will be modelled.
    """
    meta = read_model_metadata(model_dir)
    print(f"Model: {os.path.basename(model_dir)} (fit with PCNtoolkit {meta.get('ptk_version')})")
    adapt, test = prepare_data(adapt_df, test_df, meta, model_response_vars(model_dir))
    model = NormativeModel.load(model_dir)
    runner = runner_for(len(adapt.response_vars))
    return runner.transfer_predict(model, adapt, test, save_dir=out_dir)


def make_runner(n_regions: int, local: bool, session_path: str, regions_per_job: int,
                memory: str, time_limit: str, preamble: str) -> Runner:
    if local:
        return Runner(parallelize=False)
    return Runner(
        parallelize=True,
        job_type="slurm",
        n_batches=max(1, math.ceil(n_regions / regions_per_job)),
        memory=memory,
        time_limit=time_limit,
        environment=sys.prefix,  # the conda env this script runs in
        preamble=preamble,
        log_dir=os.path.join(session_path, "logs"),
        temp_dir=os.path.join(session_path, "tmp"),
    )


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    # Positional arguments, in the order execute_modelling.sh passes them.
    p.add_argument("projectdir")
    p.add_argument("model_name")
    p.add_argument("data_type")
    p.add_argument("session_id")
    p.add_argument("model_dir", help="Models folder, relative to projectdir")
    p.add_argument("email_address")
    p.add_argument("--local", action="store_true", help="Run in this process, without Slurm or email")
    p.add_argument("--regions-per-job", type=int, default=10)
    p.add_argument("--memory", default="4GB")
    p.add_argument("--time", default="02:00:00", help="Slurm time limit per job")
    p.add_argument("--preamble", default="module load anaconda3", help="Shell lines run before each job")
    args = p.parse_args()

    model_path = os.path.join(args.projectdir, args.model_dir, args.data_type, args.model_name)
    session_path = os.path.join(args.projectdir, "sessions", args.session_id)
    out_dir = os.path.join(session_path, "transfer")

    adapt_df = pd.read_pickle(os.path.join(session_path, "adapt.pkl"))
    test_df = pd.read_pickle(os.path.join(session_path, "test.pkl"))
    runner_for = partial(make_runner, local=args.local, session_path=session_path,
                         regions_per_job=args.regions_per_job, memory=args.memory,
                         time_limit=args.time, preamble=args.preamble)

    try:
        run_transfer(model_path, adapt_df, test_df, out_dir, runner_for)
    except DataError as e:
        # Kept for the user; emailing it is part of the error-handling work (#4).
        with open(os.path.join(session_path, "data_error.txt"), "w", encoding="utf-8") as f:
            f.write(str(e))
        sys.exit(f"Data check failed:\n{e}")
    print(f"Results written to {out_dir}")

    if not args.local:
        from package_and_send_surfdrive import send_results
        send_results(args.session_id, args.email_address)


if __name__ == "__main__":
    main()
