#!/usr/bin/env python
from flask  import Flask, request, jsonify
from ast    import literal_eval
import DBHelper
import Server
import json

app = Flask(__name__)


'''
Add function to check authentication(HMAC, pre-shared key etc.) 
'''
@app.route('/init', methods=['GET', 'POST'])
def nodeInit():
    content = request.json
    Server.node_init_packet_handler(content)
    return jsonify(content)

@app.route('/Temp', methods=['POST'])
def nodeTemp():
    content = request.json
    node_data = Server.node_data_packet_handler(content)
    return jsonify(node_data), 201


def main():
    Server.init_database()
    app.run(debug = True)


if __name__ == '__main__':
    main()
