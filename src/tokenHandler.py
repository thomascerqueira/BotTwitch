import os
import requests
import webbrowser

class TokenHandler:
    TwitchNick = ""
    TwitchChannel = ""
    Prefix = ""
    
    def __init__(self):
        self.url_token = "https://id.twitch.tv/oauth2/token"
        self.url_authorize = "https://id.twitch.tv/oauth2/authorize"
        self.authorization_code = ""
        self.scope = "channel:moderate+chat:edit+chat:read"
        self.client_id = os.getenv("CLIENT_ID")
        self.client_secret = os.getenv("CLIENT_SECRET")
        TokenHandler.TwitchNick = os.getenv("TWITCH_NICK")
        TokenHandler.TwitchChannel = os.getenv("TWITCH_CHANNEL")
        TokenHandler.Prefix = os.getenv("BOT_PREFIX")

        self.tokens = ""
        self.refresh_token = ""
        self.getToken()
    
    def getCode(self):
        url = f"https://id.twitch.tv/oauth2/authorize?client_id={self.client_id}&redirect_uri=http://localhost:3000&response_type=code&scope={self.scope}"

        webbrowser.open(url)
        self.authorization_code = input("Enter the code: ")
        print(self.authorization_code)
        
    def refreshToken(self):
        params = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }
        r = requests.post(self.url_token, params=params)
        self.refresh_token = r.json()["refresh_token"]
        self.tokens = r.json()['access_token']
        self.saveRefreshToken()
        
    def saveRefreshToken(self):
        with open("refresh_token.txt", "w") as f:
            f.write(self.refresh_token)
            
    def loadRefreshToken(self):
        if not os.path.isfile("refresh_token.txt"):
            return False
        
        with open("refresh_token.txt", "r") as f:
            self.refresh_token = f.read()
            return True

    def getToken(self):
        if (self.loadRefreshToken()):
            print("Refresh token loaded")
            self.refreshToken()
        else:
            self.getCode()
            params = {
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "grant_type": "authorization_code",
                "redirect_uri": "http://localhost:3000",
                "code": self.authorization_code
            }
            r = requests.post(self.url_token, params=params)
            self.refresh_token = r.json()["refresh_token"]
            self.tokens = r.json()['access_token']
            self.saveRefreshToken()