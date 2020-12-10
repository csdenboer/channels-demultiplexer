Configuration
=============

The following ``settings.py`` options are available for customizing Channels Demultiplexer's behaviour.

* ``CHANNELS_DEMULTIPLEXER_MULTIPLEX_KEY``: key that is used to (de)multiplex messages. Default: ``stream``
* ``CHANNELS_DEMULTIPLEXER_PAYLOAD_KEY``: key that contains the actual payload. Default: ``payload``
* ``CHANNELS_DEMULTIPLEXER_TIMEOUT``: number of seconds consumers have to handle a disconnect. Default: ``5``
* ``CHANNELS_DEMULTIPLEXER_FORWARD_PAYLOAD_OF_MESSAGE``: If ``True``, only the payload is forwarded to a consumer. Default: ``True``