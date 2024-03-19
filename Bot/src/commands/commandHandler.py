from src.twitchToken import TwitchToken

REPLAY_PARENT = "@reply-parent-msg-id"

class CommandHandler():
    def Pong(ws, _, **kwargs):
        print("Ping received, sending pong...")
        ws.send("PONG :tmi.twitch.tv")

    def replyWithUsername(ws, message, username):
         ws.send(f"PRIVMSG #{TwitchToken.Channel} :@{username} {message}")

    def replyToMessage(ws, message, id):
        ws.send(f"{REPLAY_PARENT}={id} PRIVMSG #{TwitchToken.Channel} :Bien recu !")

    def sendErrorMessage(ws):
        CommandHandler.sendSimpleMessage(ws, f"Une erreur s'est produite, dis le à un modérateur !")
    
    def sendSimpleMessage(ws, message):
        ws.send(f"PRIVMSG #{TwitchToken.Channel} :{message}")
    
    def dispatchSpecialCommand(ws, command, message, **kwargs):
        import src.command as Command
        
        if Command.specialCommand.get(command):
            try:
                Command.specialCommand[command].execute(ws, message, **kwargs)
            except Exception as e:
                print(f"Une erreur s'est produite: {e}")
                CommandHandler.sendSimpleMessage(ws, "Une erreur s'est produite, dis le à un modérateur !")
    
    def Privmsg(ws, info, **kwargs):
        message = info["message"]
        id = info["id"]
        username = info["display-name"]
        badges = info["badges"]
        bot = kwargs.get("bot", None)
        
        print(f"Message reçu: {info['message']}")
        if (message.startswith(TwitchToken.Prefix)):
            specialCommand = message.split(" ")[0]

            CommandHandler.dispatchSpecialCommand(ws,
                                                  specialCommand,
                                                  message,
                                                  username=username,
                                                  osuToken=kwargs["osuToken"],
                                                  badges=badges,
                                                  bot=bot)
