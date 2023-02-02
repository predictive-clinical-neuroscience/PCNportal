#! /bin/bash

find ***REMOVED***/sessions/ -type d -mtime +30 -exec rm -rf {} \; 
