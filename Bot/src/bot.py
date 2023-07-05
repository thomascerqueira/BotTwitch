from src.twitchToken import TwitchToken
from src.osuToken import OsuToken
from src.parserTwitch import ParserTwitch
import os
import websocket
from src.commands import commandesFunctions

class Bot():
    def __init__(self, twitchToken: TwitchToken, osuToken: OsuToken = None):
        self.twitchToken: TwitchToken = twitchToken
        self.osuToken: OsuToken = osuToken
        self.parser: ParserTwitch = ParserTwitch()
        self.prefixe = os.getenv("PREFIXE")
        self.ws = None
        self.url = f"wss://irc-ws.chat.twitch.tv:443"
        
        self.connectToTwitch()
        
    def connectToTwitch(self):
        self.ws = websocket.WebSocketApp(self.url,
                                    on_message=self.onMessage,
                                    on_error=self.onError,
                                    on_close=self.onClose)
        self.ws.on_open = self.onOpen
        self.ws.run_forever()
    
    def onOpen(self, socket):
        print("Connexion au chat Twitch ouverte")
        socket.send(f"PASS oauth:{self.twitchToken.tokens}")
        socket.send(f"NICK {self.twitchToken.Nick}")
        socket.send(f"JOIN #{self.twitchToken.Channel}")
        socket.send(f"CAP REQ :twitch.tv/commands twitch.tv/tags")
    
    def sendMessage(self, socket, message):
        message = f"PRIVMSG #{self.twitchToken.Channel} :{message}"
        socket.send(message)
        
    def dispatchCommand(self, message):
        if commandesFunctions.get(message["command"]):
            commandesFunctions[message["command"]](self.ws, message, osuToken=self.osuToken)
        else:
            print(f"Commande {message['command']} non reconnue")
    
    def onMessage(self, socket, message):
        messages = self.parser.parseMessages(message)
        for message in messages:
            self.dispatchCommand(message)
        
    def onError(self, socket, error):
        print(f"Erreur dans la connexion au chat Twitch: {error}")
    
    
    def onClose(self, socket, close_status_code, close_msg):
        print("Connexion au chat Twitch fermée")