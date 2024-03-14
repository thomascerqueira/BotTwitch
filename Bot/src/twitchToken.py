from src.tokenHandler import TokenHandler
import os

class TwitchToken(TokenHandler):
    Nick = ""
    Channel = ""
    Prefix = ""
    
    envNeeded = ["CLIENT_ID", "CLIENT_SECRET", "TWITCH_NICK", "TWITCH_CHANNEL", "BOT_PREFIX"]
    
    def __init__(self):
        for env in TwitchToken.envNeeded:
            if not os.getenv(env):
                print(f"Environment variable {env} is missing")
                exit(-1)
        
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