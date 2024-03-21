from src.twitchToken import TwitchToken
from src.logger.logger import logger

REPLAY_PARENT = "@reply-parent-msg-id"

logger_name = "CommandHandler"
logger.addLogger(logger_name)

class CommandHandler():
    def Pong(ws, _, **kwargs):
        """
        Send a pong message to the server
        
        Args:
            ws (websocket): The websocket to send the pong
        """
        logger.debug("Ping received, sending pong...", logger_name=logger_name)
        ws.send("PONG :tmi.twitch.tv")

    def replyWithUsername(ws, message, username):
        """
        Send a message to the chat with the username of the user
        
        Args:
            ws (websocket): The websocket to send the message
            message (str): The message to send
            username (str): The username to send the message to
        -------
        Returns:
            str: The message sent
        """
        ws.send(f"PRIVMSG #{TwitchToken.Channel} :@{username} {message}")
        return message

    def replyToMessage(ws, message, id):
        """
        Reply to a specific message
        
        Args:
            ws (websocket): The websocket to send the message
            message (str): The message to send
            id (str): The id of the message to reply to
        """
        ws.send(f"{REPLAY_PARENT}={id} PRIVMSG #{TwitchToken.Channel} :Bien recu !")

    def sendErrorMessage(ws):
        """
        Send an error message to the chat
        
        Args:
            ws (websocket): The websocket to send the message
        """
        CommandHandler.sendSimpleMessage(ws, f"Une erreur s'est produite, dis le à un modérateur !")
    
    def sendSimpleMessage(ws, message):
        ws.send(f"PRIVMSG #{TwitchToken.Channel} :{message}")
    
    def dispatchSpecialCommand(ws, command, message, **kwargs):
        """
        Dispatch and execute a special command
        
        Args:
            ws (websocket): The websocket to send the message
            command (str): The command to execute
            message (str): The message to execute
        """
        import src.command as Command
        username = kwargs.get("username", "unknown")
        user_id = kwargs.get("user_id", "no_user_id")
        
        if Command.specialCommand.get(command):
            logger.info(f"Executing special command {command} from {username}: {user_id}", logger_name=logger_name)
            try:
                output = Command.specialCommand[command].execute(ws, message, **kwargs)
                logger.debug(f"Output: {output}", logger_name=logger_name)
            except Exception as e:
                logger.error(f"An error append: {e}")
                CommandHandler.sendSimpleMessage(ws, "Une erreur s'est produite, dis le à un modérateur !", logger_name=logger_name)
        else:
            logger.warning(f"Command {command} not found from {username}: {user_id}", logger_name=logger_name)
    
    def Privmsg(ws, info, **kwargs):
        message = info["message"]
        id = info["id"]
        username = info["display-name"]
        badges = info["badges"]
        bot = kwargs.get("bot", None)
        user_id = info["user-id"]
        
        
        # print(f"Message reçu: {info['message']}")
        if (message.startswith(TwitchToken.Prefix)):
            specialCommand = message.split(" ")[0]

            logger.debug(info, logger_name=logger_name)

            CommandHandler.dispatchSpecialCommand(ws,
                                                  specialCommand,
                                                  message,
                                                  username=username,
                                                  osuToken=kwargs["osuToken"],
                                                  badges=badges,
                                                  bot=bot,
                                                  message_id=id,
                                                  user_id=user_id)
