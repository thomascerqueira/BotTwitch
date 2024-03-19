import os
from src.tokenHandler import TokenHandler
import requests

class OsuToken(TokenHandler):
    Secret = ""
    Id = ""
    
    envNeeded = ["OSU_CLIENT_ID", "OSU_CLIENT_SECRET"]
    
    def __init__(self, username, id=False):
        for env in OsuToken.envNeeded:
            if not os.getenv(env):
                print(f"Environment variable {env} is missing")
                exit(-1)
        
        super().__init__(
            "https://osu.ppy.sh/oauth/token",
            "https://osu.ppy.sh/oauth/authorize",
            "public+identify",
            os.getenv("OSU_CLIENT_ID"),
            os.getenv("OSU_CLIENT_SECRET"),
            "http://localhost:3000",
            "osu"
            )

        self.username = username
        self.endpointData = f"https://osu.ppy.sh/api/v2/users/{username}"
        self.useId = id
        
    def makeRequest(self, type, url, headers={}, params={}, data={}):
        headers = {
            **headers,
            "Authorization": f"Bearer {self.tokens}",
            "content-type": "application/json",
            "accept": "application/json",
        }
        
        r = requests.request(
            type,
            url=url,
            params=params,
            headers=headers,
            data=data
            )
        
        if (r.status_code == 401):
            return self.makeRequest(type, url, headers, params, data)
        
        if (r.status_code != 200):
            print(r.text)
        return r

        
    def getRank(self) -> requests.Response:
        params = {
            "key": "id" if self.useId else "username",
        }
        
        r = self.makeRequest("GET", self.endpointData, params=params)
        
        return r
        