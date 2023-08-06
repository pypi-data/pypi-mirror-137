import logging
import os
import pathlib
import subprocess


def do_work(path):
    os.chdir(path)
    cmd = [
        "python3",
        "-mvenv",
        ".venv",
    ]
    s1 = " ".join(cmd)
    logging.debug(s1)

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


def create_virtualenv(project_path):
    cwd = pathlib.Path.cwd()
    try:
        do_work(project_path)
    except Exception as ex:
        msg = "Something went wrong"
        logging.exception(msg)
        raise ex
    finally:
        os.chdir(cwd)
