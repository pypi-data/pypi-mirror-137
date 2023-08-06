ipydatatable
===============================
[![Version](https://img.shields.io/pypi/v/ipydatatable.svg)](https://pypi.python.org/pypi/ipydatatable)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gl/teia_engineering%2Fipydatatable/master?filepath=examples)
[![Documentation Status](http://readthedocs.org/projects/ipydatatable/badge/?version=latest)](https://ipydatatable.readthedocs.io/)

Library to wrap interactive datatables js into a library that helps pandas dataframes

Installation
------------

To install use pip:

    $ pip install ipydatatable

After that if using Classic Jupyter you need to activate the extension

    $ jupyter nbextension install --py ipydatatable

If using JupyterLab you need to build the library with the following command

    $ jupyter labextension install ipydatatable

When Developing
---------------

For a development installation (requires [Node.js](https://nodejs.org) and [Yarn version 1](https://classic.yarnpkg.com/)),

    $ git clone https://github.com//ipydatatable.git
    $ cd ipydatatable
    $ pip install -e .
    $ jupyter nbextension install --py --symlink --overwrite --sys-prefix ipydatatable
    $ jupyter nbextension enable --py --sys-prefix ipydatatable

When actively developing your extension for JupyterLab, run the command:

    $ jupyter labextension develop --overwrite ipydatatable

Then you need to rebuild the JS when you make a code change:

    $ cd js
    $ yarn run build

You then need to refresh the JupyterLab page when your javascript changes.
