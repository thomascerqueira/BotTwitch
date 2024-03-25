# BotTwitch
Simple bot twitch made in python

You will find 3 modules in this project:
- Bot
- Web
- Server


## Bot twitch

This is a bot that can be used in twitch chat. It is a simple bot that can be used to run commands in the chat.

All the commands that the bot knows are in the `Bot/src/commands` directory. You can add, remove or patch commands by adding a file in this directory and adding in the `command.json` file or by using the combo web-ui/server.

You can add commands by adding a python script in the `Bot/src/commands` directory with the following structure:

```python
from Bot.src.commands.command import Command

class MyCommand(Command):
    def __init__(self, **kwargs):
        pass
    
    def help(self):
        return "This is a help message"
    
    def execute(self, ws, message, **kwargs):
        ws.send_message("Hello world")
```

Then add it to the `command.json` file:

```json
{
    ...,
     "!<commandName>": {
        "description": "This is a description",
        "file": "<Where The python script is located>"
    }
}
```

If your script need additional data you can provide it in the `command.json` file:

```json
{
    ...,
     "!<commandName>": {
        "description": "This is a description",
        "file": "<Where The python script is located>",
        "data": {
            .....
        }
    }
}
```

A good example will be in the file `Bot/src/commands/print.py`.

**/!\ A file is not linked to a command, you can add different command for the same file**

If you add a command from the Web-UI and the server you need to make sure that your script is in the `Bot/src/commands` directory otherwise it will not work.


You have two basic commands in the bot:
- `!help` : Display all the commands that the bot knows
- `!osu` : If you logged your osu account then the bot will display your osu profile