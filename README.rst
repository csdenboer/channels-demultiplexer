
channels-demultiplexer
=======================

.. image:: https://img.shields.io/github/stars/csdenboer/channels-demultiplexer.svg?label=Stars&style=socialcA
   :target: https://github.com/csdenboer/channels-demultiplexer
   :alt: GitHub

.. image:: https://img.shields.io/pypi/v/channels-demultiplexer.svg
   :target: https://pypi.org/project/channels-demultiplexer/
   :alt: PyPI release

.. image:: https://img.shields.io/readthedocs/channels-demultiplexer.svg
   :target: https://channels-demultiplexer.readthedocs.io/
   :alt: Documentation

.. image:: https://secure.travis-ci.org/csdenboer/channels-demultiplexer.svg?branch=master
   :target: http://travis-ci.org/csdenboer/channels-demultiplexer
   :alt: Build Status

.. image:: https://codecov.io/gh/csdenboer/channels-demultiplexer/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/csdenboer/channels-demultiplexer
   :alt: Coverage

(De)multiplexer for Django Channels 3 (and 2)

Functionality
-------------

Channels Demultiplexer provides a standard way to multiplex different data streams over a single websocket.

It expects JSON-formatted WebSocket frames with two keys, stream and payload (both configurable). It matches the stream against a mapping to find a consumer and subsequently forwards the message. Consumers do not require any modifications in order to be plugged in to a (de)multiplexer, so you can hook them directly in the ``routing.py`` file as well as in a (de)multiplexer.

Quickstart
-------------

Install using `pip`:

.. code-block:: bash

   $ pip install channels-demultiplexer

Add ``channels_demultiplexer`` to your ``INSTALLED_APPS``

.. code-block:: python

    INSTALLED_APPS = [
        # channels_demultiplexer can be in any position in the INSTALLED_APPS list.
        "channels_demultiplexer",
    ]

Create a demultiplexer in ``demultiplexer.py``:

.. code-block:: python

    from channels_demultiplexer.demultiplexer import WebsocketDemultiplexer

    from .consumers import EchoConsumer, AnotherConsumer

    class Demultiplexer(WebsocketDemultiplexer):
        # Wire your async JSON consumers here: {stream_name: consumer}
        consumer_classes = {
            "echo": EchoConsumer,
            "other": AnotherConsumer,
        }

Add the demultiplexer to your Channels routing configuration:

.. code-block:: python

    from channels.routing import ProtocolTypeRouter, URLRouter
    from django.conf.urls import url
    from django.core.asgi import get_asgi_application

    from .demultiplexer import Demultiplexer

    application = ProtocolTypeRouter
        "http": get_asgi_application(),
        "websocket": URLRouter([
            url(r"^/$", Demultiplexer.as_asgi()),
        ])
    })

Documentation
-------------

For more information on installation and configuration see the documentation at:

https://channels-demultiplexer.readthedocs.io/


Issues
------

If you have questions or have trouble using the app please file a bug report at:

https://github.com/csdenboer/channels-demultiplexer/issues


Contributions
-------------

It is best to separate proposed changes and PRs into small, distinct patches
by type so that they can be merged faster into upstream and released quicker:

* features,
* bugfixes,
* code style improvements, and
* documentation improvements.

All contributions are required to pass the quality gates configured
with the CI. This includes running tests and linters successfully
on the currently officially supported Python and Django versions.

The test automation is run automatically by Travis CI, but you can
run it locally with the ``tox`` command before pushing commits.
