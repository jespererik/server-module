from flask  import Flask, request, jsonify
from ast    import literal_eval
import Server
import json

app = Flask(__name__)

sensorData = {
        'nodeID'    :'',
        'dataType'  :'',
        'timestamp' :'',
        'data'      :''
    }

@app.route('/init', methods=['GET', 'POST'])
def nodeInit():
    content = request.json
    if content['NODE_ID'] == '': content['NODE_ID'] = Server.Get_Node_ID()
    return jsonify(content)

@app.route('/Temp', methods=['POST'])
def nodeTemp():
    content = request.json
    sensorData = {
        'nodeID'    :content['nodeID'],
        'dataType'  :content['dataType'],
        'timestamp' :content['timestamp'],
        'data'      :content['data']
    }
    with open('textdb.txt', 'a') as dbfile:
        dbfile.writelines(sensorData)
    dbfile.close()
    print json.dumps(sensorData)
    return jsonify(sensorData), 201


if __name__ == '__main__':
    
    Server.Populate_NODE_ID_Log()
    Server.Read_Node_Log()
    Server.Read_Server_Config()

    print Server.server_config['SERVER_PORT']
    app.run(debug = True, port = int(Server.server_config['SERVER_PORT']))