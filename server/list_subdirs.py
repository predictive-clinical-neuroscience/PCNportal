#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  1 12:01:11 2022

@author: Pieter Barkema

This script lists the available data types and corresponding models.
It is executed on the server side and the output is provided to the client side.
The website displays this information in dropdown selection menus.

"""


def main():
    import os, sys, config
    chosen_dir = sys.argv[1]
    full_path = os.path.join(config.project_dir, chosen_dir)
    subdirs = os.listdir(full_path)
    print(subdirs)
    return subdirs

if __name__ == "__main__":
    main()
