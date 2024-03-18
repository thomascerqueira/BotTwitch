from src.twitchToken import TwitchToken
from src.osuToken import OsuToken
from src.parserTwitch import ParserTwitch
import os
import websocket

class Bot():
    def __init__(self, twitchToken: TwitchToken, fileCommand, osuToken: OsuToken = None):
        print("Initialisation du bot")
        self.twitchToken: TwitchToken = twitchToken
        self.osuToken: OsuToken = osuToken
        self.parser: ParserTwitch = ParserTwitch()
        self.prefixe = os.getenv("PREFIXE")
        self.ws = None
        self.url = f"wss://irc-ws.chat.twitch.tv:443"
        self.fileCommand = fileCommand
        
        self.baseCommands = ["!reload", "!help"]
        
        self.loadCommandFromFile()
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
        print(f"Envoi du message: {message}")
        message = f"PRIVMSG #{self.twitchToken.Channel} :{message}"
        socket.send(message)
        
    def dispatchCommand(self, message):
        import src.command
        
        if src.command.commandesFunctions.get(message["command"]):
            src.command.commandesFunctions[message["command"]](self.ws, message, osuToken=self.osuToken, bot=self)
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
        
    def loadCommandFromFile(self):
        import json
        import src.command
        import src.utils.commandsHelper as commandsHelper
        
        if not self.fileCommand:
            print("Aucun fichier de commande à charger")
            return
        
        with open(self.fileCommand, "r") as file:
            data = json.load(file)
            
            for command in data:
                if command in src.command.specialCommand:
                    print(f"La commande {command} est déjà chargée")
                    continue
                
                print(f"Chargement de la commande {command}")
                value = data[command]
                
                module = commandsHelper.module_load(value["file"])
                classModule = commandsHelper.getClassFromModule(module)
                dataAdded = value.get("data", {})
                src.command.specialCommand[command] = classModule(**dataAdded)
                
                print(f"Chargement de la commande {command} réussi")
                
    def reloadCommand(self):
        import src.command
        
        keysToDelete = [key for key in src.command.specialCommand.keys() if key not in self.baseCommands]
        
        for key in keysToDelete:
            del src.command.specialCommand[key]
                
        self.loadCommandFromFile()
