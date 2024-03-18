
from src.commands.commandHandler import CommandHandler
from src.commands.printHelp import PrintHelp
from src.commands.osuRank import OsuRank
from src.commands.reloadCommands import ReloadCommand
       
specialCommand = {
    "!help": PrintHelp(),
    "!reload": ReloadCommand()
}
    
commandesFunctions = {
    "PING": CommandHandler.Pong,
    "PRIVMSG": CommandHandler.Privmsg
}