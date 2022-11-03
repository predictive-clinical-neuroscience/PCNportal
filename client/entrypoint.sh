#!/bin/bash

mkdir -p ~/.ssh

if [ ! -f ~/.ssh/id_rsa ]; then
  ## generate a new SSH key, the public key should be copied to the submission host of qsub
  ssh-keygen -t rsa -N "" -C "PCNonline" -f ~/.ssh/id_rsa
  echo "copy the following content to ~/.ssh/authorized_keys"
  cat ~/.ssh/id_rsa.pub
fi
env > /tmp/env.txt
gunicorn --timeout=1000 --workers=5 --threads=1 -b 0.0.0.0:80 app:server
