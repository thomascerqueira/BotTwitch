from dotenv import load_dotenv
from src.tokenHandler import TokenHandler
from src.bot import Bot

load_dotenv()

if __name__ == "__main__":
    print("Lancement du bot")
    tokenHandler = TokenHandler()
    bot = Bot(tokenHandler)
