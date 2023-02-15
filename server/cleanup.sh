#! /bin/bash

find /project_cephfs/3022051.01/sessions/ -type d -mtime +30 -exec rm -rf {} \; 
