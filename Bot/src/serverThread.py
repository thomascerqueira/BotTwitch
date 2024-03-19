from werkzeug.serving import make_server
import threading
from werkzeug.routing import Map, Rule
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET", "POST"])
def token():
    import src.codeHandler
    
    print("REQUEST RECU")
    code = request.args.get("code")
    
    if code:
        print("CODE RECUPERE")
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
        print("Starting server in a thread")
        self.server.serve_forever()

    def shutdown(self, hard=False):
        print("Shutting down server")
        self.server.shutdown()
        self.shutdown_event.set()
        
server = ServerThread(app)