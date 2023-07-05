from flask import Flask, jsonify, request
from flask_cors import CORS
import copy
from functions import printToChat

app = Flask(__name__)
CORS(app)

functions = {
    "print": {
        "function": printToChat,
        "args": {
            "value": "Value to print to the chat"
        },
        "description": "Prints a value to the chat"
    }  
}

commands = {
    "mdr": {
        "function": "print",
        "args": {
            "value": "mdr",
            "test": "test"
        },
        "description": "Prints 'mdr' in the chat"
    },
    "haha": {
        "function": "print",
        "args": {
            "value": "mdr",
            "test": "test"
        },
        "description": "Prints 'mdr' in the chat"
    }
}

def remove_function_key(dictionary):
    dictionary_copy = copy.deepcopy(dictionary)
    
    for key in dictionary.keys():
        dictionary_copy[key].pop("function")
    return dictionary_copy

@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "message": "Hello World!"
        })

@app.route("/command", methods=["GET"])
def getAllCommands():
    return jsonify({
        "commands": commands
        })

@app.route("/functions", methods=["GET"])
def getAllFunctions():
    return jsonify({
        "functions": remove_function_key(functions)
        })

if __name__ == "__main__":
    app.run(debug=True)