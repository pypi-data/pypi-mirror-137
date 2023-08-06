import logging
import pathlib
import shutil
import subprocess
import tempfile
import time


def putup(project_path):
    unique_id = int(time.time())
    tmp_dir = pathlib.Path(tempfile.gettempdir()) / str(unique_id) / project_path.name
    tmp_dir.parent.mkdir()

    cmd = [
        "putup",
        "--pre-commit",
        f"{tmp_dir.resolve()}",
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

    logging.debug(f"moving {tmp_dir} to {project_path}")
    shutil.move(tmp_dir, project_path)
