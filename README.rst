=============================
django-chats
=============================

.. image:: https://badge.fury.io/py/django-chats.svg
    :target: https://badge.fury.io/py/django-chats

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
    from chatter.api import urls as chatter_api_urls


    urlpatterns = [
        ...
        re_path(r'^', include(chatter_urls)),
        re_path(r'^', include(chatter_api_urls)),
        ...
    ]


Redis is required for group chatting
.. code-block:: python

    # settings
    import platform

    # Configure the redis server
    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels_redis.core.RedisChannelLayer',
            'CONFIG': {
                "hosts": [('192.168.99.100', 6379) if platform.system()=='Windows' else ('127.0.0.1', 6379)],
            },
        },
    }


Official acount username could be specified or by default: "official_account"


Features
--------

* Support Realtime communication through ASGI compatible Server
* Automatically generated official account if not specified
* Message implemented using django-restframework


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

