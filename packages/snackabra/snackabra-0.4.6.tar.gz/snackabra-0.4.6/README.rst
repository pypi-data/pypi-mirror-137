.. image:: snackabra.svg
   :height: 100px
   :align: center
   :alt: The 'michat' Pet Logo

========================
Snackabra Python Library
========================

This repo contains the Python utility libraries for snackabra.

For all snackabra documentation, including this pylib API, see:

* https://snackabra.io
* https://snackabra.github.org

If you would like to contribute or help out with the snackabra
project, please feel free to reach out to us at snackabra@gmail.com or
snackabra@protonmail.com


Installation
============

Requires Python >= 3.8.  If you're simply using the library, you
should just need to install the ``snackabra`` package:

.. code-block:: console

   pip install snackabra


The rest of this README is for package contributors.


Developers
==========


You'll need (Python 3.8 or higher):

.. code-block:: console

   $ python3 -m pip install --upgrade pip
   $ python3 -m venv venv
   $ source venv/bin/activate
   $ pip install -r ./requirement.txt
   $ python -m build

Results will be in 'dist'.

To test deploy to testpypi (you'll need an account and a token, and
use "__token__" as user). 

.. code-block:: console

   python -m twine upload --repository testpypi dist/snackabra-N.N.N*

Remember to bump version number in setup.cfg: "A.B.C" where "A.B"
should match the overall snackabra version numbers, and "C" simply
track fixes to the library - ergo the CLI should simply have a
requirement (for example) ">=0.4.0" if it (the CLI) is version "0.4".

For (final) live update, of course:

.. code-block:: console

   python -m twine upload dist/snackabra-N.N.N*

*Note: don't use wildcard "dist/*".*


Simple Testing
--------------

*(Trivial - actual tests real soon now.)*

.. code-block:: console
		
   # (create a scratch directory)
   $ python3 -m pip install --upgrade pip
   $ python3.8 -m venv venv
   $ source venv/bint/activate
   $ python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps snackabra

Note "no-deps" - the test pip server doesn't have all dependencies (in
our case, last I tried it didn't have jwcrypto), so you manually:


.. code-block:: console

   $ pip install -r ./requirements.txt
   $ python
   >>> import snackabra.crypto
   >>> help(snackabra.crypto)
   


References
==========

* https://packaging.python.org/en/latest/tutorials/packaging-projects/
* https://setuptools.pypa.io/en/latest/userguide/declarative_config.html


Directory
---------

Following files should be present:

::

.
├── LICENSE.md
├── README.rst
├── dist
│   ├── snackabra-N.N.N-py3-none-any.whl
│   └── snackabra-N.N.N.tar.gz
├── pyproject.toml
├── requirements.txt
├── setup.cfg
├── snackabra.svg
└── src
    ├── snackabra
    │   ├── __init__.py
    │   └── crypto.py
    └── snackabra.egg-info
        ├── PKG-INFO
        ├── SOURCES.txt
        ├── dependency_links.txt
        ├── requires.txt
        └── top_level.txt


*Note: we version control some distros.*


LICENSE
-------

Copyright (c) 2016-2021 Magnusson Institute, All Rights Reserved.

"Snackabra" is a registered trademark

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Affero General Public License for more details.

Licensed under GNU Affero General Public License
https://www.gnu.org/licenses/agpl-3.0.html


Cryptography Notice
-------------------

This distribution includes cryptographic software. The country in
which you currently reside may have restrictions on the import,
possession, use, and/or re-export to another country, of encryption
software. Before using any encryption software, please check your
country's laws, regulations and policies concerning the import,
possession, or use, and re-export of encryption software, to see if
this is permitted. See http://www.wassenaar.org/ for more information.

United States: This distribution employs only "standard cryptography"
under BIS definitions, and falls under the Technology Software
Unrestricted (TSU) exception.  Futher, per the March 29, 2021,
amendment by the Bureau of Industry & Security (BIS) amendment of the
Export Administration Regulations (EAR), this "mass market"
distribution does not require reporting (see
https://www.govinfo.gov/content/pkg/FR-2021-03-29/pdf/2021-05481.pdf ).
