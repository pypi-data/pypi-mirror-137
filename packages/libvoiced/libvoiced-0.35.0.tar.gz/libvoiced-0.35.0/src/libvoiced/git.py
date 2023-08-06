import logging
import os
import pathlib
import subprocess


def git_commit_initial(project_path):
    os.chdir(project_path.resolve())
    cmd = [
        "git",
        "commit",
        "-am",
        "Initial",
    ]

    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    try:
        outs, errs = proc.communicate(timeout=15)
        logging.debug(outs.decode())
    except subprocess.TimeoutExpired:
        proc.kill()
        outs, errs = proc.communicate()
        logging.warning(errs.decode())

    logging.debug(errs.decode())


def git_add_all(project_path):
    os.chdir(project_path.resolve())
    cmd = [
        "git",
        "add",
        "-A",
    ]

    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    try:
        outs, errs = proc.communicate(timeout=15)
        logging.debug(outs.decode())
    except subprocess.TimeoutExpired:
        proc.kill()
        outs, errs = proc.communicate()
        logging.warning(errs.decode())

    logging.debug(errs.decode())


def git_init(project_path):
    os.chdir(project_path.resolve())
    cmd = [
        "git",
        "init",
    ]

    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    try:
        outs, errs = proc.communicate(timeout=15)
        logging.debug(outs.decode())
    except subprocess.TimeoutExpired:
        proc.kill()
        outs, errs = proc.communicate()
        logging.warning(errs.decode())

    logging.debug(errs.decode())


def do_all(path):
    os.chdir(path.resolve())
    cwd = pathlib.Path.cwd()
    if not cwd.name == path.name:
        msg = f"blocking if we're not in expected directory {path.resolve()}"
        raise ValueError(msg)
    git_init(path)
    git_add_all(path)
    git_commit_initial(path)
