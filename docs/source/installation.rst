Installation
=======================

Channels Demultiplexer is easy to install from the PyPI index:

.. code-block:: bash

   $ pip install channels-demultiplexer

This will install ``channels-demultiplexer`` along with its dependencies:

* channels 3;
* django-appconf.

After installing the package, the project settings need to be configured.

Add ``channels_demultiplexer`` to your ``INSTALLED_APPS``::

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',

        # Channels Demultiplexer app can be in any position in the INSTALLED_APPS list.
        'channels_demultiplexer',
    ]