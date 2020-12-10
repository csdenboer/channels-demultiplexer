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
    # determines whether only the payload is forwarded to the consumer or the full original message
    FORWARD_PAYLOAD_OF_MESSAGE = True

    class Meta:
        prefix = "channels_demultiplexer"
