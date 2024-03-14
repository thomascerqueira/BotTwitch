from src.commands.specialCommand import SpecialCommand
from src.twitchToken import TwitchToken

class PrintHelp(SpecialCommand):
    def __init__(self):
        pass
    
    def help(self):
        return "!help: Affiche l'aide"
    
    def execute(self, ws, message, **kwargs):
        import src.command as Command
        from src.commands.commandHandler import CommandHandler
        
        print(f"Execiuting prtin help")
        
        splitted = message.split(" ")
        commands = ", ".join(list(Command.specialCommand.keys()))
        
        if len(splitted) == 1:
            CommandHandler.replyWithUsername(ws, f"Commands disponibles: {commands}", kwargs["username"])
            return

        commandToHelp = message.split(" ")[1]
        commandToHelp = commandToHelp if commandToHelp.startswith(TwitchToken.Prefix) else TwitchToken.Prefix + commandToHelp

        if commandToHelp and commandToHelp in Command.specialCommand:
            CommandHandler.replyWithUsername(ws, Command.specialCommand[commandToHelp].help(), kwargs["username"])
        else:
            CommandHandler.replyWithUsername(ws, f"Commands disponibles: {commands}", kwargs["username"])
