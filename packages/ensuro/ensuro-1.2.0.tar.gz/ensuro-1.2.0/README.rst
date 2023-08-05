.. These are examples of badges you might want to add to your README:
   please update the URLs accordingly

    .. image:: https://api.cirrus-ci.com/github/<USER>/ensuro.svg?branch=main
        :alt: Built Status
        :target: https://cirrus-ci.com/github/<USER>/ensuro
    .. image:: https://readthedocs.org/projects/ensuro/badge/?version=latest
        :alt: ReadTheDocs
        :target: https://ensuro.readthedocs.io/en/stable/
    .. image:: https://img.shields.io/coveralls/github/<USER>/ensuro/main.svg
        :alt: Coveralls
        :target: https://coveralls.io/r/<USER>/ensuro
    .. image:: https://img.shields.io/pypi/v/ensuro.svg
        :alt: PyPI-Server
        :target: https://pypi.org/project/ensuro/
    .. image:: https://img.shields.io/conda/vn/conda-forge/ensuro.svg
        :alt: Conda-Forge
        :target: https://anaconda.org/conda-forge/ensuro
    .. image:: https://pepy.tech/badge/ensuro/month
        :alt: Monthly Downloads
        :target: https://pepy.tech/project/ensuro
    .. image:: https://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Twitter
        :alt: Twitter
        :target: https://twitter.com/ensuro

.. image:: https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold
    :alt: Project generated with PyScaffold
    :target: https://pyscaffold.org/

|

======
ensuro
======


    Prototype and wrappers to work with Ensuro Smart Contracts


This package is for working with the Ensuro Protocol (https://github.com/ensuro/ensuro) from Python.

It includes the prototype written in pure-python that can be used for simulation of Ensuro. Also includes
the wrappers that together with the compiled contracts can be used to deploy or use contracts deployed on the
blockchain.



Copying files from Ensuro main repository
=========================================

Instructions to copy files from ensuro repository::

    for x in `find ../ensuro/artifacts/contracts/ ../ensuro/artifacts/interfaces/ -name "*.json" -not -name "*.dbg.json" | grep -v /dependencies/ `; do
        cp $x src/ensuro/contracts/ ;
    done
    cp ../ensuro/prototype/ensuro.py src/ensuro/prototype.py
    cp ../ensuro/prototype/wrappers.py src/ensuro/wrappers.py
    cp ../ensuro/prototype/utils.py src/ensuro/utils.py


.. _pyscaffold-notes:

Note
====

This project has been set up using PyScaffold 4.1.1. For details and usage
information on PyScaffold see https://pyscaffold.org/.
