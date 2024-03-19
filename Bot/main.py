from dotenv import load_dotenv
from src.twitchToken import TwitchToken
from src.bot import Bot
import argparse
from src.serverThread import server
from time import sleep

load_dotenv()

if __name__ == "__main__":
    
    # argument
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--osu", help="Username to use to connect to osu, if not provided the bot will not use Osu Api", dest="osu")
    parser.add_argument("-i", "--id", help="If the bot have to use osu api, this option is to use an id instead of the username", dest="osuId", action="store_true")
    parser.add_argument("-f", "--file", help="File of command to load", dest="commandFile", required=True)
    
    args = parser.parse_args()
    
    server.start()
    print("Lancement du bot")
    twitchToken = TwitchToken()
    error = []
    
    try:
        twitchToken.getToken()
    except Exception as e:
        error.append(e)
    
    print("Token Twitch récupéré")
    osuToken = None
    osuUsername = args.osu

    if osuUsername:
        if osuUsername == "":
            print("The osu username is missing")
            exit(-1)
        actualToken = "osu"
        from src.osuToken import OsuToken
        osuToken = OsuToken(osuUsername, args.osuId)
        
        sleep(1)
        try:
            osuToken.getToken()
        except Exception as e:
            print(type(e))
            error.append(e)
    
    if len(error) > 0:
        for e in error:
            print(e)
            
        server.shutdown()
        server.join()
        exit(-1)
        
    
    bot = Bot(twitchToken, osuToken=osuToken, fileCommand=args.commandFile)
    
    print("Bot initialisé")
    print("Shutting down the server that was used to get the token")
    server.shutdown()
    
    bot.run()