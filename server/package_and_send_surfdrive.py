"""Package a session's results, upload them to SURFdrive and email the user a link.

Original author: Pieter Barkema (2022). Packaging updated for PCNtoolkit 1.x.

What goes in results.zip (from <session>/transfer/):
- results/  all test outputs, plus statistics_adapt.csv (how well the transfer fit)
- model/    the transferred model, loadable with NormativeModel.load
- plots/    test plots, plus the adaptation centile plots (no adaptation Q-Q plots)
- README.txt

Credentials (SURFdrive, Gmail) come from config.py, which only exists on the cluster.
build_results_zip() does not need it, so packaging can be tested locally.
"""

import os
import zipfile
from datetime import date
from importlib.metadata import version

import pandas as pd

README = """PCNportal results
=================

Pretrained model:    {model_name}
Date:                {today}
PCNtoolkit version:  {ptk_version}
Adaptation subjects: {n_adapt}
Test subjects:       {n_subjects}
Regions:             {n_regions}
Main result:         results/Z_test.csv (one Z-score per subject and region)
Plots:               plots/ (centile and Q-Q plots per region)

Load your transferred model and plot it in Python (pip install pcntoolkit=={ptk_version}),
from the folder where you unzipped this file:

    from pcntoolkit import NormativeModel, plot_centiles

    model = NormativeModel.load(".")
    plot_centiles(model, response_vars=["{example_region}"])

Your data is deleted from our servers after 30 days.
"""


def include_in_zip(relpath: str) -> bool:
    """Decide per file (path relative to the transfer folder) whether the user gets it."""
    parts = relpath.replace("\\", "/").split("/")
    folder, name = parts[0], parts[-1]
    if folder == "model":
        return True
    if folder == "results":
        return "_adapt" not in name or name == "statistics_adapt.csv"
    if folder == "plots":
        return "_adapt" not in name or name.startswith("centiles_")
    return False


def build_results_zip(transfer_dir: str, zip_path: str, model_name: str) -> list:
    """Write results.zip from a transfer folder. Returns the files included."""
    z_test = pd.read_csv(os.path.join(transfer_dir, "results", "Z_test.csv"))
    regions = [c for c in z_test.columns if c not in ("observations", "subject_ids")]
    readme = README.format(
        model_name=model_name,
        today=date.today().isoformat(),
        ptk_version=version("pcntoolkit"),
        n_adapt=len(pd.read_csv(os.path.join(transfer_dir, "results", "Z_adapt.csv"), usecols=[0])),
        n_subjects=len(z_test),
        n_regions=len(regions),
        example_region=regions[0],
    )

    included = []
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("README.txt", readme)
        for root, _, files in os.walk(transfer_dir):
            for f in sorted(files):
                relpath = os.path.relpath(os.path.join(root, f), transfer_dir)
                if include_in_zip(relpath):
                    zf.write(os.path.join(root, f), relpath)
                    included.append(relpath)
    return included


def send_results(session_path: str, session_id: str, email_address: str, model_name: str) -> None:
    """Zip the results, upload them to SURFdrive and email the user the link."""
    zip_path = os.path.join(session_path, "results.zip")
    build_results_zip(os.path.join(session_path, "transfer"), zip_path, model_name)
    upload_results(zip_path, session_id)
    email_results(session_id, email_address)


def email_results(session_id: str, email_receiver: str) -> None:
    """Email the user a SURFdrive link to their results (Gmail account from config.py)."""
    import smtplib
    import ssl
    from email.message import EmailMessage

    import config

    em = EmailMessage()
    em["From"] = config.gmail_username
    em["To"] = email_receiver
    em["Subject"] = "Your normative modelling results"
    em.set_content(
        "Here are your normative modelling results:\n"
        f"{config.surf_link}{session_id}\n\n"
        "You'll be taken to your results folder. Click results.zip to download it.\n"
    )

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(config.gmail_username, config.gmail_password)
        smtp.sendmail(config.gmail_username, email_receiver, em.as_string())


def upload_results(from_path: str, session_id: str) -> None:
    """Upload results.zip to SURFdrive under /sessions/<session_id>/ (WebDAV account from config.py)."""
    from webdav3.client import Client

    import config

    client = Client({
        "webdav_login": config.webdav_username,
        "webdav_password": config.webdav_password,
        "webdav_hostname": config.webdav_hostname,
    })
    client.verify = False  # Do not check SSL certificates (as before)
    remote_session = "/sessions/" + session_id
    client.execute_request("mkdir", remote_session)
    client.upload_sync(remote_path=remote_session + "/results.zip", local_path=from_path)
