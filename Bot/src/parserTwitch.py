from src.logger.logger import logger

class ParserTwitch():
    def __init__(self):
        pass
    
    def createDictionnaryFromInfo(self, info):
        dictionnary = {}
        for i in info:
            if i == "":
                continue
            key, value = i.split("=")
            dictionnary[key] = value
        
        return dictionnary
    
    def parse(self, message):
        # print(f"Message avant de split {message}")
        if message.startswith("PING"):
            logger.warning("PING received from Twitch, awaiting PONG...")
            result = {"command": "PING"}
            return result
        
        messages = message.strip().split(":")
        # print("Messages splités: ")
        result = {}
        # for m in messages:
            # print(f"\t{m}")
        
        if messages[0].startswith('@'):
            infos = messages[0].split(";")
            infosDictionnary = self.createDictionnaryFromInfo(infos)
            # print("\tInfos from dictionnary: ")
            # for k, v in infosDictionnary.items():
                # print(f"\t\t{k}: {v}")
            
            command = messages[1].split(" ")[1]
            # print(f"\t\tCommande: {command}")
            result = {**infosDictionnary, **{"command": command}}
        else:
            messages = messages[1:]
            splited = messages[0].split(" ")
            
            if len(splited) > 1:
                command = splited[1]
            else:
                command = splited[0]
            # print(f"\t\tCommande: {command}")
            
            result["command"] = command
        
        if command == "PRIVMSG":
            result["message"] = messages[2]
            
        return result
    
    def parseMessages(self, message):
        messages = message.split("\r\n")
        
        result = []
        for _message in messages:
            if (_message == ""):
                continue
            result.append(self.parse(_message))
        return result