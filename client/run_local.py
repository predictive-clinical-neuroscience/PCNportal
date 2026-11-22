"""Run the website locally, without Docker or the cluster.

It uses a local copy of the cluster project folder (default: local_runs/fake_project):
    models/<data_type>/<model_name>/model/normative_model.json
    sessions/     (created when you submit)
Submitting runs the transfer on this machine in the background, without email.
The results go to sessions/<session_id>/transfer.

From the repo root, in the pcnportal-ptk-1.4.0 env:
    python client/run_local.py
then open http://127.0.0.1:8050
Set PROJECTDIR to use another project folder.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)

os.environ.setdefault("PROJECTDIR", os.path.join(REPO, "local_runs", "fake_project"))
os.environ.update(
    RUN_LOCAL="1",
    MODELS="models",
    SCRIPTDIR=os.path.join(REPO, "server"),  # absolute, so it is not joined to PROJECTDIR
    LISTDIR="list_subdirs.py",
)
sys.path.insert(0, HERE)

from app import app  # noqa: E402 (needs the settings above)

if __name__ == "__main__":
    app.run(debug=True)
