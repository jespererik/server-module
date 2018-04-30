from flask  import Flask, request, jsonify, abort, Response, make_response
from ast    import literal_eval
from flask_cors import CORS
import controller
import json
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
CORS(app)
cors = CORS(app, resources={r"/api/v1.0/*": {"origins": "*", "supports_credentials": "true"}})

'''
Add function to check authentication(HMAC, pre-shared key etc.) 
'''
auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    if username == controller.get_user(username)['name']:
        return controller.get_user_password(username)['password']
    return None

@auth.error_handler
def unauthorized():
    return jsonify({'error': 'Unauthorized access'}), 401

#Create node
@app.route('/api/v1.0/nodes', methods=['POST'])
@auth.login_required
def create_node():
    content = request.json
    response =  controller.create_node(content)
    return jsonify(response), 201

#Create sensor
@app.route('/api/v1.0/nodes/<string:node_name>/sensors', methods=['POST'])
@auth.login_required
def create_sensor(node_name):
    content = request.json
    response = controller.create_sensor(content, node_name)
    return jsonify(response), 201

#Create reading
@app.route('/api/v1.0/nodes/<string:node_name>/sensors/<string:sensor_name>/readings', methods=['POST'])
@auth.login_required
def process_reading_post(node_name, sensor_name):
    content = request.json
    response = controller.create_reading(content, node_name, sensor_name)
    return jsonify(response), 201

#Get reading
@app.route("/api/v1.0/locations", methods = ["GET"])
#@auth.login_required
def get_all_locations():
    response = controller.get_locations()
    return jsonify({'locations' : response}), 200

@app.route("/api/v1.0/locations/<string:location>/nodes", methods = ["GET"])
#@auth.login_required
def get_nodes(location):
    response = controller.get_location_nodes(location)
    if response is None:
        abort(404)
    if len(response) == 0:
        return '', 204
    return jsonify({'nodes' : response}), 200

@app.route("/api/v1.0/locations/<string:location>/nodes/<string:node_name>/sensors", methods = ["GET"])
#@auth.login_required
def get_sensors(location, node_name):
    response = controller.get_node_sensors(location, node_name)
    if response is None:
        abort(404)
    if len(response) == 0:
        return '', 204
    return jsonify({'sensors' : response}), 200

@app.route("/api/v1.0/locations/<string:location>/nodes/<string:node_name>/sensors/<string:sensor_name>/readings/latest", methods = ["GET"])
#@auth.login_required
def get_latest_reading(location, node_name, sensor_name):
    response = controller.get_sensor_latest_reading(location, node_name, sensor_name)
    if response is None:
        abort(404)    
    if len(response) == 0:
        return '', 204
    return jsonify({'reading' : response}),200


def main():
    controller.init_database()
    app.run(debug = True, host = '0.0.0.0', port = 3000)


if __name__ == '__main__':
    main()
