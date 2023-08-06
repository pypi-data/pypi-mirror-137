import pathlib
import tempfile

from libvoiced.skeleton import main

__author__ = "Taylor Monacelli"
__copyright__ = "Taylor Monacelli"
__license__ = "MPL-2.0"


def test_main():
    tmpdir = pathlib.Path(tempfile.gettempdir())
    main([str(tmpdir), "--no-menu"])
