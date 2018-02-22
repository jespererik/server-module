from flask import Flask, request, jsonify
from Server_Debug_functions import *

import Server
import sys

app = Flask(__name__)

@app.route('/init', methods=['GET', 'POST'])
def nodeInit():
    content = request.json
    DebugPrint('dict', 'content', content)
    if content['NODE_ID'] == '': 
        content['NODE_ID'] = Server.getNodeID()
    DebugPrint('dict', 'content', content)
    return jsonify(content)

def runServerREST():
    app.run(port = 6105)

if __name__ == '__main__':
    app.run(debug = True)
