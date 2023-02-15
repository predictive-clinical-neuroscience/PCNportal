import pathlib
import pandas as pd
from webdav3.client import Client

def send_results(session_id, email_address):#results_path #session_id="session_id427076", email_address="pieterwbarkema@gmail.com"
    import os
    session_subdir = "sessions/" + session_id
    session_path = "/project_cephfs/3022051.01/sessions/" + session_id
    # for now we remove idp_results
    #results_dir = "idp_results"
    #get sessions/session_id
    
    #dropbox_dir = os.path.join("/sessions", session_id)
    from_path = os.path.join("/project_cephfs/3022051.01/sessions/", session_id, "results.zip")
    session_path = os.path.join("/project_cephfs/3022051.01", "sessions", session_id)
    #zip_name =  the optional subdir within projects folder that contain a session's results.
    zip_name = "results.zip"

    

    # what results do we want to use?
    #filter = lambda name : 'Z_' in name
    zipper(session_path, zip_name) #filter
    
    upload_results(from_path, session_id)
    email_results(session_id, email_address)
    # and then email and everyone was happy
    #share_download_link
    #send_results(download_link, email_address)

def email_results(session_id, email_receiver):
    import smtplib
    import ssl
    import config
    from email.message import EmailMessage

    # Define email sender and receiver
    email_sender = config.gmail_username
    email_password = config.gmail_password

    # Set the subject and body of the email
    subject = "Your normative modelling results"
    session_results_URL = "https://surfdrive.surf.nl/files/index.php/s/uW3tlx7RGzpK0R5?path=%2F" + session_id
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
    import config
    options = {
    'webdav_hostname': 'https://surfdrive.surf.nl/files/remote.php/nonshib-webdav',
    'webdav_login': config.webdav_username, 
    'webdav_password': config.webdav_password
    }
    remote_session = "/sessions/" + session_id 
    client = Client(options)
    client.verify = False # To not check SSL certificates (Default = True)
    # client.session.proxies(...) # To set proxy directly into the session (Optional)
    # client.session.auth(...) # To set proxy auth directly into the session (Optional)
    #from_path = "/project_cephfs/3022051.01/sessions/session_id924687/Z_transfer.pkl"
    #curl -T filetoput.xml http://www.url.com/filetoput.xml

    # fails if dir already exists, can use 'list' to check first
    client.execute_request("mkdir", remote_session)
    
    to_path = remote_session + "/results.zip"
    client.upload_sync(remote_path = to_path, local_path = from_path)

def zipper(dirName, zipFileName): #filter
    from zipfile import ZipFile
    import os
    from os.path import basename
    # create a ZipFile object
    os.chdir(dirName)
    with ZipFile(zipFileName, 'w') as zipObj:
        # Iterate over all the files in directory
        # for folderName, subfolders, filenames in os.walk(dirName):
            
        #     for filename in filenames:
        for filename in os.listdir(dirName):
            if filter_results(filename):
                # create complete filepath of file in directory
                #filePath = os.path.join(folderName, filename)
                # Add file to zip
                zipObj.write(filename, filename)
def filter_results(filename):
    measures = ["Z_", "SMSE_", "RMSE_", "Rho_", "pRho_", "MSLL_", "EXPV_"]
    for measure_type in measures:
        if measure_type in filename:
            return True
#send_results()