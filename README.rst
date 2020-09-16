=============================
chatter
=============================

.. image:: https://badge.fury.io/py/chatter.svg
    :target: https://badge.fury.io/py/chatter

.. image:: https://travis-ci.org/Ming-Lyu/chatter.svg?branch=master
    :target: https://travis-ci.org/Ming-Lyu/chatter

.. image:: https://codecov.io/gh/Ming-Lyu/chatter/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/Ming-Lyu/chatter

Async Chatter App Based on Webscokets

Documentation
-------------

The full documentation is at https://chatter.readthedocs.io.

Quickstart
----------

Install chatter::

    pip install chatter

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'chatter.apps.chatter',
        ...
    )

Add chatter's URL patterns:

.. code-block:: python

    from chatter import urls as chatter_urls


    urlpatterns = [
        ...
        url(r'^', include(chatter_urls)),
        ...
    ]

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox


Development commands
---------------------

::

    pip install -r requirements_dev.txt
    invoke -l


Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
