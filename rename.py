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


class Color:
    reset = '\x1b[0m'
    grey = '\x1b[38;21m'
    blue = '\x1b[38;5;39m'
    yellow = '\x1b[38;5;226m'
    red = '\x1b[38;5;196m'
    bold_red = '\x1b[31;1m'


# logic from https://stackoverflow.com/a/75339761
class ColorLevelFormatter(logging.Formatter):

    _color_levelname = {
        'DEBUG': f"{Color.grey}DEBUG{Color.reset}",
        'INFO': f"{Color.blue}INFO{Color.reset}",
        'WARNING': f"{Color.yellow}WARNING{Color.reset}",
        'ERROR': f"{Color.red}ERROR{Color.reset}",
        'CRITICAL': f"{Color.bold_red}CRITICAL{Color.reset}",
    }

    def __init__(
            self,
            fmt: str = "%(levelname)s %(filename)s:%(lineno)s : %(message)s",
            *args,
            **kwargs,
    ):
        super().__init__(fmt, *args, **kwargs)

    def format(self, record):
        record.levelname = self._color_levelname[record.levelname]
        return super().format(record)


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
        encoding="utf-8",
        capture_output=True,
        text=True,
    )
    level = logging.DEBUG
    if res.returncode != 0:
        level = logging.ERROR
        logger.error(f"Command failed with return code: {res.returncode}")
    if res.stdout:
        logger.log(level, f"stdout:\n{res.stdout}")
    else:
        logger.log(level, "no stdout")
    if res.stderr:
        logger.log(level, f"stderr:\n{res.stderr}")
    else:
        logger.log(level, "no stderr")

    if res.returncode != 0:
        sys.exit(res.returncode)


def main():
    parser = build_parser()
    args = parser.parse_args()

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.getLevelNamesMapping()[args.log_level])
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(ColorLevelFormatter())
    root_logger.addHandler(stdout_handler)

    # copy the example-go-cli directory to the new name
    projects_dir = pathlib.Path(__file__).parent.parent.resolve()
    src_dir = projects_dir / "example-go-cli"
    dest_dir = projects_dir / args.name
    logger.info("Copying: %s to %s", src_dir, dest_dir)
    shutil.copytree(src_dir, dest_dir)

    logger.debug("Changing working directory to: %s", os.getcwd())
    os.chdir(dest_dir)

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
    run("git", "commit", "-m", f"Initial commit for {args.name}")
    logger.info("First commit in: %s", dest_dir)

    # create upstream repo, add go topic, and push
    logger.info("Creating upstream repository for %s", args.name)
    run("gh", "repo", "create", args.name, "--public", "--source", ".", "--remote", "origin")  # noqa: E501
    logger.info("Adding 'go' topic to repo")
    run("gh", "repo", "edit", "--add-topic", "go")
    logger.info("pushing")
    run("git", "push")

    logger.info("Continue steps at: https://www.bbkane.com/blog/go-project-notes/#steps")  # noqa: E501


if __name__ == "__main__":
    main()
