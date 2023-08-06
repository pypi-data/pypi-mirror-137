# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2022 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""plum-py package builder/installer."""

from setuptools import setup, find_packages

LONG_DESCRIPTION = """
#########################
[plum] Pack/Unpack Memory
#########################

.. image:: https://readthedocs.org/projects/plum-py/badge/?version=latest
    :target: https://plum-py.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

The plum-py Python package provides classes and utility functions to
transform byte sequences into Python objects and back. While similar in
purpose to Python's standard library ``struct`` module, this package
provides a larger set of format specifiers and is extensible, allowing
you to easily create complex ones of your own.
"""

setup(
    name="plum-py",
    version="0.7.3",
    description="Pack/Unpack Memory.",
    long_description=LONG_DESCRIPTION,
    url="https://plum-py.readthedocs.io/en/latest/index.html",
    download_url="https://plum-py.readthedocs.io/en/latest/index.html",
    author="Dan Gass",
    author_email="dan.gass@gmail.com",
    maintainer="Dan Gass",
    maintainer_email="dan.gass@gmail.com",
    license="MIT License; http://opensource.org/licenses/MIT",
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
    ],
    package_dir={"": "src"},
    packages=find_packages("src"),
    package_data={
        "plum": ["py.typed"],
    },
)
