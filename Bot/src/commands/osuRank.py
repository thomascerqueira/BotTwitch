from src.commands.specialCommand import SpecialCommand
from src.twitchToken import TwitchToken
from requests import Response

class OsuRank(SpecialCommand):
    def __init__(self, **kwargs):
        pass
    
    def help(self):
        return "Affiche le rank osu de ton streamer"
    
    def execute(self, ws, message, **kwargs):
        from src.commands.commandHandler import CommandHandler
        
        if kwargs["osuToken"]:
            info: Response = kwargs["osuToken"].getRank()

            if info.status_code != 200:
                CommandHandler.sendErrorMessage(ws)
            else:
                data = info.json()
                country = data.get("country").get('name')
                statistics = data.get("statistics")

                rank = {
                    "global": statistics.get("global_rank"),
                    "country": statistics.get("country_rank"),
                }
                answer = f"Le rank de {TwitchToken.Channel} est {rank.get('global')} global et {rank.get('country')} en {country}"
                return CommandHandler.replyWithUsername(ws, f"{answer}", kwargs["username"])
