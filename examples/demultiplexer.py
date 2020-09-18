class Demultiplexer(WebsocketDemultiplexer):

    # Wire your JSON consumers here: {stream_name: consumer}
    consumer_classes = {
        "echo": EchoConsumer,
        "other": AnotherConsumer,
    }