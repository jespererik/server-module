import sys
import DBHelper
import logging

DB_CONNECTON = DBHelper.create_connection('../shared/database/test.db')

FORMAT = '%(asctime)s %(module)s %(funcName)s %(levelname)s %(message)s'
logging.basicConfig(
    format = FORMAT,
    filename = '../shared/log/server.log',
    level = logging.DEBUG,
)
SERVER_LOGGER = logging.getLogger(__name__)


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
    

    if (recieved_packet.keys() == packet_check):
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

    if (recieved_packet.keys() == packet_check):
        SERVER_LOGGER.debug('\n Check passed for {}'.format(recieved_packet))
        SERVER_LOGGER.debug('EXIT')
        return True
    else:
        SERVER_LOGGER.debug('\n Check Failed for {}'.format(recieved_packet)) 
        SERVER_LOGGER.debug('EXIT')
        return False
        


def create_database():
    DBHelper.create_node_tables(DB_CONNECTON)
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
        node_name   = node_packet['NODE_NAME']
        sensor_name = node_packet['SENSOR_NAME']
        reading_entry = tuple(
                            node_packet['TYPE'],
                            node_packet['TIMESTAMP'],
                            node_packet['DATA']
                        )
        add_node_reading(sensor_name, node_name, reading_entry)
        return node_packet

    SERVER_LOGGER.debug('EXIT')


def node_init_packet_handler(node_init_packet):
    if __is_init_packet(node_init_packet):
        if init_packet['NODE_NAME'] is None:
            init_packet['NODE_NAME'] = create_new_node(init_packet['LOCATION'])
        init_packet['NODE_NAME'] 

        return init_packet


def create_new_node(location):
    #Refactor this, too messy
    if DBHelper.is_table_empty(DB_CONNECTON, 'nodes'):
        DBHelper.insert_node(DB_CONNECTON, ('Node#1', location))
        return 'Node#1'
    else:
        latest_name = DBHelper.get_latest_node_name(DB_CONNECTON)
        new_name, new_id = latest_name.split('#')
        new_node_name = new_name + '#' + str(int(new_id) + 1)
        DBHelper.insert_node(DB_CONNECTON, (new_node_name, location))
        return new_node_name
    

def add_sensor_to_node(sensor_name, node_name):
    sensor_info = (sensor_name, DBHelper.get_node_id_by_name(DB_CONNECTON, node_name))
    DBHelper.insert_sensor(DB_CONNECTON, sensor_info)
    

def add_node_reading(sensor_name, node_name, reading_entry):
    if(DBHelper.get_sensor_id_by_name(sensor_name)):
        DBHelper.add_sensor_to_node(new_sensor_name, node_name)
    reading_entry[3] = DBHelper.get_sensor_id_by_name(sensor_name, node_name)
    DBHelper.insert_reading(DB_CONNECTON, reading_entry)