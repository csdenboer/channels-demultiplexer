import asyncio
from functools import partial
import logging
from typing import Dict, Type, Any, List

from channels.exceptions import StopConsumer
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from .conf import settings
from .queue import MessageQueue

logger = logging.getLogger(__name__)

__all__ = ("WebsocketDemultiplexer",)


class WebsocketDemultiplexer(AsyncJsonWebsocketConsumer):
    """
    Async JSON-understanding WebSocket consumer subclass that handles
    multiplexing and demultiplexing streams using a "stream" key in a
    top-level dict and the actual payload in a sub-dict called "payload"
    (both configurable). This lets you run multiple streams over a single
    WebSocket connection in a standardised way.
    """

    # mapping between stream and multiplexed consumer
    consumer_classes: Dict[str, Type[AsyncJsonWebsocketConsumer]] = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._consumers: Dict[str, AsyncJsonWebsocketConsumer] = {}
        self._input_queues: Dict[str, MessageQueue] = {}

        for stream, consumer in self.consumer_classes.items():
            self._consumers[stream] = consumer(*args)
            # patch send_json so that messages are multiplexed
            self._consumers[stream].send_json = partial(
                self._send_json_multiplexed, stream
            )
            # patch accept so that connections are only accepted by the multiplexer
            self._consumers[stream].accept = self._accept_multiplexed

            self._input_queues[stream] = MessageQueue()

    async def __call__(self, scope, receive, send):
        await asyncio.wait(
            [super().__call__(scope, receive, send)]
            + [
                consumer(
                    scope,
                    self._input_queues[stream].get,
                    send,
                )
                for stream, consumer in self._consumers.items()
            ]
        )

    async def connect(self):
        """
        Called when a WebSocket connection is opened.
        """
        for input_queue in self._input_queues.values():
            await input_queue.put({"type": "websocket.connect"})

        await super().connect()

    async def receive_json(self, content: dict, **kwargs):
        """
        Demultiplex message by matching it with a consumer.
        """
        if (
            isinstance(content, dict)
            and settings.CHANNELS_DEMULTIPLEXER_MULTIPLEX_KEY in content
            and settings.CHANNELS_DEMULTIPLEXER_PAYLOAD_KEY in content
        ):
            try:
                input_queue = self._input_queues[
                    content[settings.CHANNELS_DEMULTIPLEXER_MULTIPLEX_KEY]
                ]
            except KeyError:
                raise ValueError(
                    "Invalid multiplexed frame received (stream not mapped)"
                )
            else:
                # add message to the queue
                await input_queue.put(
                    {
                        "type": "websocket.receive",
                        "text": await self.encode_json(
                            content[settings.CHANNELS_DEMULTIPLEXER_PAYLOAD_KEY]
                        ),
                    }
                )
        else:
            raise ValueError(
                "Invalid multiplexed **frame received (no channel/payload key)"
            )

    async def close(self, code=None):
        """
        Closes the WebSocket from the server end.
        """
        # let all child applications close first
        await self._disconnect_consumers({"type": "websocket.disconnect", "code": code})

        await super().close(code)

    async def websocket_disconnect(self, message: dict):
        """
        Called when a WebSocket connection is closed.
        """
        # let all child applications close first
        await self._disconnect_consumers(message)

        # raise StopConsumer to halt the ASGI application cleanly and let the server clean it up
        raise StopConsumer()

    async def _send_json_multiplexed(self, stream: str, content: Any, close=False):
        """
        Multiplex message.
        """
        await self.send_json(
            {
                settings.CHANNELS_DEMULTIPLEXER_MULTIPLEX_KEY: stream,
                settings.CHANNELS_DEMULTIPLEXER_PAYLOAD_KEY: content,
            },
            close,
        )

    async def _accept_multiplexed(self, subprotocol=None):
        """
        Connections may only be accepted once and handling is done by the (de)multiplexer.
        """
        pass

    async def _disconnect_consumers(self, message: dict):
        """
        Disconnect consumers by sending message and block untill all items in the input queues have been processed.
        """
        streams = list(self._input_queues.keys())
        input_queues = list(self._input_queues.values())

        for stream, input_queue in zip(streams, input_queues):
            # pop input queue so no new messages can be put
            self._input_queues.pop(stream)
            await input_queue.put(message)

        await self._join_queues(input_queues)

    @classmethod
    async def _join_queues(cls, queues: List[MessageQueue]):
        await asyncio.wait(
            [input_queue.join() for input_queue in queues],
            timeout=settings.CHANNELS_DEMULTIPLEXER_CONSUMER_CLOSE_TIMEOUT,
        )
