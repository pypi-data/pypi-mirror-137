========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |github-actions| |travis| |appveyor| |requires|
        | |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/python-spihole/badge/?style=flat
    :target: https://python-spihole.readthedocs.io/
    :alt: Documentation Status

.. |travis| image:: https://api.travis-ci.com/zoloft/python-spihole.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.com/github/zoloft/python-spihole

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/zoloft/python-spihole?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/zoloft/python-spihole

.. |github-actions| image:: https://github.com/zoloft/python-spihole/actions/workflows/github-actions.yml/badge.svg
    :alt: GitHub Actions Build Status
    :target: https://github.com/zoloft/python-spihole/actions

.. |requires| image:: https://requires.io/github/zoloft/python-spihole/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/zoloft/python-spihole/requirements/?branch=master

.. |codecov| image:: https://codecov.io/gh/zoloft/python-spihole/branch/master/graphs/badge.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/zoloft/python-spihole

.. |version| image:: https://img.shields.io/pypi/v/spihole.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/spihole

.. |wheel| image:: https://img.shields.io/pypi/wheel/spihole.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/spihole

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/spihole.svg
    :alt: Supported versions
    :target: https://pypi.org/project/spihole

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/spihole.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/spihole

.. |commits-since| image:: https://img.shields.io/github/commits-since/zoloft/python-spihole/v0.0.4.svg
    :alt: Commits since latest release
    :target: https://github.com/zoloft/python-spihole/compare/v0.0.4...master



.. end-badges

Operate a raspberrypi powered peephole camera

* Free software: MIT license

Installation
============

::

    pip install spihole

You can also install the in-development version with::

    pip install https://github.com/zoloft/python-spihole/archive/master.zip


Documentation
=============


https://python-spihole.readthedocs.io/


Development
===========

To run all the tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
