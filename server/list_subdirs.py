#!/usr/bin/env python3
"""List the subfolders of a folder in the project dir, for the website's dropdowns.

Original author: Pieter Barkema (2022).

Called over SSH by the website with a path relative to the project dir:
    <models>                -> data types
    <models>/<data_type>    -> models of that data type
Prints a Python list, which the website reads with ast.literal_eval.
"""

import os
import sys

import config


def main():
    full_path = os.path.join(config.project_dir, sys.argv[1])
    subdirs = sorted(
        d for d in os.listdir(full_path)
        if not d.startswith(".") and os.path.isdir(os.path.join(full_path, d))
    )
    print(subdirs)
    return subdirs


if __name__ == "__main__":
    main()
