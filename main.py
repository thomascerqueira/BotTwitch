from dotenv import load_dotenv
from src.twitchToken import TwitchToken
from src.bot import Bot
import argparse

load_dotenv()

if __name__ == "__main__":
    
    # argument
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--osu", help="Username to use to connect to osu, if not provided the bot will not use Osu Api", dest="osu")
    parser.add_argument("-i", "--id", help="If the bot have to use osu api, this option is to use an id instead of the username", dest="osuId", action="store_true")
    args = parser.parse_args()
    
    print("Lancement du bot")
    twitchToken = TwitchToken()
    osuToken = None
    
    osuUsername = args.osu
    
    if osuUsername:
        if osuUsername == "":
            print("The osu username is missing")
            exit(-1)
        from src.osuToken import OsuToken
        osuToken = OsuToken(osuUsername, args.osuId)
    bot = Bot(twitchToken, osuToken=osuToken)
