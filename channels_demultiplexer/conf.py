from typing import Optional, List

# recommended by appconf package to import first
from django.conf import settings
import appconf


class ChannelsDemultiplexerConf(appconf.AppConf):

    # key in message that is used to match the message with its consumer
    MULTIPLEX_KEY = "stream"
    # key in message that contains the actual payload
    PAYLOAD_KEY = "payload"
    # maximum number of seconds consumers have to disconnect
    CONSUMER_CLOSE_TIMEOUT = 5
    # determines whether the envelope is managed by the multiplexer -> only the payload of a message is forwarded to a
    # consumer and messages sent by a consumer are automatically wrapped in an envelope with the consumer's multiplexing
    # key
    MANAGE_ENVELOPE = True

    class Meta:
        prefix = "channels_demultiplexer"
