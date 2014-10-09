#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name = "semspaces",
    version = "0.1",
    packages = find_packages(),

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires = ['fs', 'scipy'],

    # metadata for upload to PyPI
    author = "Paweł Mandera",
    author_email = "pawel.mandera@ugent.be",
    description = "This is a package for working with semantic spaces.",
    keywords = "semantic space word vectors",
    # could also include long_description, download_url, classifiers, etc.
)
