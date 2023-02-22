#!/bin/bash

mkdir -p ~/.ssh

if [ ! -f ~/.ssh/id_rsa ]; then
  # Generate a new SSH key, that the user should copy to the submission host of qsub.
  ssh-keygen -t rsa -N "" -C "PCNportal" -f ~/.ssh/id_rsa
  echo "copy the following content to ~/.ssh/authorized_keys"
  cat ~/.ssh/id_rsa.pub
fi
env > /tmp/env.txt
# This chmod has to be here and not in Dockerfile, because it will strangely not have an effect.
# May be related to Windows + Docker Desktop flaws
chmod -R 600 /root/
gunicorn --timeout=1000 --workers=5 --threads=1 -b 0.0.0.0:80 app:server
# ssh piebar@mentat004.dccn.nl