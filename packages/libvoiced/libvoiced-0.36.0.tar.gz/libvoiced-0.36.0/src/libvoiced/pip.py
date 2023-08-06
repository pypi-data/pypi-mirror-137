import logging
import pathlib
import shutil
import subprocess
import tempfile
import textwrap
import time


def pip_upgrade(project_path):
    script = pathlib.Path(tempfile.gettempdir()) / f"script_{str(int(time.time()))}.sh"
    out = textwrap.dedent(
        f"""\
    #!/bin/bash
    source {project_path}/.venv/bin/activate
    pip install --upgrade pip
    """
    )
    script.write_text(out)

    cmd = ["bash", f"{script}"]
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
