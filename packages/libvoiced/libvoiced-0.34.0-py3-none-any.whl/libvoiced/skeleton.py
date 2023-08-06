"""
This is a skeleton file that can serve as a starting point for a Python
console script. To run this script uncomment the following lines in the
``[options.entry_points]`` section in ``setup.cfg``::

    console_scripts =
         fibonacci = libvoiced.skeleton:run

Then run ``pip install .`` (or ``pip install -e .`` for editable mode)
which will install the command ``fibonacci`` inside your current environment.

Besides console scripts, the header (i.e. until ``_logger``...) of this file can
also be used as template for Python modules.

Note:
    This skeleton file can be safely removed if not needed!

References:
    - https://setuptools.pypa.io/en/latest/userguide/entry_point.html
    - https://pip.pypa.io/en/stable/reference/pip_install
"""

import argparse
import logging
import pathlib
import sys

from clinepunk import clinepunk

from libvoiced import __version__, direnv, putup, venv

__author__ = "Taylor Monacelli"
__copyright__ = "Taylor Monacelli"
__license__ = "MPL-2.0"

_logger = logging.getLogger(__name__)


def parse_args(args):
    """Parse command line parameters

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--help"]``).

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(
        description="Create a new project using random words"
    )
    parser.add_argument(
        "--version",
        action="version",
        version="libvoiced {ver}".format(ver=__version__),
    )
    parser.add_argument(
        "basepath",
        nargs="?",
        default=".",
        help="base directory for where to put new package",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
    )
    parser.add_argument(
        "-nm",
        "--no-menu",
        action="store_true",
        help="just create one project without allowing to choose the name",
    )
    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )
    parser.add_argument(
        "-n",
        "--name",
        dest="name",
        help="instead of choosing a random name, use this name",
    )
    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    # logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    format_stream = "{%(filename)s:%(lineno)d} %(levelname)s - %(message)s"  # console
    logging.basicConfig(
        level=loglevel,
        stream=sys.stdout,
        format=format_stream,
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def get_unused_path(root):
    def doit():
        words = clinepunk.sample(count=2)
        name = "".join(words)
        path = pathlib.Path(root) / name
        return path

    path = doit()
    while path.exists():
        path = doit()

    return path


def run_putup(path):
    _logger.info(f"creating new project in {path}")
    putup.putup(path)


def select_with_menu(basepath) -> pathlib.Path:
    from simple_term_menu import TerminalMenu

    paths = [get_unused_path(basepath) for _ in range(20)]
    options = [str(path.name) for path in paths]
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    _logger.debug(f"menu_entry_index={menu_entry_index}")
    if menu_entry_index is None:
        return None
    path = basepath / options[menu_entry_index]
    return path


def select_without_menu(basepath):
    return get_unused_path(basepath)


def main(args):
    args = parse_args(args)
    setup_logging(args.loglevel)

    basepath = pathlib.Path(args.basepath)

    if not args.name:
        if args.no_menu:
            path = select_without_menu(basepath)
        else:
            path = select_with_menu(basepath)
    else:
        path = basepath / args.name

    _logger.debug(f"path={path}")

    if path:
        _logger.info(f"creating new project in {path.resolve()}")
        run_putup(path)
        venv.create_virtualenv(path)
        direnv.setup(path)
        # git.do_all(path)
        print(path)

    _logger.info("Script ends here")


def run():
    """Calls :func:`main` passing the CLI arguments extracted from :obj:`sys.argv`

    This function can be used as entry point to create console scripts with setuptools.
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    # After installing your project with pip, users can also run your Python
    # modules as scripts via the ``-m`` flag, as defined in PEP 338::
    #
    #     python -m libvoiced.skeleton
    #
    run()
