#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import logging
import os
import pathlib
import shlex
import shutil
import subprocess
import sys

__author__ = "Benjamin Kane"
__version__ = "0.1.0"
__doc__ = f"""
Rename example-go-cli to a new name
Examples:
    {sys.argv[0]}
Help:
Please see Benjamin Kane for help.
Code at <repo>
"""

logger = logging.getLogger(__name__)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--log-level",
        choices=["NOTSET", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
        help="log level",
    )

    parser.add_argument(
        "name",
        help="The name to copy example-go-cli to",
    )

    return parser


def run(*args: str):
    logger.info(f"Running command: {shlex.join(args)}")
    subprocess.run(args, check=True)


def main():
    parser = build_parser()
    args = parser.parse_args()

    logging.basicConfig(
        format="# %(levelname)s %(filename)s:%(lineno)s : %(message)s",  # noqa: E501
        level=logging.getLevelNamesMapping()[args.log_level],
    )

    # copy the example-go-cli directory to the new name
    projects_dir = pathlib.Path(__file__).parent.parent.resolve()
    src_dir = projects_dir / "example-go-cli"
    dest_dir = projects_dir / args.name
    shutil.copytree(src_dir, dest_dir)
    logger.info("Copied %s to %s", src_dir, dest_dir)

    os.chdir(dest_dir)
    logger.info("Changed working directory to: %s", os.getcwd())

    # git clean
    logger.info("Cleaning git repository in: %s", dest_dir)
    run("git", "clean", "-fdx")
    logger.info("Git clean completed in: %s", dest_dir)

    # remove the .git directory
    git_dir = dest_dir / ".git"
    shutil.rmtree(git_dir, ignore_errors=True)
    logger.info("Removed .git directory: %s", git_dir)

    # remove the rename script
    rename_script = dest_dir / "rename.py"
    rename_script.unlink()
    logger.info("Removed rename script: %s", rename_script)

    # replace 'example-go-cli' with the new name in all files
    for root, dirs, files in dest_dir.walk():
        for file in files:
            file_path: pathlib.Path = pathlib.Path(root) / file
            if file_path.suffix in (".gif",):
                logger.debug("Skipping binary file: %s", file_path)
                continue
            logger.debug("Checking: %s", file_path)
            text = file_path.read_text(encoding="utf-8")
            new_text = text.replace("example-go-cli", args.name)
            if new_text != text:
                logger.debug(
                    "Replacing 'example-go-cli' with '%s' in: %s", args.name, file_path,
                )
                file_path.write_text(new_text, encoding="utf-8")
    logger.info("Replaced 'example-go-cli' with '%s' in all files", args.name)

    # create a new git repository and commit
    logger.info("Initializing new git repository in: %s", dest_dir)
    run("git", "init")
    run("git", "add", ".")
    run("git", "commit", "-m", f"Initial commit for {args.name}")
    logger.info("First commit in: %s", dest_dir)

    logger.info("Continue steps at: https://www.bbkane.com/blog/go-project-notes/#steps")  # noqa: E501


if __name__ == "__main__":
    main()
