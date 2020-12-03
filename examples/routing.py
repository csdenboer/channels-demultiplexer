application = ProtocolTypeRouter({
    "websocket": URLRouter([
        url(r"^/$", Demultiplexer.as_asgi()),
    ])
})