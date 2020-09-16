=====
Usage
=====

To use chatter in a project, add it to your `INSTALLED_APPS`:

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
