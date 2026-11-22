"""Checks on user data before a model transfer.

PCNtoolkit's BLR transfer estimates a mean shift and a scale for every
combination of batch effects (e.g. site x sex) in the adaptation data, and
predicts the test data with those estimates. That means:

1. every combination in the adaptation data needs at least 2 subjects, and
2. every combination in the test data must also be in the adaptation data.

PCNtoolkit raises an error otherwise (after PCNtoolkit PR #645; 1.4.0 gives
infinite Z-scores instead). These checks catch it before any modelling starts,
with a message the user can act on.
"""

from typing import List

import pandas as pd

MIN_ADAPT_SUBJECTS = 2


def _label(batch_effects: List[str], key) -> str:
    values = key if isinstance(key, tuple) else (key,)
    return ", ".join(f"{be}={v}" for be, v in zip(batch_effects, values))


def check_batch_effect_groups(
    adapt_df: pd.DataFrame,
    test_df: pd.DataFrame,
    batch_effects: List[str],
    min_adapt_subjects: int = MIN_ADAPT_SUBJECTS,
) -> List[str]:
    """Return a list of problems; an empty list means the data is OK.

    Values are compared as text, so 1 and "1" count as the same group.
    """
    adapt_counts = adapt_df[batch_effects].astype(str).groupby(batch_effects).size()
    test_counts = test_df[batch_effects].astype(str).groupby(batch_effects).size()

    problems = []
    for key, n in adapt_counts[adapt_counts < min_adapt_subjects].items():
        problems.append(
            f"Adaptation data: {_label(batch_effects, key)} has {n} subject(s); "
            f"at least {min_adapt_subjects} are needed."
        )
    for key in test_counts.index.difference(adapt_counts.index):
        problems.append(
            f"Test data: {_label(batch_effects, key)} ({test_counts[key]} subject(s)) "
            f"does not appear in the adaptation data."
        )
    return problems
