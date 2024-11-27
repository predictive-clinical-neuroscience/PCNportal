"""
Created on Wed Jun  1 12:01:11 2022

@author: Pieter Barkema

This script sends normative modelling results to the user.
It connects to the SURFdrive to upload the results.
Then, it retrieves a download link for the results, and
emails the link to the user with the provided email address
and by connecting to the Gmail API.


"""

from webdav3.client import Client

def send_results(session_id, email_address):
    """
    
    Main function to upload and send results.
    It sends a download link to the user containing the 
    model evaluation scores and z-scores of the current session.
    
    Parameters
    ----------
    session_id : string
        Unique session ID corresponding to the client side ID.
    email_address : string
        User email address to send modelling results to.

    Returns
    -------
    No values are returned. Instead, the results are uploaded, and an email is 
    sent to the user, containing a SURFdrive link to download their results.
    

    """
    
    import os
    session_path = "/project_cephfs/3022051.01/sessions/" + session_id
    from_path = os.path.join(session_path, "results.zip")
    zip_name = "results.zip"

    # Zip up the results.
    zipper(session_path, zip_name)
    
    # Upload them to SURFdrive.
    upload_results(from_path, session_id)

    # Email the results to the user.
    email_results(session_id, email_address)

def email_results(session_id, email_receiver):
    """
    
    Emails the user with a SURFdrive link to download their results.

    Parameters
    ----------
    session_id : string
        Unique session ID corresponding to the client side ID.
    email_receiver : User email address to send the email with results to.
        

    Returns
    -------
    None. Sends an email.

    """
    import smtplib
    import ssl
    import config
    from email.message import EmailMessage

    # Define email sender and receiver
    email_sender = config.gmail_username
    email_password = config.gmail_password

    # Set the subject and body of the email
    subject = "Your normative modelling results"
    session_results_URL = config.surf_link + session_id #"https://surfdrive.surf.nl/files/index.php/s/FwXZqWwp2asnj2c?path=%2F"
    body = " Here's your normative results: \n" + session_results_URL + " \n You'll be navigated to your results directory. \n Please click on the results.zip file to download it. "

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    # Add SSL (layer of security)
    context = ssl.create_default_context()

    # Log in and send the email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())

def upload_results(from_path, session_id):
    """
    
    Uploads the zipped up results to SURFdrive, using its API.

    Parameters
    ----------
    from_path : string
        The path to the directory that needs to be uploaded.
    session_id : string
        Unique session ID corresponding to the client side ID.

    Returns
    -------
    None. Creates files on remote SURFdrive server.

    """
    import config
    options = {
    'webdav_hostname': 'https://surfdrive.surf.nl/files/remote.php/nonshib-webdav',
    'webdav_login': config.webdav_username, 
    'webdav_password': config.webdav_password
    }
    remote_session = "/sessions/" + session_id 
    client = Client(options)
    client.verify = False # To not check SSL certificates (Default = True)
    client.execute_request("mkdir", remote_session)
    
    to_path = remote_session + "/results.zip"
    client.upload_sync(remote_path = to_path, local_path = from_path)

def zipper(dirName, zipFileName):
    """
    
    Creates a zipped directory from the results directory.

    Parameters
    ----------
    dirName : STRING
        Path to the directory that needs to be zipped.
    zipFileName : STRING
        Name of the created .zip file.

    Returns
    -------
    None. Creates a zipped up directory.

    """
    
    from zipfile import ZipFile
    import os, pandas, pickle
    os.chdir(dirName)
    with ZipFile(zipFileName, 'w') as zipObj:
        # Iterate over all the files in session directory
        for filename in os.listdir(dirName):
            # Only share and zip up the relevant files.
            if filter_results(filename):
    		# posthoc convert to .csv
                with open(filename, "rb") as f: 
                    myobject = pickle.load(f) 
                    newname = filename.split(".")[0] + ".csv"
                    df = pandas.DataFrame(myobject)
                    df.to_csv(newname)
                    zipObj.write(newname, newname)

def filter_results(filename):
    # Filter what error measures and results should be shared.
    measures = ["Z_", "SMSE_", "RMSE_", "Rho_", "pRho_", "MSLL_", "EXPV_"]
    for measure_type in measures:
        if measure_type in filename:
            return True
