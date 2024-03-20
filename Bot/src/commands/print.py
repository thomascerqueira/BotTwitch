from src.commands.specialCommand import SpecialCommand


class Print(SpecialCommand):
    def __init__(self, **kwargs):
        self.messageToPrint = kwargs.get("message", "")
        self.commandTrigger = kwargs.get("commandTrigger", "")
        self.helpMessage = kwargs.get("helpMessage", "")

    def help(self):
        return f"{self.commandTrigger}: {self.helpMessage}"
    
    def execute(self, ws, message, **kwargs):
        from src.commands.commandHandler import CommandHandler
        
        CommandHandler.replyWithUsername(ws, self.messageToPrint, kwargs["username"])
        return self.messageToPrint