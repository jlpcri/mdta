from channels import Group
from channels.sessions import channel_session


# Connected to websocket.connect
@channel_session
def ws_add(message):
    # Accept the connection
    message.reply_channel.send({"accept": True})
    # Add to the chat group
    Group("chat").add(message.reply_channel)


# Connected to websocket.receive
@channel_session
def ws_message(message):

    Group("chat").send({
        "text": message.content['text'],
    })


# Connected to websocket.disconnect
@channel_session
def ws_disconnect(message):
    Group("chat").discard(message.reply_channel)
