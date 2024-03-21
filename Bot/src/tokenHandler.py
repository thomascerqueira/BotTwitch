import os
import requests
import webbrowser
from time import sleep

from src.logger.logger import logger

class TokenHandler:
    def __init__(self, url_token, url_authorize, scope, client_id, client_secret, redirect_uri, name):
        self.url_token = url_token
        self.url_authorize = url_authorize
        self.authorization_code = ""
        self.scope = scope
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.name = name
        self.tokens = ""
        self.refresh_token = ""
        self.maxTry = 120
    
    def getCode(self):
        import src.codeHandler
        url = f"{self.url_authorize}?client_id={self.client_id}&redirect_uri={self.redirect_uri}&response_type=code&scope={self.scope}"

        webbrowser.open(url)
        
        nbTry = 0
        while nbTry < self.maxTry:
            with src.codeHandler.lock:
                self.authorization_code = src.codeHandler.tokenGet
            if self.authorization_code:
                with src.codeHandler.lock:
                    src.codeHandler.tokenGet = ""
                return
            nbTry += 1
            sleep(1)
        
        if nbTry == self.maxTry:
            raise Exception(f"Error while getting {self.name} code")
            
        
    def refreshToken(self):
        params = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }
        r = requests.post(self.url_token, data=params)
        
        if (r.status_code != 200):
                logger.error(f"Error while refreshing {self.name} token")
                logger.error(f"Error: {r.status_code} {r.text}")
                exit(-1)
        self.refresh_token = r.json()["refresh_token"]
        self.tokens = r.json()['access_token']
        self.saveRefreshToken()
        
    def saveRefreshToken(self):
        if not os.path.isdir("tokens"):
            os.mkdir("tokens")
        
        with open(f"tokens/{self.name}_token.txt", "w") as f:
            f.write(self.refresh_token)
            
    def loadRefreshToken(self):
        if not os.path.isfile(f"tokens/{self.name}_token.txt"):
            return False
        
        with open(f"tokens/{self.name}_token.txt", "r") as f:
            self.refresh_token = f.read()
            return True

    def getToken(self):
        if (self.loadRefreshToken()):
            logger.info(f"Loading {self.name} token from file")
            self.refreshToken()
        else:
            self.getCode()
            params = {
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "grant_type": "authorization_code",
                "redirect_uri": self.redirect_uri,
                "code": self.authorization_code
            }
            r = requests.post(self.url_token, data=params)
            
            if (r.status_code != 200):
                logger.error(f"Error while getting {self.name} token you can find information in the file {self.name}_token_error.txt\nExiting...")
                with open(f"{self.name}_token_error.txt", "w") as f:
                    f.write(r.text)
                logger.error(r.status_code)
                exit(-1)
            self.refresh_token = r.json()["refresh_token"]
            self.tokens = r.json()['access_token']
            self.saveRefreshToken()