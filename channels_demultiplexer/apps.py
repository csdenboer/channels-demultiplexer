from django import apps

# ensure app settings are loaded
from channels_demultiplexer.conf import settings


class ChannelsDemultiplexerConfig(apps.AppConfig):
    name = "channels_demultiplexer"
    verbose_name = "Channels Demultiplexer"
