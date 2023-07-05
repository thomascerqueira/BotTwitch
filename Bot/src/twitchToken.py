from src.tokenHandler import TokenHandler
import os

class TwitchToken(TokenHandler):
    Nick = ""
    Channel = ""
    Prefix = ""
    
    def __init__(self):
        super().__init__(
            "https://id.twitch.tv/oauth2/token",
            "https://id.twitch.tv/oauth2/authorize", 
            "channel:moderate+chat:edit+chat:read",
            os.getenv("CLIENT_ID"),
            os.getenv("CLIENT_SECRET"),
            "http://localhost:3000",
            "twitch"
            )
        TwitchToken.Nick = os.getenv("TWITCH_NICK")
        TwitchToken.Channel = os.getenv("TWITCH_CHANNEL")
        TwitchToken.Prefix = os.getenv("BOT_PREFIX")