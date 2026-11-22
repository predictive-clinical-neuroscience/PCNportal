#!/usr/bin/env python3
"""List the subfolders of a folder, for the website's dropdowns.

Original author: Pieter Barkema (2022).

Called by the website (over SSH, or directly when running locally) with a full path:
    <projectdir>/<models>                -> data types
    <projectdir>/<models>/<data_type>    -> models of that data type
Prints a Python list, which the website reads with ast.literal_eval.
"""

import os
import sys


def main():
    full_path = sys.argv[1]
    subdirs = sorted(
        d for d in os.listdir(full_path)
        if not d.startswith(".") and os.path.isdir(os.path.join(full_path, d))
    )
    print(subdirs)
    return subdirs


if __name__ == "__main__":
    main()
