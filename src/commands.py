from tokenHandler import TokenHandler

REPLAY_PARENT = "@reply-parent-msg-id"

def Pong(ws, _):
    ws.send("PONG :tmi.twitch.tv")
    
def replyWithUsername(ws, message, username):
     ws.send(f"PRIVMSG #{TokenHandler.TwitchChannel} :@{username} {message}")
     
def replyToMessage(ws, message, id):
    ws.send(f"{REPLAY_PARENT}={id} PRIVMSG #{TokenHandler.TwitchChannel} :Bien recu !")
    
def printHelp(ws, message, **kwargs):
    commands = ",".join(list(specialCommand.keys()))
    replyWithUsername(ws, f"Commands disponibles: {commands}", kwargs["username"])

def dispatchSpecialCommand(ws, message, **kwargs):
    if specialCommand.get(message):
        specialCommand[message](ws, message, **kwargs)
    
def Privmsg(ws, info):
    message = info["message"]
    id = info["id"]
    username = info["display-name"]
    
    print(f"Message reçu: {info['message']}")
    if (message.startswith(TokenHandler.Prefix)):
        dispatchSpecialCommand(ws, message, username=username)
    else:
       replyWithUsername(ws, message, username)
       
specialCommand = {
    "!help": printHelp
}
    
commandesFunctions = {
    "PING": Pong,
    "PRIVMSG": Privmsg
}