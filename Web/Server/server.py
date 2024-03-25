from flask import Flask, jsonify, request
from flask_cors import CORS
import json
from checker.addCommand import AddCommandSchema
from marshmallow import ValidationError, Schema
from functools import wraps

class Command():    
    def __init__(self, command, description, file, data={}):
        self.command = command
        self.description = description
        self.file = file
        self.data = data
        
    def toDict(self):
        return {
            self.command: {
                "description": self.description,
                "file": self.file,
                "data": self.data
                }
            }
        
    @staticmethod
    def fromDict(data):
        print(data)

        return Command(
            command=data["command"] if data["command"].startswith("!") else f"!{data['command']}",
            description=data["description"],
            file=data["file"],
            data=data.get("data", {})
            )
        
    def __str__(self):
        return f"Command: {self.command}, Description: {self.description}, File: {self.file}, Data: {self.data}"
        
    def __repr__(self):
        return self.__str__()

def validate_schema(SchemaValidator: Schema):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kw):
            try:
               SchemaValidator().load(request.get_json())
            except ValidationError as e:
                return jsonify({"error": e.messages}), 400
            return f(*args, **kw)
        return wrapper
    return decorator

class Server():
    def __init__(self, file_command, port=5000):
        self.app = Flask(__name__)
        CORS(self.app)
        
        self.port = port
        self.file_command = file_command
        
        self.app.route("/", methods=["GET"])(self.index)
        self.app.route("/commands", methods=["GET"])(self.getAllCommands)
        self.app.route("/commands/<command>", methods=["POST"])(self.addCommand)
        self.app.route("/commands/<command>", methods=["PATCH"])(self.updateCommand)
        self.app.route("/commands/<command>", methods=["DELETE"])(self.deleteCommand)
        
    def index(self):
        return jsonify({
            "message": "Hello World!"
            })
        
    def getAllCommands(self):
        commands = {}
        
        with open(self.file_command, "r") as f:
            commands = json.load(f)
            
        return jsonify(commands)
    
    @validate_schema(AddCommandSchema)
    def addCommand(self, command):
        requestBody = request.get_json()
        
        with open(self.file_command, "r") as f:
            commands = json.load(f)

        command = f"!{command}" if not command.startswith("!") else command
        if command in commands:
            return jsonify({"error": "Command already exists"}), 400
        
        newCommand = Command.fromDict(
            {
                "command": command,
                **requestBody
            }
        )
        commands.update(newCommand.toDict())
        
        with open(self.file_command, "w") as f:
            json.dump(commands, f, indent=4)

        return "", 200
    
    def updateCommand(self, command):
        requestBody = request.get_json()
        
        with open(self.file_command, "r") as f:
            commands = json.load(f)
        
        command = f"!{command}" if not command.startswith("!") else command

        if command not in commands:
            return jsonify({"error": "Command does not exists"}), 400
        
        oldCommand = commands[command]
        newValus = {
            **oldCommand,
            **requestBody
        } 
        newCommand = Command.fromDict(
            {
                "command": command,
                **newValus
            }
        )
        commands.update(newCommand.toDict())
        
        with open(self.file_command, "w") as f:
            json.dump(commands, f, indent=4)

        return "", 200
    
    def deleteCommand(self, command):
        with open(self.file_command, "r") as f:
            commands = json.load(f)
        
        command = f"!{command}" if not command.startswith("!") else command

        if command not in commands:
            return jsonify({"error": "Command does not exists"}), 400
        
        del commands[command]
        
        with open(self.file_command, "w") as f:
            json.dump(commands, f, indent=4)

        return "", 200
    
    def run(self):
        self.app.run(port=self.port)