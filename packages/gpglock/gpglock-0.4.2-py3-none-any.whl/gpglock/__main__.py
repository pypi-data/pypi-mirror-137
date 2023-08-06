#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import argparse
import os
from gpglock.core import init_dir, lock_dir, unlock_dir
from gpglock.utils.console_logging_formatter import get_formatted_console_logger


logger = get_formatted_console_logger("main")


def __parse_args():
    parser = argparse.ArgumentParser(
        description="Lock secrets in your directory.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("command", choices=["lock", "unlock", "init"])
    parser.add_argument("dir", nargs="?", default=os.getcwd())
    return parser.parse_args()


def main():
    args = __parse_args()
    if args.command == "lock":
        lock_dir(args.dir)
    elif args.command == "unlock":
        unlock_dir(args.dir)
    else:
        init_dir(args.dir)


# __main__.py: Enterpoint of debugging mode
# cli.py:      Enterpoint of cli mode installed by Setuptools
try:
    main()
except Exception as e:
    logger.error(e)
    exit(1)
