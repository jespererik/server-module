#!/usr/bin/env python
from flask  import Flask, request, jsonify
from ast    import literal_eval
import server as Server
import json

app = Flask(__name__)


'''
Add function to check authentication(HMAC, pre-shared key etc.) 
'''

#Post/Get routes
@app.route('/init', methods=['GET', 'POST'])
def process_node_init():
    content = request.json
    init_packet = Server.node_init_packet_handler(content)
    return jsonify(init_packet)


#Post routes
@app.route('/Temp', methods=['POST'])
def process_reading_post():
    content = request.json
    node_data = Server.node_data_packet_handler(content)
    return jsonify(node_data), 201


#Get routes
@app.route('/readings/<string:reading_type>', methods = ['GET'])
def get_readings_type(reading_type):
    content = Server.get_type_readings(reading_type)
    return json.dumps(content)

'''
need to fix routes here

app.route('/node/<string:node_location>', methods = ['GET'])
def get_location_node(node_location):
    content = Server.get_location_nodes(node_location)
    return json.dumps(content)

@app.route('/reading/<string:node_location>', methods = ['GET'])
def get_readings_location(node_location):
    content = Server.get_location_readings(node_location)
    return json.dumps(content)


@app.route("/sensors/<string:node_name>", methods = ['GET'])
def get_sensors_node(node_name):
    content = Server.get_node_sensors(node_name)
    return json.dumps(content)


@app.route('/sensors/<string:node_location>', methods = ['GET'])
def get_sensors_location(node_location):
    content = Server.get_location_sensors(node_location)
    return json.dumps(content)
'''

def main():
    Server.init_database()
    app.run(debug = True, host = '0.0.0.0', port = 5000)


if __name__ == '__main__':
    main()
