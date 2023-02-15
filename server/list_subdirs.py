#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  1 12:01:11 2022

@author: piebar
"""


def main():
    import os, sys
    chosen_dir = sys.argv[1]
    full_path = os.path.join("/project_cephfs/3022051.01", chosen_dir)
    subdirs = os.listdir(full_path)
    print(subdirs)
    return subdirs

if __name__ == "__main__":
    main()