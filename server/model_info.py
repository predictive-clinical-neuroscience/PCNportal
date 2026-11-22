#!/usr/bin/env python3
"""Print what the website needs to know about one PCNtoolkit 1.x model, as JSON.

Called by the website (over SSH, or directly when running locally) with the model folder:
    python model_info.py <projectdir>/<models>/<data_type>/<model_name>

Output: {"covariates": [...], "batch_effects": {name: [values]}, "regions": [...], "readme": "..."}
"readme" is the model folder's README.md if there is one, otherwise "".
"""

import json
import os
import sys


def model_info(model_dir: str) -> dict:
    with open(os.path.join(model_dir, "model", "normative_model.json"), encoding="utf-8") as f:
        meta = json.load(f)
    model_root = os.path.join(model_dir, "model")
    regions = sorted(d for d in os.listdir(model_root) if os.path.isdir(os.path.join(model_root, d)))
    readme_path = os.path.join(model_dir, "README.md")
    readme = ""
    if os.path.isfile(readme_path):
        with open(readme_path, encoding="utf-8") as f:
            readme = f.read()
    return {
        "covariates": meta["covariates"],
        "batch_effects": meta["unique_batch_effects"],
        "regions": regions,
        "readme": readme,
    }


if __name__ == "__main__":
    print(json.dumps(model_info(sys.argv[1])))
