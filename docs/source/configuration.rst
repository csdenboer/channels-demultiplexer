Configuration
=============

The following ``settings.py`` options are available for customizing Channels Demultiplexer's behaviour.

* ``CHANNELS_DEMULTIPLEXER_MULTIPLEX_KEY``: key that is used to (de)multiplex messages. Default: ``stream``
* ``CHANNELS_DEMULTIPLEXER_PAYLOAD_KEY``: key that contains the actual payload. Default: ``payload``
* ``CHANNELS_DEMULTIPLEXER_TIMEOUT``: number of seconds consumers have to handle a disconnect. Default: ``5``
* ``CHANNELS_DEMULTIPLEXER_MANAGE_ENVELOPE``: If ``True``, only the payload of a message is forwarded to a consumer and messages sent by a consumer are automatically wrapped in an envelope with keys ``CHANNELS_DEMULTIPLEXER_MULTIPLEX_KEY`` and ``CHANNELS_DEMULTIPLEXER_PAYLOAD_KEY`` . Default: ``True``