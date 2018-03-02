#!/usr/bin/env python
from flask  import Flask, request, jsonify
from ast    import literal_eval
import DBHelper
import server as Server
import json

app = Flask(__name__)


'''
Add function to check authentication(HMAC, pre-shared key etc.) 
'''
@app.route('/init', methods=['GET', 'POST'])
def process_node_init():
    content = request.json
    init_packet = Server.node_init_packet_handler(content)
    return jsonify(init_packet)


@app.route('/Temp', methods=['POST'])
def process_reading_post():
    content = request.json
    node_data = Server.node_data_packet_handler(content)
    return jsonify(node_data), 201


@app.route('/GET/reading/<reading_type>')
def process_reading_get(reading_type):
    pass
    

def main():
    Server.init_database()
    app.run(debug = True)


if __name__ == '__main__':
    main()
