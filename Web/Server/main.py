from flask import Flask, jsonify, request
from flask_cors import CORS
import copy
from functions import printToChat
import argparse
from server import Server

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Web server for the bot")
    
    parser.add_argument("-f", "--file", type=str, help="Path to the commands file", required=True)
    args = parser.parse_args()

    server = Server(args.file, port=4500)
    server.run()
    