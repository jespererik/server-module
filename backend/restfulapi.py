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
@app.route('reading/<reading_type>', methods = ['GET'])
def process_reading_get(reading_type):
    pass

@app.route("/sensors/<sensor_name>", methods = ['GET'])
def getSensors(sensor_name):
    Server.get_connected_sensors(sensor_name)

@app.route("/redings/<node_location>/", methods = ['GET'])
def readings_by_location():
    return json.dumps(Server.get_readings_by_location(node_location))

@app.route("/readings/<reading_type>/<node_location>", methods = ['GET'])
def readings_by_type_and_location(node_location, reading_type):
    return json.dumps(Server.get_readings_by_location_and_type(node_location, reading_type))

@app.route("/readings/<reading_type>/", methods = ['GET'])
def readings_by_type(reading_type):
    return json.dumps(Server.get_readings_by_type(reading_type))

    
def main():
    Server.init_database()
    app.run(debug = True, host = '0.0.0.0', port = 5000)


if __name__ == '__main__':
    main()
