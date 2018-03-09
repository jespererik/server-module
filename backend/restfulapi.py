#!/usr/bin/env python
from flask  import Flask, request, jsonify
from ast    import literal_eval
import server
import json

app = Flask(__name__)


'''
Add function to check authentication(HMAC, pre-shared key etc.) 
'''

#Create node
@app.route('/api/nodes', methods=['POST'])
def create_node():
    content = request.json
    response =  server.create_node(content)
    return jsonify(response), 201

#Create sensor
@app.route('/api/nodes/<string:node_name>/sensors', methods=['POST'])
def create_sensor(node_name):
    content = request.json
    response = server.create_sensor(content, node_name)
    return jsonify(response), 201

#Create reading
@app.route('/api/nodes/<string:node_name>/sensors/<string:sensor_name>/readings', methods=['POST'])
def process_reading_post(node_name, sensor_name):
    content = request.json
    response = server.create_reading(content, node_name, sensor_name)
    return jsonify(response), 201


#Get routes
@app.route('/readings/<string:reading_type>', methods = ['GET'])
def get_readings_type(reading_type):
    content = server.get_type_readings(reading_type)
    return json.dumps(content)


def main():
    server.init_database()
    app.run(debug = True, host = '0.0.0.0', port = 5000)


if __name__ == '__main__':
    main()
