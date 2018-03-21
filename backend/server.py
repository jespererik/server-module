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
def get_readings(node_name, sensor_name):
    content = dbhelper.select_readings_by_sensor_and_node(DB_CONNECTION, sensor_name, node_name)
    return content

def get_locations():
    content = dbhelper.select_all_locations(DB_CONNECTION)
    print(content)
    content = [dicts["location"] for dicts in content]
    return content

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

        inhouse_nodes = [inhouse_node]*5
        outhouse_nodes = [outhouse_node]*5
        heater_nodes = [heater_node]*5

        [create_node(node) for node in inhouse_nodes]
        [create_node(node) for node in outhouse_nodes]
        [create_node(node) for node in heater_nodes]
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