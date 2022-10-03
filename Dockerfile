# Installs and file size management: the smaller, the less downtime
FROM python:3.8
RUN apt-get update
RUN apt-get install -y nano openssh-client
RUN apt-get clean
COPY requirements.txt .
RUN pip3 install -r requirements.txt
RUN python3.8 -m pip install argparse
RUN pip3 cache purge

# Copy files
RUN mkdir sessions
COPY app.py ./app.py
COPY .ssh /root/.ssh
RUN chmod -R 600 /root/.ssh
# Runs gunicorn and SSH
COPY entrypoint.sh ./entrypoint.sh
RUN chmod +x ./entrypoint.sh
#RUN mkdir -p ~/.ssh
#COPY ssh_rsa ~/.ssh/ssh_rsa.pub
# Safer than CMD, no injection possible
ENTRYPOINT [ "./entrypoint.sh" ]
