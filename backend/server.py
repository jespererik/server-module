from datetime import datetime
import sys
import dbhelper
import logging


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


def __is_init_packet(recieved_packet):
    '''
        Checks if the packet is the correct format for processing in the node_data_packet_handler

        The reason for the packet_check tuple is reversed to the actual ordering of the dict keys
        is because if you call <somedict>.keys() it seems to reverse the order.

        Args:
            recieved packet: JSON object which contains the fields
                NODE_NAME
                SENSOR_NAME
                TYPE
                TIMESTAMP
                DATA

        return:
            If the packet is the correct format return True
            if not return False
    '''
    SERVER_LOGGER.debug('ENTER')
    packet_check = ('LOCATION', 'NODE_NAME')
    
    if bool(set(recieved_packet.keys()) & set(packet_check)):
        SERVER_LOGGER.debug('\n Check passed for {}'.format(recieved_packet))
        SERVER_LOGGER.debug('EXIT')
        return True

    else:
        SERVER_LOGGER.debug('\n Check failed for {}'.format(recieved_packet)) 
        SERVER_LOGGER.debug('EXIT')
        return False
        

def __is_sensor_data_packet(recieved_packet):
    '''
        Checks if the packet is the correct format for processing in the node_init_packet_handler
        
        The reason for the packet_check tuple is reversed to the actual ordering of the dict keys
        is because if you call <somedict>.keys() it seems to reverse the order.

        Args:
            recieved packet: JSON object which contains the nodes name and location

        return:
            If the packet is the correct format return True
            if not return False
    '''
    SERVER_LOGGER.debug('ENTER')
    packet_check = ('DATA', 'TIMESTAMP', 'TYPE', 'SENSOR_NAME', 'NODE_NAME')

    if bool(set(recieved_packet.keys()) & set(packet_check)):
        SERVER_LOGGER.debug('\n Check passed for {}'.format(recieved_packet))
        SERVER_LOGGER.debug('EXIT')
        return True
    else:
        SERVER_LOGGER.debug('\n Check Failed for {}'.format(recieved_packet)) 
        SERVER_LOGGER.debug('EXIT')
        return False
        

def node_data_packet_handler(sensor_data_packet):
    '''
        If the recieved sensor_data_packet passes the __is_sensor_data_packet
        check parses the packet formats the data for insertion into the readings
        table in the connected database

        Args:

        return:
    '''

    SERVER_LOGGER.debug('ENTER')

    if __is_sensor_data_packet(sensor_data_packet):
        SERVER_LOGGER.debug('\n Recieved "sensor_data_packet" {}, adding to database'.format(sensor_data_packet))
        node_name   = sensor_data_packet['NODE_NAME']
        sensor_name = sensor_data_packet['SENSOR_NAME']
        reading_entry = (
                            sensor_data_packet['TYPE'],
                            sensor_data_packet['DATA'],
                            sensor_data_packet['TIMESTAMP']
                        )
        add_reading(sensor_name, node_name, reading_entry)
        return sensor_data_packet
    else:
        return 
    
    SERVER_LOGGER.debug('EXIT')
    

def node_init_packet_handler(node_init_packet):
    SERVER_LOGGER.debug('ENTER')
    if __is_init_packet(node_init_packet):
        if node_init_packet['NODE_NAME'] == '':
            node_init_packet['NODE_NAME'] = add_node(node_init_packet['LOCATION'])

    SERVER_LOGGER.debug('EXIT')    
    return node_init_packet

def __generate_new_node_id():
    latest_name = dbhelper.select_latest_node_name(DB_CONNECTION)
    return 'NODE#' + str(int(latest_name.split('#')[1]) + 1)

