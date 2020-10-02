class Demultiplexer(WebsocketDemultiplexer):
    # Wire your async JSON consumers here: {stream_name: consumer}
    consumer_classes = {
        "echo": EchoConsumer,
        "other": AnotherConsumer,
    }