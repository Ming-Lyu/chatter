=============================
django-chats
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

The full documentation is at https://django-chats.readthedocs.io.

Quickstart
----------

Install chatter::

    pip install django-chats

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'chatter.apps.chatter',
        ...
    )

Add chatter's URL patterns:

.. code-block:: python
    from django.urls import re_path, include
    from chatter import urls as chatter_urls


    urlpatterns = [
        ...
        re_path(r'^', include(chatter_urls)),
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

