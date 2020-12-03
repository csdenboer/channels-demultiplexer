from channels.generic import websocket
from channels.testing import WebsocketCommunicator
import pytest

from channels_demultiplexer.demultiplexer import WebsocketDemultiplexer


@pytest.mark.asyncio
async def test_connect():
    class MyWebsocketConsumer(websocket.AsyncJsonWebsocketConsumer):
        pass

    class Demultiplexer(WebsocketDemultiplexer):
        consumer_classes = {"echo": MyWebsocketConsumer}

    communicator = WebsocketCommunicator(Demultiplexer.as_asgi(), "/")

    connected, subprotocol = await communicator.connect()

    assert connected

    await communicator.disconnect()


@pytest.mark.asyncio
async def test_receive_json_missing_multiplex_key():
    class Demultiplexer(WebsocketDemultiplexer):
        consumer_classes = {}

    demultiplexer = Demultiplexer()

    with pytest.raises(ValueError) as excinfo:
        await demultiplexer.receive_json({"payload": {}})

    assert "Invalid multiplexed **frame received (no channel/payload key)" == str(
        excinfo.value
    )


@pytest.mark.asyncio
async def test_receive_json_missing_payload_key():
    class Demultiplexer(WebsocketDemultiplexer):
        consumer_classes = {}

    demultiplexer = Demultiplexer()

    with pytest.raises(ValueError) as excinfo:
        await demultiplexer.receive_json({"stream": "echo"})

    assert "Invalid multiplexed **frame received (no channel/payload key)" == str(
        excinfo.value
    )


@pytest.mark.asyncio
async def test_receive_json_unknown_multiplex_key():
    class Demultiplexer(WebsocketDemultiplexer):
        consumer_classes = {}

    demultiplexer = Demultiplexer()

    with pytest.raises(ValueError) as excinfo:
        await demultiplexer.receive_json({"stream": "echo", "payload": {}})

    assert "Invalid multiplexed frame received (stream not mapped)" == str(
        excinfo.value
    )


@pytest.mark.asyncio
async def test_receive_json_success():
    class MyWebsocketConsumer(websocket.AsyncJsonWebsocketConsumer):
        async def receive_json(self, content, **kwargs):
            await self.send_json(content)

    class Demultiplexer(WebsocketDemultiplexer):
        consumer_classes = {"echo": MyWebsocketConsumer}

    communicator = WebsocketCommunicator(Demultiplexer.as_asgi(), "/")

    await communicator.connect()

    # missing type
    await communicator.send_json_to({"stream": "echo", "payload": {}})

    response = await communicator.receive_json_from()
    assert response == {"stream": "echo", "payload": {}}

    await communicator.disconnect()


@pytest.mark.asyncio
async def test_send_json_multiplexed_success():
    class MyWebsocketConsumer(websocket.AsyncJsonWebsocketConsumer):
        async def receive_json(self, content, **kwargs):
            await self.send_json({"success": True})

    class Demultiplexer(WebsocketDemultiplexer):
        consumer_classes = {"echo": MyWebsocketConsumer}

    communicator = WebsocketCommunicator(Demultiplexer.as_asgi(), "/")

    await communicator.connect()

    # missing type
    await communicator.send_json_to({"stream": "echo", "payload": {}})

    response = await communicator.receive_json_from()
    assert response == {"stream": "echo", "payload": {"success": True}}

    await communicator.disconnect()


@pytest.mark.asyncio
async def test_settings_multiplex_key(settings):
    settings.CHANNELS_DEMULTIPLEXER_MULTIPLEX_KEY = "type"

    class Demultiplexer(WebsocketDemultiplexer):
        consumer_classes = {}

    demultiplexer = Demultiplexer()

    with pytest.raises(ValueError) as excinfo:
        await demultiplexer.receive_json({"stream": "echo", "payload": {}})

    assert "Invalid multiplexed **frame received (no channel/payload key)" == str(
        excinfo.value
    )


@pytest.mark.asyncio
async def test_settings_payload_key(settings):
    settings.CHANNELS_DEMULTIPLEXER_PAYLOAD_KEY = "body"

    class Demultiplexer(WebsocketDemultiplexer):
        consumer_classes = {}

    demultiplexer = Demultiplexer()

    with pytest.raises(ValueError) as excinfo:
        await demultiplexer.receive_json({"stream": "echo", "payload": {}})

    assert "Invalid multiplexed **frame received (no channel/payload key)" == str(
        excinfo.value
    )
