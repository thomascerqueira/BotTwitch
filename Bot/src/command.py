
from src.commands.commandHandler import CommandHandler
from src.commands.printHelp import PrintHelp
from src.commands.osuRank import OsuRank
       
specialCommand = {
    "!help": PrintHelp(),
    "!osu": OsuRank()
}
    
commandesFunctions = {
    "PING": CommandHandler.Pong,
    "PRIVMSG": CommandHandler.Privmsg
}