def add_node(location):
    SERVER_LOGGER.debug('ENTER')

    if dbhelper.is_empty_nodes(DB_CONNECTION):
        dbhelper.insert_node(DB_CONNECTION, ('NODE#1', location,))

        SERVER_LOGGER.debug('EXIT')
        return 'NODE#1'
    else:
        new_node_name = __generate_new_node_id()
        dbhelper.insert_node(DB_CONNECTION, (new_node_name, location,))

        SERVER_LOGGER.debug('EXIT')
        return new_node_name
    

def add_sensor(sensor_name, node_name):
    SERVER_LOGGER.debug('ENTER')

    dbhelper.insert_sensor(DB_CONNECTION, (sensor_name, dbhelper.select_node_id_by_name(DB_CONNECTION, node_name)))

    SERVER_LOGGER.debug('EXIT')

def add_reading(sensor_name, node_name, reading_entry):
    #When a node reading comes in, we will also register the sensor it came from
    #instead of pre-registrering it with the node init.

    #@Cleanup Move Sensor adding to node_data_packet_handler()

    SERVER_LOGGER.debug('ENTER')

    if not (dbhelper.select_sensor_id_by_name_and_node(DB_CONNECTION, sensor_name, node_name)):
        SERVER_LOGGER.info('\n=> "sensor" {} not found on "node", adding'.format(sensor_name, node_name))
        add_sensor(sensor_name, node_name)
    reading_entry += (dbhelper.select_sensor_id_by_name_and_node(DB_CONNECTION, sensor_name, node_name),)
    dbhelper.insert_reading(DB_CONNECTION, reading_entry)

    SERVER_LOGGER.debug('EXIT')


#@Note get all the reading information from db, filter later? or filter with sql?
#@Note add checks for the params on the get functions? Or should they just be a interface between the restfulapi.py and dbhelper.py

#Node GETs
def get_nodes():
    SERVER_LOGGER.debug('ENTER')
    SERVER_LOGGER.debug('EXIT')
    return dbhelper.select_all_nodes(DB_CONNECTION)


def get_location_nodes(node_location):
    SERVER_LOGGER.debug('ENTER')
    SERVER_LOGGER.debug('EXIT')
    return dbhelper.select_node_by_location(DB_CONNECTION, node_location)


#Sensor GETs
def get_node_sensors(node_name):
    SERVER_LOGGER.debug('ENTER')
    SERVER_LOGGER.debug('EXIT')
    return dbhelper.select_all_node_sensors(node_name)

def get_location_sensors(node_location):
    SERVER_LOGGER.debug('ENTER')
    SERVER_LOGGER.debug('EXIT')
    return dbhelper.select_all_location_sensors(DB_CONNECTION, node_location)

#Reading GETs
def get_type_readings(reading_type):
    SERVER_LOGGER.debug('ENTER')
    
    SERVER_LOGGER.debug('EXIT')
    return dbhelper.select_readings_by_type(DB_CONNECTION, reading_type)

def get_node_readings(node_name):
    SERVER_LOGGER.debug('ENTER')

    SERVER_LOGGER.debug('EXIT')
    return dbhelper.select_readings_by_node(DB_CONNECTION, node_name)

def get_location_readings(node_location):
    SERVER_LOGGER.debug('ENTER')

    SERVER_LOGGER.debug('EXIT')
    return dbhelper.select_readings_by_node_location(DB_CONNECTION, node_location)



if __name__ == '__main__':
    if sys.argv[1]:
        dbhelper.create_node_tables(DB_CONNECTION)
        add_node('Outhouse')
        add_sensor('DHT11', 'NODE#1')
        add_reading(
            'DHT11',
            'NODE#1',
            ('temp', 12.345, datetime.now())    
        )


    print(dbhelper.select_node_by_location(DB_CONNECTION, 'Outhouse'))

    print(dbhelper.execute_select_fetchall(
        DB_CONNECTION, 
        'SELECT * FROM sensors WHERE name = ?',
        ('DHT11',)
        )
    )

    print(dbhelper.select_readings_by_type(DB_CONNECTION, 'temp'))
