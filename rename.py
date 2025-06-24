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
    res = subprocess.run(
        args,
        check=True,
        encoding="utf-8",
        stdout=subprocess.PIPE,
        text=True,
    )
    logger.debug(f"stdout:\nr{res.stdout}")


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
    logger.info("Copying: %s to %s", src_dir, dest_dir)
    shutil.copytree(src_dir, dest_dir)

    os.chdir(dest_dir)
    logger.debug("Changed working directory to: %s", os.getcwd())

    # git clean
    logger.info("Cleaning git repository in: %s", dest_dir)
    run("git", "clean", "-fdx")

    # remove the .git directory
    git_dir = dest_dir / ".git"
    logger.info("Removing .git directory: %s", git_dir)
    shutil.rmtree(git_dir, ignore_errors=True)

    # remove the rename script
    rename_script = dest_dir / "rename.py"
    logger.info("Removing rename script: %s", rename_script)
    rename_script.unlink()

    # replace 'example-go-cli' with the new name in all files
    logger.info("Replacing 'example-go-cli' with '%s' in all files", args.name)
    for root, dirs, files in dest_dir.walk():
        for file in files:
            file_path: pathlib.Path = pathlib.Path(root) / file
            logger.debug("Checking: %s", file_path)
            if file_path.suffix in (".gif",):
                logger.debug("Skipping binary file: %s", file_path)
                continue
            text = file_path.read_text(encoding="utf-8")
            new_text = text.replace("example-go-cli", args.name)
            if new_text != text:
                logger.debug(
                    "Replacing 'example-go-cli' with '%s' in: %s", args.name, file_path,
                )
                file_path.write_text(new_text, encoding="utf-8")

    # create a new git repository and commit
    logger.info("Initializing new git repository in: %s", dest_dir)
    run("git", "init")
    run("git", "add", ".")
    run("git", "commit", "-m", shlex.quote(f"Initial commit for {args.name}"))
    logger.info("First commit in: %s", dest_dir)

    logger.info("Continue steps at: https://www.bbkane.com/blog/go-project-notes/#steps")  # noqa: E501


if __name__ == "__main__":
    main()
