from channels.routing import route
#  изменить импорт !
from online_game.consumers import ws_connect, ws_message, ws_disconnect

# from online_game.consumers import game_start, game_end, game_proc

channel_routing = [
    route("websocket.connect", ws_connect),
    route("websocket.receive", ws_message),
    route("websocket.disconnect", ws_disconnect),
]

# на будущееее

# custom_routing = [
#     # Handling different chat commands (websocket.receive is decoded and put
#     # onto this channel) - routed on the "command" attribute of the decoded
#     # message.
#     route("game.receive", game_start, command="^start$"),
#     route("game.receive", game_end, command="^end$"),
#     route("game.receive", game_proc, command="^proc$"),
# ]