from werkzeug.serving import make_server
import threading
from werkzeug.routing import Map, Rule
from flask import Flask, jsonify, request
from flask_cors import CORS
from src.logger.logger import logger

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET", "POST"])
def token():
    import src.codeHandler
    
    logger.info("REQUEST GOT")
    code = request.args.get("code")
    
    if code:
        logger.info("CODE GOT")
        src.codeHandler.tokenGet = code
    
    with src.codeHandler.lock:
        src.codeHandler.tokenGet = code
        
    return "", 200
        

class ServerThread(threading.Thread):

    def __init__(self, app):
        threading.Thread.__init__(self)
        self.server = make_server('127.0.0.1', 3000, app, threaded=True)
        self.ctx = app.app_context()
        self.ctx.push()
        self.shutdown_event = threading.Event()

    def run(self):
        logger.debug("Starting server in a thread")
        self.server.serve_forever()

    def shutdown(self, hard=False):
        logger.debug("Shutting down server")
        self.server.shutdown()
        self.shutdown_event.set()
        
server = ServerThread(app)