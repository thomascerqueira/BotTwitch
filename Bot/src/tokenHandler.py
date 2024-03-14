import os
import requests
import webbrowser

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

        self.getToken()
    
    def getCode(self):
        url = f"{self.url_authorize}?client_id={self.client_id}&redirect_uri={self.redirect_uri}&response_type=code&scope={self.scope}"

        webbrowser.open(url)
        self.authorization_code = input(f"Enter the code for {self.name}: ")
        
    def refreshToken(self):
        params = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }
        r = requests.post(self.url_token, data=params)
        
        if (r.status_code != 200):
                print(f"Error while refreshing {self.name} token")
                print(r.status_code)
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
            print("Refresh token loaded")
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
                print(f"Error while getting {self.name} token you can find information in the file {self.name}_token_error.txt\nExiting...")
                with open(f"{self.name}_token_error.txt", "w") as f:
                    f.write(r.text)
                print(r.status_code)
                exit(-1)
            self.refresh_token = r.json()["refresh_token"]
            self.tokens = r.json()['access_token']
            self.saveRefreshToken()