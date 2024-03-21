from src.commands.specialCommand import SpecialCommand
from src.twitchToken import TwitchToken
from src.logger.logger import logger

class ReloadCommand(SpecialCommand):
    def __init__(self, **kwargs):
        pass
    
    def help(self):
        return "!help: Affiche l'aide"
    
    def execute(self, ws, message, **kwargs):
        import src.command as Command
        from src.commands.commandHandler import CommandHandler
        import src.bot
        
        bot: src.bot.Bot = kwargs.get("bot", None)
        
        if not bot:
            logger.error("Bot not found")
            return
        
        badges = kwargs.get("badges", "")
        
        if isinstance(badges, list):
            badges = ",".join(badges)
        
        if "broadcaster" in badges:
            bot.reloadCommand()
            return "Command reloaded"
        return "Not allowed to do that"