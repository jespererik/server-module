from datetime import datetime
import sys
import logging
import dbhelper


FORMAT = '%(asctime)s - %(module)s - %(funcName)s - %(levelname)s - %(\nmessage)s'
logging.basicConfig(
    format = FORMAT,
    filename = '/server-module/shared/server.log',
    level = logging.DEBUG,
)
SERVER_LOGGER = logging.getLogger(__name__)



DB_CONNECTION = dbhelper.create_connection('/server-module/shared/skynet.db')
def init_database():
    dbhelper.create_node_tables(DB_CONNECTION)

#create
def create_node(content):
    if dbhelper.is_empty_nodes(DB_CONNECTION):
        content['NODE_NAME'] = 'NODE_1'
        dbhelper.insert_node(DB_CONNECTION, (content['NODE_NAME'], content['LOCATION'],))
        return content
    else:
        content['NODE_NAME'] = __generate_new_node_id()
        dbhelper.insert_node(DB_CONNECTION, (content['NODE_NAME'], content['LOCATION'],))
        return content

def create_sensor(content, node_name):
    nodeID = dbhelper.select_node_id_by_name(DB_CONNECTION, node_name)
    dbhelper.insert_sensor(DB_CONNECTION, (content['SENSOR_NAME'], nodeID))
    return content

def create_reading(content, node_name, sensor_name):
    #type, data, timestamp, sensor_id
    sensorID = dbhelper.select_sensor_id_by_name_and_node(DB_CONNECTION, sensor_name, node_name)
    content['TIMESTAMP'] = datetime.now()
    dbhelper.insert_reading(DB_CONNECTION, (content['TYPE'], content['DATA'], content['TIMESTAMP'], sensorID ))

    return content

def __generate_new_node_id():
    latest_name = dbhelper.select_latest_node_name(DB_CONNECTION)
    return 'NODE_' + str(int(latest_name.split('_')[1]) + 1)

#read
def get_readings(node_name, sensor_name):
    content = dbhelper.select_readings_by_sensor_and_node(DB_CONNECTION, sensor_name, node_name)
    return content
