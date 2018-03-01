import sys
import DBHelper
import logging

DB_CONNECTION = DBHelper.create_connection('../shared/database/test.db')

FORMAT = '%(asctime)s %(module)s %(funcName)s %(levelname)s %(message)s'
logging.basicConfig(
    format = FORMAT,
    filename = '../shared/log/server.log',
    level = logging.DEBUG,
)
SERVER_LOGGER = logging.getLogger(__name__)

def init_database():
    DBHelper.create_node_tables()


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
                            sensor_data_packet['TIMESTAMP'],
                            sensor_data_packet['DATA']
                        )
        add_node_reading(sensor_name, node_name, reading_entry)
    
    SERVER_LOGGER.debug('EXIT')
    return sensor_data_packet




def node_init_packet_handler(node_init_packet):
    SERVER_LOGGER.debug('ENTER')
    if __is_init_packet(node_init_packet):
        if node_init_packet['NODE_NAME'] == '':
            node_init_packet['NODE_NAME'] = create_new_node(node_init_packet['LOCATION'])
        node_init_packet['NODE_NAME'] 

    SERVER_LOGGER.debug('EXIT')    
    return node_init_packet


def create_new_node(location):
    #Refactor this, too messy?
    SERVER_LOGGER.debug('ENTER')

    if DBHelper.is_table_empty('nodes'):
        SERVER_LOGGER.debug('\n   No nodes in table "nodes" creating first node "Node#1"')
        DBHelper.insert_node(('Node#1', location))

        SERVER_LOGGER.debug('EXIT')
        return 'Node#1'
    else:
        latest_name = DBHelper.get_latest_node_name(DB_CONNECTION)
        new_name, new_id = latest_name.split('#')
        new_node_name = new_name + '#' + str(int(new_id) + 1)
        SERVER_LOGGER.debug('\n Inserting new "node" {} with location {}'.format(new_node_name, location))
        DBHelper.insert_node((new_node_name, location))

        SERVER_LOGGER.debug('EXIT')
        return new_node_name
    

def add_sensor_to_node(sensor_name, node_name):
    SERVER_LOGGER.debug('ENTER')

    SERVER_LOGGER.debug('\n Inserting "sensor" {} on "node" {}'.format(sensor_name, node_name))
    sensor_info = (sensor_name, DBHelper.get_node_id_by_name(node_name))
    DBHelper.insert_sensor(sensor_info)

    SERVER_LOGGER.debug('EXIT')

def add_node_reading(sensor_name, node_name, reading_entry):
    SERVER_LOGGER.debug('ENTER')

    if(DBHelper.get_sensor_id_by_name(sensor_name, node_name) is None):
        SERVER_LOGGER.debug('\n "sensor" {} not found on "node" adding'.format(sensor_name, node_name))
        DBHelper.add_sensor_to_node(new_sensor_name, node_name)
    reading_entry += DBHelper.get_sensor_id_by_name(sensor_name, node_name)
    SERVER_LOGGER.debug('\n Inserting "reading" {}'.format(reading_entry))
    DBHelper.insert_reading(reading_entry)

    SERVER_LOGGER.debug('EXIT')
