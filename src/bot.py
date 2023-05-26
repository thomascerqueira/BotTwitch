from tokenHandler import TokenHandler
from parserTwitch import ParserTwitch
import os
import websocket
from commands import commandesFunctions

class Bot():
    def __init__(self, tokenHandler: TokenHandler):
        self.tokenHandler: TokenHandler = tokenHandler
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
        socket.send(f"PASS oauth:{self.tokenHandler.tokens}")
        socket.send(f"NICK {self.tokenHandler.TwitchNick}")
        socket.send(f"JOIN #{self.tokenHandler.TwitchChannel}")
        socket.send(f"CAP REQ :twitch.tv/commands twitch.tv/tags")
    
    def sendMessage(self, socket, message):
        message = f"PRIVMSG #{self.tokenHandler.TwitchChannel} :{message}"
        socket.send(message)
        
    def dispatchCommand(self, message):
        if commandesFunctions.get(message["command"]):
            commandesFunctions[message["command"]](self.ws, message)
        else:
            print(f"Commande {message['command']} non reconnue")
    
    def onMessage(self, socket, message):
        messages = self.parser.parseMessages(message)
        for message in messages:
            self.dispatchCommand(message)
        # message_data = json.loads(message)
        # if "PING" in message_data.keys():
        #     # Répondre au PING pour éviter d'être déconnecté
        #     ws.send("PONG :tmi.twitch.tv")
        # elif "PRIVMSG" in message_data.keys():
        #     # Traitement des messages PRIVMSG (messages du chat)
        #     username = message_data["PRIVMSG"]["display-name"]
        #     message_content = message_data["PRIVMSG"]["message"]
        #     process_message(f"{username}: {message_content}")
        
    def onError(self, socket, error):
        print(f"Erreur dans la connexion au chat Twitch: {error}")
    
    
    def onClose(self):
        print("Connexion au chat Twitch fermée")