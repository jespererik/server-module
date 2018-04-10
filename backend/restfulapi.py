from flask  import Flask, request, jsonify, abort
from ast    import literal_eval
from flask_cors import CORS
import server
import json
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
CORS(app)

'''
Add function to check authentication(HMAC, pre-shared key etc.) 
'''
auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    if username == 'test':
        return 'python'
    return None

@auth.error_handler
def unauthorized():
    return jsonify({'error': 'Unauthorized access'}), 401

#Create node
@app.route('/api/nodes', methods=['POST'])
@auth.login_required
def create_node():
    content = request.json
    response =  server.create_node(content)
    return jsonify(response), 201

#Create sensor
@app.route('/api/nodes/<string:node_name>/sensors', methods=['POST'])
@auth.login_required
def create_sensor(node_name):
    content = request.json
    response = server.create_sensor(content, node_name)
    return jsonify(response), 201

#Create reading
@app.route('/api/nodes/<string:node_name>/sensors/<string:sensor_name>/readings', methods=['POST'])
@auth.login_required
def process_reading_post(node_name, sensor_name):
    content = request.json
    response = server.create_reading(content, node_name, sensor_name)
    return jsonify(response), 201

#Get reading
@app.route("/api/locations", methods = ["GET"])
@auth.login_required
def get_all_locations():
    response = server.get_locations()
    return jsonify({'locations' : response})

@app.route("/api/locations/<string:location>/nodes", methods = ["GET"])
@auth.login_required
def get_nodes(location):
    response = server.get_location_nodes(location)
    if len(response) == 0:
        abort(404)
    return jsonify({'nodes' : response})

@app.route("/api/locations/<string:location>/nodes/<string:node_name>/sensors", methods = ["GET"])
@auth.login_required
def get_sensors(location, node_name):
    response = server.get_node_sensors(location, node_name)
    if len(response) == 0:
        abort(404)
    return jsonify({'sensors' : response})

@app.route("/api/locations/<string:location>/nodes/<string:node_name>/sensors/<string:sensor_name>/readings/latest", methods = ["GET"])
@auth.login_required
def get_latest_reading(location, node_name, sensor_name):
    response = server.get_sensor_latest_reading(location, node_name, sensor_name)
    if len(response) == 0:
        abort(404)
    return jsonify({'reading' : response})


def main():
    server.init_database()
    app.run(debug = True, host = '0.0.0.0', port = 3000)


if __name__ == '__main__':
    main()
