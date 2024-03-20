from src.commands.specialCommand import SpecialCommand
from src.twitchToken import TwitchToken

class PrintHelp(SpecialCommand):
    def __init__(self, **kwargs):
        pass
    
    def help(self):
        return "!help: Affiche l'aide"
    
    def execute(self, ws, message, **kwargs):
        import src.command as Command
        from src.commands.commandHandler import CommandHandler
        
        splitted = message.split(" ")
        keys = list(Command.specialCommand.keys())
        keys.remove("!reload")

        commands = ", ".join(keys)
        output = ""
        
        if len(splitted) == 1:
            output = f"Commands disponibles: {commands}"
            CommandHandler.replyWithUsername(ws, output, kwargs["username"])
            return output

        commandToHelp = message.split(" ")[1]
        commandToHelp = commandToHelp if commandToHelp.startswith(TwitchToken.Prefix) else TwitchToken.Prefix + commandToHelp

        if commandToHelp and commandToHelp in Command.specialCommand:
            output = Command.specialCommand[commandToHelp].help()
            CommandHandler.replyWithUsername(ws, output, kwargs["username"])
        else:
            CommandHandler.replyWithUsername(ws, output, kwargs["username"])
        return output
