pl-ocr_tool
================================

.. image:: https://img.shields.io/docker/v/fnndsc/pl-ocr_tool?sort=semver
    :target: https://hub.docker.com/r/fnndsc/pl-ocr_tool

.. image:: https://img.shields.io/github/license/fnndsc/pl-ocr_tool
    :target: https://github.com/FNNDSC/pl-ocr_tool/blob/master/LICENSE

.. image:: https://github.com/FNNDSC/pl-ocr_tool/workflows/ci/badge.svg
    :target: https://github.com/FNNDSC/pl-ocr_tool/actions


.. contents:: Table of Contents


Abstract
--------

An application that can take images as input and identify and extract written text from them.
Idea users of this tool includes doctors, healthcare professionals or anyone familiar with the ChRIS project


Description
-----------


``ocr_tool`` is a *ChRIS ds-type* application that takes in images as  files
and produces text.


Usage
-----

.. code::

    docker run --rm fnndsc/pl-ocr_tool ocr_tool
        [-h|--help]
        [--json] [--man] [--meta]
        [--savejson <DIR>]
        [-v|--verbosity <level>]
        [--version]
        <inputDir> <outputDir>


Arguments
~~~~~~~~~

.. code::

    [-h] [--help]
    If specified, show help message and exit.
    
    [--json]
    If specified, show json representation of app and exit.
    
    [--man]
    If specified, print (this) man page and exit.

    [--meta]
    If specified, print plugin meta data and exit.
    
    [--savejson <DIR>] 
    If specified, save json representation file to DIR and exit. 
    
    [-v <level>] [--verbosity <level>]
    Verbosity level for app. Not used currently.
    
    [--version]
    If specified, print version number and exit. 

    [--langdetect]
    If specified, print lang on image and exit.


Getting inline help is:

.. code:: bash

    docker run --rm fnndsc/pl-ocr_tool ocr_tool --man

Run
~~~

You need to specify input and output directories using the `-v` flag to `docker run`.


.. code:: bash

    docker run --rm -u $(id -u)                             \
        -v $(pwd)/in:/incoming -v $(pwd)/out:/outgoing      \
        fnndsc/pl-ocr_tool ocr_tool                        \
        /incoming /outgoing


Development
-----------

Build the Docker container:

.. code:: bash

    docker build -t local/pl-ocr_tool .

Run unit tests:

.. code:: bash

    docker run --rm local/pl-ocr_tool nosetests

Examples
--------

Put some examples here!


.. image:: https://raw.githubusercontent.com/FNNDSC/cookiecutter-chrisapp/master/doc/assets/badge/light.png
    :target: https://chrisstore.co
