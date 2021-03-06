from channels.routing import route
from mdta.ws_consumers import ws_connect, ws_message, ws_disconnect

path = r"^/mdta/(?P<room_name>[a-zA-Z0-9_]+)/$"
channel_routing = [
    route("websocket.connect", ws_connect, path=path),
    route("websocket.receive", ws_message, path=path),
    route("websocket.disconnect", ws_disconnect, path=path),
]
