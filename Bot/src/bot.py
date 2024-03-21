from src.twitchToken import TwitchToken
from src.osuToken import OsuToken
from src.parserTwitch import ParserTwitch
import os
import websocket

from src.logger.logger import logger

class Bot():
    def __init__(self, twitchToken: TwitchToken, fileCommand, osuToken: OsuToken = None):
        logger.info("Initializing bot")
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
        logger.info("Bot initialized")

    def connectToTwitch(self):
        logger.info("Connecting to the Twitch chat...")
        self.ws = websocket.WebSocketApp(self.url,
                                    on_message=self.onMessage,
                                    on_error=self.onError,
                                    on_close=self.onClose)
        self.ws.on_open = self.onOpen
    
    def run(self):
        logger.info("Running the bot")
        self.ws.run_forever()
    
    def onOpen(self, socket):
        logger.info("Connexion to the Twitch chat opened")
        socket.send(f"PASS oauth:{self.twitchToken.tokens}")
        socket.send(f"NICK {self.twitchToken.Nick}")
        socket.send(f"JOIN #{self.twitchToken.Channel}")
        socket.send(f"CAP REQ :twitch.tv/commands twitch.tv/tags")
    
    def sendMessage(self, socket, message):
        logger.debug(f"Sending message: {message}")
        message = f"PRIVMSG #{self.twitchToken.Channel} :{message}"
        socket.send(message)
        
    def dispatchCommand(self, message):
        import src.command
        
        if src.command.commandesFunctions.get(message["command"]):
            src.command.commandesFunctions[message["command"]](self.ws, message, osuToken=self.osuToken, bot=self)
        else:
            logger.error(f"Command {message['command']} not found")
    
    def onMessage(self, socket, message):
        messages = self.parser.parseMessages(message)
        for message in messages:
            self.dispatchCommand(message)
        
    def onError(self, socket, error):
        logger.error(f"Error in chat Twitch: {error}")

    
    def onClose(self, socket, close_status_code, close_msg):
        logger.warning(f"Connexion to the Twitch chat closed: {close_status_code} {close_msg}")
        
    def loadCommandFromFile(self):
        import json
        import src.command
        import src.utils.commandsHelper as commandsHelper
        
        logger.info(f"Loading command from file {self.fileCommand}")
        
        if not self.fileCommand:
            logger.error("No file command to load")
            return
        
        with open(self.fileCommand, "r") as file:
            data = json.load(file)
            
            for command in data:
                if command in src.command.specialCommand:
                    logger.debug(f"Command {command} already loaded")
                    continue
                
                logger.debug(f"Loading command {command}")
                value = data[command]
                
                module = commandsHelper.module_load(value["file"])
                classModule = commandsHelper.getClassFromModule(module)
                dataAdded = value.get("data", {})
                src.command.specialCommand[command] = classModule(**dataAdded)
                
                logger.debug(f"Command {command} loaded")
                
    def reloadCommand(self):
        import src.command
        
        keysToDelete = [key for key in src.command.specialCommand.keys() if key not in self.baseCommands]
        
        for key in keysToDelete:
            del src.command.specialCommand[key]
                
        self.loadCommandFromFile()
