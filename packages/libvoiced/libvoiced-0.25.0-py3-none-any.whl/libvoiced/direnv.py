import logging
import pathlib
import subprocess
import textwrap


def ensure_directory(folder: pathlib.Path):
    logging.debug(f"verify {folder} is a directory")
    if not folder.is_dir():
        msg = f"expecting folder for {folder}"
        logging.exception(msg)
        raise ValueError(msg)


def create_envrc(folder: pathlib.Path):
    ensure_directory(folder)
    path = folder / ".envrc"

    tpl = textwrap.dedent(
        """\
    export VIRTUAL_ENV=.venv/
    PATH_add "$VIRTUAL_ENV/bin"
    """
    )
    if path.exists():
        logging.warning(f"skipping overwrite of {path}")
    else:
        logging.debug(f"creating {path}")
        path.write_text(tpl)
    return path


def allow_direnv(rc_path: pathlib.Path):
    logging.debug(f"allowing direnv to load {rc_path}")
    cmd = ["direnv", "allow", str(rc_path)]
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

    if errs:
        logging.warning(f"failed to run {' '.join(cmd)}, error: {errs.decode()}")
    else:
        logging.debug(f"ran ok: {' '.join(cmd)}")
