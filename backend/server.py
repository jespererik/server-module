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


def __generate_new_node_id():
    latest_name = dbhelper.select_latest_node_name(DB_CONNECTION)
    return 'NODE_' + str(int(latest_name.split('_')[1]) + 1)


#create
def create_node(content):
    if content['NODE_NAME'] = '':
        if dbhelper.is_empty_nodes(DB_CONNECTION):
            content['NODE_NAME'] = 'NODE_1'
            dbhelper.insert_node(DB_CONNECTION, (content['NODE_NAME'], content['LOCATION'],))
        else:
            content['NODE_NAME'] = __generate_new_node_id()
            dbhelper.insert_node(DB_CONNECTION, (content['NODE_NAME'], content['LOCATION'],))
    return content


def create_sensor(content, node_name):
    nodeID = dbhelper.select_node_by_name(DB_CONNECTION, node_name)['id']
    dbhelper.insert_sensor(DB_CONNECTION, (content['SENSOR_NAME'], nodeID))
    return content


def create_reading(content, node_name, sensor_name):
    #type, data, timestamp, sensor_id
    sensorID = dbhelper.select_sensor_by_name_and_node(DB_CONNECTION, sensor_name, node_name)['id']
    dbhelper.insert_reading(DB_CONNECTION, (content['TYPE'], content['DATA'], content['TIMESTAMP'], sensorID ))

    return content


#read
def get_readings(node_name, sensor_name):
    content = dbhelper.select_readings_by_sensor_and_node(DB_CONNECTION, sensor_name, node_name)
    return content

def get_locations():
    pass

#Location queries
def get_location_reading_type_readings(location, reading_type)
    pass

def get_location_readings(location):
    pass

def get_location_nodes(location):
    pass

def get_location_sensors(location):
    pass

def get_location_sensor(location, sensor):
    pass

def get_location_sensor_readings(location, sensor)
    pass

#Node Queries
def get_node(node)
    pass

def get_node_readings(node):
    pass

def get_node_sensors(node):
    pass

def get_node_sensors_readings(node):
    pass

def get_node_sensors_type_readings(node, reading_type):
    pass

def get_node_sensor(node, sensor):
    pass

def get_node_sensor_readings(node, sensor):
    pass

def get_node_sensor_type_readings(node, sensor, reading_type):
    pass

