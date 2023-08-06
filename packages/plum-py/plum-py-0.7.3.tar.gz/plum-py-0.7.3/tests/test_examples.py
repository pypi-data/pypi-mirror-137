# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Verify accuracy of example code in all docstrings and RST files."""

import doctest
import os

import pytest


def get_docfiles():
    """Walk repository and return list of all .rst and .py files.

    :returns: list of all .py and .rst files
    :rtype: list of str

    """
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    docfiles = []

    for subdir in ["docs", "src", "boost"]:
        for dirpath, _dirnames, filenames in os.walk(os.path.join(root, subdir)):
            if os.path.join("plum-py", "build") in dirpath:
                continue
            for filename in filenames:
                if os.path.splitext(filename)[1] not in {".rst", ".py"}:
                    continue
                if ".tox" in dirpath:
                    continue  # do not test examples from 3rd-party packages
                if filename in "about.rst":
                    continue  # contains examples of future functionality
                docfiles.append(os.path.join(dirpath, filename))
    return docfiles


OPTION_FLAGS = doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE

DOCS_WITH_ENUMS = ("index.rst", "bitfields.rst", "enum.rst", "flag.rst")


@pytest.mark.parametrize("docfile", get_docfiles())
def test_examples(docfile):
    """Test interactive examples in documentation file.

    :param str docfile: path of RST file

    """
    if os.path.basename(docfile) not in DOCS_WITH_ENUMS:
        failure_count, _test_count = doctest.testfile(
            docfile, module_relative=False, optionflags=OPTION_FLAGS
        )

        assert failure_count == 0
