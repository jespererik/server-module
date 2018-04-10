from datetime import datetime
import sys
import logging
import dbhelper
import random
from datetime import datetime


FORMAT = '%(asctime)s - %(module)s - %(funcName)s - %(levelname)s - %(\nmessage)s'
logging.basicConfig(
    format = FORMAT,
    filename = '/backend/shared/server.log',
    level = logging.DEBUG,
)
SERVER_LOGGER = logging.getLogger(__name__)

DB_CONNECTION = dbhelper.create_connection('/backend/shared/skynet.db')


def init_database():
    dbhelper.create_node_tables(DB_CONNECTION)


def __generate_new_node_id():
    latest_name = dbhelper.select_latest_node_name(DB_CONNECTION)['name']
    return 'NODE_' + str(int(latest_name.split('_')[1]) + 1)


#create
def create_node(content):
    if (content['NODE_NAME'] == ''):
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
def get_locations():
    content = dbhelper.select_all_locations(DB_CONNECTION)
    print(content)
    content = [dicts["location"] for dicts in content]
    return content

def get_location_nodes(location):
    content = dbhelper.select_nodes_by_location(DB_CONNECTION, location)
    return content

def get_node_sensors(location, node_name):
    nodes = dbhelper.select_nodes_by_location(DB_CONNECTION, location) 
    for node in nodes:
        if node["name"] == node_name:
            content = dbhelper.select_all_node_sensors(DB_CONNECTION, node_name)
            return content
    return []

def get_sensor_latest_reading(location, node_name, sensor_name):
    #nodes = dbhelper.select_nodes_by_location(DB_CONNECTION, location)
    #sensors = dbhelper.select_sensor_by_name_and_node(DB_CONNECTION, sensor_name, node_name)
    sensors = get_node_sensors(location, node_name)
    for sensor in sensors:
        if sensor["name"] == sensor_name:
            content = dbhelper.select_latest_reading_by_sensor_and_node(DB_CONNECTION, node_name, sensor_name)
            return content
    return []

#function for debugging
def get_locations_nodes():

    location_nodes = {}
    locations = get_locations()
    content = dbhelper.select_all_nodes(DB_CONNECTION)

    for location in locations:
        nodes = []
        for node in content:
            if node["location"] == location:
                nodes.append(node["name"])
        location_nodes[location] = nodes

    return {"NODE LOCATIONS": location_nodes} 

def creading(reading_type):
    return {
        "TYPE": reading_type,
        "DATA": random.uniform(-15, 40),
        "TIMESTAMP": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


if __name__ == "__main__":
    if sys.argv[1]:
        init_database()

        inhouse_node = {
            "NODE_NAME": "",
            "LOCATION": "inhouse"
        }
        outhouse_node = {
            "NODE_NAME": "",
            "LOCATION": "outhouse"
        }
        heater_node = {
            "NODE_NAME": "",
            "LOCATION": "heater"
        }

        DHT11_sensor = {
            "SENSOR_NAME": "DHT11"
        }

        DHT12_sensor = {
            "SENSOR_NAME": "DHT12"
        }




        inhouse_nodes = [inhouse_node]*5
        outhouse_nodes = [outhouse_node]*5
        heater_nodes = [heater_node]*5

        [create_node(node) for node in inhouse_nodes]
        [create_node(node) for node in outhouse_nodes]
        [create_node(node) for node in heater_nodes]

        [dbhelper.insert_sensor(DB_CONNECTION, ("DHT11", x)) for x in range(1, 11)]
        [dbhelper.insert_sensor(DB_CONNECTION, ("DHT12", x)) for x in range(1, 11)]

        [create_reading(creading("temperature"), ("NODE_" + str(x)), "DHT11") for x in range(1, 6)]
        [create_reading(creading("temperature"), ("NODE_" + str(x)), "DHT11") for x in range(1, 6)]

        [create_reading(creading("humidity"), ("NODE_" + str(x)), "DHT12") for x in range(1, 6)]
        [create_reading(creading("humidity"), ("NODE_" + str(x)), "DHT12") for x in range(1, 6)]



    print("*"*50)
    print("get_locations")
    print(get_locations())
    print("*"*50)
    print("\n")


    print("*"*50)
    print("get_locations_nodes()")
    print(get_locations_nodes())
    print("*"*50)
    print("\n")


    print("*"*50)
    print("get_locations_nodes()")
    print(get_locations_nodes())
    print("*"*50)
    print("\n")