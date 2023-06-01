from src.twitchToken import TwitchToken
from requests import Response

REPLAY_PARENT = "@reply-parent-msg-id"

def Pong(ws, _):
    ws.send("PONG :tmi.twitch.tv")
    
def replyWithUsername(ws, message, username):
     ws.send(f"PRIVMSG #{TwitchToken.Channel} :@{username} {message}")
     
def replyToMessage(ws, message, id):
    ws.send(f"{REPLAY_PARENT}={id} PRIVMSG #{TwitchToken.Channel} :Bien recu !")
    
def printHelp(ws, message, **kwargs):
    commands = ", ".join(list(specialCommand.keys()))
    replyWithUsername(ws, f"Commands disponibles: {commands}", kwargs["username"])

def sendSimpleMessage(ws, message):
    ws.send(f"PRIVMSG #{TwitchToken.Channel} :{message}")
    
def sendErrorMessage(ws):
    sendSimpleMessage(ws, f"Une erreur s'est produite, dis le à un modérateur !")

def printOsuRank(ws, message, **kwargs):
    if kwargs["osuToken"]:
        info: Response = kwargs["osuToken"].getRank()
        
        if info.status_code != 200:
            sendErrorMessage(ws)
        else:
            data = info.json()
            country = data.get("country").get('name')
            statistics = data.get("statistics")
            
            rank = {
                "global": statistics.get("global_rank"),
                "country": statistics.get("country_rank"),
            }
            replyWithUsername(ws, f"Le rank de {TwitchToken.Channel} est {rank.get('global')} global et {rank.get('country')} en {country}", kwargs["username"])
    else:
        replyWithUsername(ws, f"Pas de compte osu !", kwargs["username"])

def dispatchSpecialCommand(ws, message, **kwargs):
    if specialCommand.get(message):
        try:
            specialCommand[message](ws, message, **kwargs)
        except Exception as e:
            print(f"Une erreur s'est produite: {e}")
            sendSimpleMessage(ws, "Une erreur s'est produite, dis le à un modérateur !")
    
def Privmsg(ws, info, **kwargs):
    message = info["message"]
    id = info["id"]
    username = info["display-name"]
    
    print(f"Message reçu: {info['message']}")
    if (message.startswith(TwitchToken.Prefix)):
        dispatchSpecialCommand(ws, message, username=username, osuToken=kwargs["osuToken"])
    else:
       replyWithUsername(ws, message, username)
       
specialCommand = {
    "!help": printHelp,
    "!osu": printOsuRank
}
    
commandesFunctions = {
    "PING": Pong,
    "PRIVMSG": Privmsg
}