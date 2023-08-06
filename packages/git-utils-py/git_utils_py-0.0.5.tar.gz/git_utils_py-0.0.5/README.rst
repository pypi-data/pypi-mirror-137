git-utils-py
=============

.. image:: https://badge.fury.io/py/git-utils-py.svg
   :target: https://badge.fury.io/py/git-utils-py

.. image:: https://img.shields.io/pypi/pyversions/git-utils-py.svg
   :target: https://pypi.python.org/pypi/git-utils-py

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/python/black

``git-utils-py`` is a Python package providing utils task to the Git.

Installation
------------

As of 0.0.5, ``git-utils-py`` is compatible with Python 3.7+.

Use ``pip`` to install the latest stable version of ``git-utils-py``:

.. code-block:: console

   $ pip install --upgrade git-utils-py

Command
-------------
download_file(host, token, project_name, project_id, file_search_path, file_search_name, file_search_extension,
file_output_path, file_output_name=None, branch_name='master')
