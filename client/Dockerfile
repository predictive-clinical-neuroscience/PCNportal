# Installs software and cleans up unnecessary memory: the smaller, the less downtime
FROM python:3.8
RUN apt-get update
RUN apt-get install -y nano openssh-client
RUN apt-get clean
COPY requirements.txt .
RUN pip3 install -r requirements.txt
RUN python3.8 -m pip install argparse
RUN pip3 cache purge

# Copy files and create file structure
RUN mkdir sessions
COPY app.py ./app.py
COPY assets ./assets

# Runs gunicorn and SSH
COPY entrypoint.sh ./entrypoint.sh
RUN chmod +x ./entrypoint.sh
# Safer than CMD, no injection possible
ENTRYPOINT ["./entrypoint.sh"]
