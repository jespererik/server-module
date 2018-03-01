import sqlite3
from datetime import datetime
import logging

FORMAT = '%(asctime)s %(module)s %(funcName)s %(levelname)s %(message)s'
logging.basicConfig(
    format = FORMAT,
    filename = '../shared/log/Database.log',
    level = logging.DEBUG
)

DB_LOGGER = logging.getLogger(__name__)
DB_LOGGER.propagate = True

#It's getting ridicilous with all the loggers, really a good approach?


def is_table_empty(conn, table_name):
    #Will there be a problem with True return for success and 1 return on error?
    #This function is probably too long aswell
    DB_LOGGER.debug('ENTER')

    tokens = (table_name,)
    try:
        c_cursor = conn.cursor()
        DB_LOGGER.debug('\n  is empty? {}'.format(table_name))
        query_result = c_cursor.execute('SELECT count(*) FROM = ?', tokens)

        if query_result is 0:
            DB_LOGGER.debug('EXIT') 
            return True

        else:
            DB_LOGGER.debug('EXIT')
            return False

    except sqlite3.Error as e:
        DB_LOGGER.error('\n  '.format(e))
        DB_LOGGER.debug('EXIT')
        return 1


#CRUD
def create_connection(db_file):
    DB_LOGGER.debug('ENTER')
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        DB_LOGGER.error('\n  '.format(e))
        DB_LOGGER.debug('EXIT')
        return 1


def create_table(conn, create_table_sql):
    DB_LOGGER.debug('ENTER')

    try:
        c_cursor = conn.cursor()
        DB_LOGGER.debug('\n  Creating table {}'.format(create_table_sql))
        c_cursor.execute(create_table_sql)
        DB_LOGGER.info('\n   Created table {}'.format(create_table_sql))
        conn.commit()

        DB_LOGGER.debug('EXIT')
        return 0
    except sqlite3.Error as e:
        DB_LOGGER.error('\n  '.format(e))    
        DB_LOGGER.debug('EXIT')
        return 1

'''
def create_index(conn, index_name, table_name, column_name):
    DB_LOGGER.debug('ENTER')
    tokens = (index_name, table_name, column_name)
    try:
        c_cursor = conn.cursor()
        DB_LOGGER.debug('\n  Creating index {} for table {}'.format(index_name, table_name))
        c_cursor.execute('CREATE INDEX ? ON ?(?)', tokens)
        
        DB_LOGGER.debug('EXIT')
        return 0

    except sqlite3.error as e:
        DB_LOGGER.error('\n  '.format(e))

    DB_LOGGER.debug('EXIT')
    return 1
'''
def insert_node(conn, node_info):
    DB_LOGGER.debug('ENTER')

    try:
        insert_cursor = conn.cursor()
        DB_LOGGER.debug('\n  Inserting {} into table "nodes"'.format(node_info))

        insert_cursor.execute('INSERT INTO nodes(name, location) VALUES (?, ?)', node_info)
        conn.commit()
        
        DB_LOGGER.info('\n   Inserted {} into table "nodes"'.format(node))
        return 0
    except sqlite3.Error as e:
        DB_LOGGER.error('\n  '.format(e))  
        DB_LOGGER.debug('EXIT')
        return 1


def insert_sensor(conn, sensor_info):
    DB_LOGGER.debug('ENTER')

    try:
        insert_cursor = conn.cursor()
        DB_LOGGER.debug('\n  Inserting {} into table "sensors"'.format(sensor_info))

        insert_cursor.execute('INSERT INTO sensors(name, node_id) VALUES (?, ?)', sensor_info)
        conn.commit()
        
        DB_LOGGER.info('\n   Inserted {} into table "sensors"'.format(sensor))
        return 0

    except sqlite3.Error as e:
        DB_LOGGER.error('\n  '.format(e))
        DB_LOGGER.debug('EXIT')
        return 1


def insert_reading(conn, reading):
    DB_LOGGER.debug('ENTER')

    try:
        insert_cursor = conn.cursor()
        DB_LOGGER.debug('\n  Inserting {} into table "readings"'.format(reading))

        insert_cursor.execute('INSERT INTO readings(readingtype, data, timestamp, sensor_id) VALUES (?, ?, ?, ?)', reading)
        conn.commit()
        
        DB_LOGGER.info('\n   Inserted {} into table "readings"'.format(reading))
        DB_LOGGER.debug('EXIT')
        return 0

    except sqlite3.Error as e:
        DB_LOGGER.error('\n  '.format(e))
        DB_LOGGER.debug('EXIT')
        return 1
    
def get_latest_node_name(conn):
    DB_LOGGER.debug('ENTER')

    try:
        query_cursor = conn.cursor()
        DB_LOGGER('\n    Querying for latest "nodes" entry "name"')

        query_result = query_cursor.execute('SELECT name FROM nodes GROUP BY name').fetchone()[0]

        DB_LOGGER.debug('\n  Found {}'.format(query_result))
        DB_LOGGER.debug('EXIT')
        return query_result

    except:
        DB_LOGGER.error('\n  '.format(e))
        DB_LOGGER.debug('EXIT')
        return 1


def get_nodes_by_name(conn, node_name):
    DB_LOGGER.debug('ENTER')

    tokens = (node_name,)
    try:
        query_cursor = conn.cursor()
        DB_LOGGER.debug('\n  Querying nodes for * with name {}'.format(node_name))

        query_result = query_cursor.execute('SELECT * FROM nodes WHERE name = ?', tokens).fetchall()

        DB_LOGGER.debug('\n  Found {}'.format(query_result))
        
        DB_LOGGER.debug('EXIT')
        return query_result
    
    except sqlite3.Error as e:
        DB_LOGGER.error('\n  '.format(e))
        DB_LOGGER.debug('EXIT')
        return 1


def get_sensors_by_name(conn, sensor_name):
    '''
        Executes a SELECT statement on the given database connection "conn" to get all entries of the "sensors" table
        where column "name" == "sensor_name"

        params: conn sqlite3.connection('path/to/file.db')
                sensor_name string

        return: on success a list of tuples containing all columns of the matching "sensors" entries
                on sqlite3.error int 1

        Example usaage:
            get_readings_by_sensor_id(
                DB_CONNECTION,
                'DHT11'
            )

    '''
    DB_LOGGER.debug('ENTER')

    tokens = (sensor_name,)
    try:
        query_cursor = conn.cursor()
        DB_LOGGER.debug('\n  Querying sensors for * with name {}'.format(sensor_name))

        query_result = query_cursor.execute('SELECT * FROM sensors WHERE name = ?', tokens).fetchall()
        
        DB_LOGGER.debug('\n  Found {}'.format(query_result))

        DB_LOGGER.debug('EXIT')
        return query_result
    
    except sqlite3.Error as e:
        DB_LOGGER.error('\n  '.format(e))
        DB_LOGGER.debug('EXIT')
        return 1


def get_node_id_by_name(conn, node_name):
    '''
        Executes a SELECT statement on the given database connection "conn" to get all entries of the "nodes" table
        where column "name" == "node_name"

        params: conn sqlite3.connection('path/to/file.db')
                node_name string

        return: on sucess returns the id of the matching entry as an integer
                on sqlite3.error 1

        Example usaage:
            get_readings_by_sensor_id(
                DB_CONNECTION,
                'Node#1'
            )

    '''
    DB_LOGGER.debug('ENTER')

    tokens = (node_name,)
    try:
        query_cursor = conn.cursor()
        DB_LOGGER.debug('\n  Querying for id with name {} in nodes'.format(node_name))

        query_result = query_cursor.execute('SELECT id FROM nodes WHERE name = ?', tokens).fetchone()[0]

        DB_LOGGER.debug('\n  Found {}'.format(query_result))
        
        DB_LOGGER.debug('EXIT')
        return query_result
    
    except sqlite3.Error as e:
        DB_LOGGER.error(e)
        DB_LOGGER.debug('EXIT')
        return 1
    
def get_sensor_id_by_name(conn, sensor_name, node_name):
    '''
        Executes a SELECT statement on the given database connection "conn" 
        to get all entries of the "sensors" table which
        have the "node_id" of "node_name" in table "nodes" and the name sensor_name in "sensors"

        Args: 
            conn: an instance sqlite3.connection('path/to/file.db')
            sensor_name: A string representing the sensor_name that is being searched for
            node_name: A string representing the node_name that is being searched for

        return: 
            The id of the queried sensor entry as an integer
        
        Raises:
            sqlite3.Error


        Example usage:
            get_readings_by_sensor_id(
                DB_CONNECTION,
                'DHT11',
                'Node#1'
            )

    '''
    DB_LOGGER.debug('ENTER')

    tokens = (sensor_name, node_name,)
    try:
        query_cursor = conn.cursor()
        DB_LOGGER.debug('\n  Querying for name {} with nodes.name {} in sensor'.format(sensor_name, node_name))

        query_result = query_cursor.execute(
            'SELECT sensors.id FROM sensors,nodes WHERE (sensors.name = ? AND nodes.name = ?))', tokens).fetchone()[0]

        DB_LOGGER.debug('\n  Found {}'.format(query_result))

        DB_LOGGER.debug('EXIT')
        return query_result
    
    except sqlite3.Error as e:
        DB_LOGGER.error(e)
        DB_LOGGER.debug('EXIT')
        return 1


def get_readings_by_sensor_id(conn, sensor_id):
    '''
        Executes a SELECT statement on the given database connection to get all entries of the readings table which
        have a matching sensor_id

        params: conn sqlite3.connection('path/to/file.db')
                sensor_id integer

        return: on sucessA list of tuples containing the data and timestamps columns of the readings table
                on sqlite3.error 1

        Example usaage:
            get_readings_by_sensor_id(
                DB_CONNECTION,
                get_sensor_id_by_name(DB_CONNECTION, 'DHT11', 'Node#1')
            )

    '''
    DB_LOGGER.debug('ENTER')

    tokens = (sensor_id,)
    try:
        query_cursor = conn.cursor()
        DB_LOGGER.debug('\n  Querying for sensor_id {} in readings'.format(sensor_id))

        query_result = query_cursor.execute('SELECT data, timestamp FROM readings WHERE sensor_id = ?', tokens).fetchall()

        DB_LOGGER.debug('\n  Found {}'.format(query_result))

        DB_LOGGER.debug('EXIT')
        return query_result

    except sqlite3.Error as e:
        DB_LOGGER.error(e)  
        DB_LOGGER.debug('EXIT')
        return 1

def get_readings_by_location(conn, node_location):
    '''
        Executes a SELECT statement on the given database connection to get all entries of the readings table which
        are connected to a node with the given location 

        params: conn is the database connection
                node_location is the physical placement of a node given a symbolic name for access
        return: on success a List of tuples where the tuples contain the data and timestamp columns of the table readings
                on sqlite3.error 1
    '''
    DB_LOGGER.debug('ENTER')

    tokens = (node_location,)
    try:
        query_cursor = conn.cursor()
        DB_LOGGER.debug('\n  Querying for readings with location {}'.format(node_location))

        query_result = query_cursor.execute(
            'SELECT data, timestamp FROM readings WHERE sensor_id = (SELECT id FROM sensors WHERE node_id = (SELECT id FROM nodes WHERE location = ?))', tokens).fetchall()
        
        DB_LOGGER.debug('\n  Found {}'.format(query_result))
        DB_LOGGER.debug('EXIT')
        return query_result

    except sqlite3.Error as e:
        DB_LOGGER.error('\n  '.format(e))
        DB_LOGGER.debug('EXIT')
        return 1
    

def create_node_tables(conn):
    '''
        Creates all tables related to a node to the given database connection 
        with the function create_table()

        sql statements:
        CREATE TABLE IF NOT EXISTS nodes(
                id integer PRIMARY KEY, 
                name text NOT NULL UNIQUE,
                location text
                created DateTime DEFAULT CURRENT_DATE
            );
        CREATE TABLE IF NOT EXISTS sensors(
                id integer PRIMARY KEY, 
                name text NOT NULL,
                node_id integer, 
                    FOREIGN KEY (node_id) REFERENCES nodes(id) ON DELETE RESTRICT ON UPDATE CASCADE,
                UNIQUE (id, node_id)
                UNIQUE (node_id, name)     
            );    
        CREATE TABLE IF NOT EXISTS readings (
            readingtype text, 
            data float, 
            timestamp DateTime,
            sensor_id integer NOT NULL,
                FOREIGN KEY (sensor_id) REFERENCES sensors(id) ON DELETE RESTRICT ON UPDATE CASCADE
            );
        
        return: 0 on success
                1 if any of create_table() calls failed
    '''
    DB_LOGGER.debug('ENTER')

    try:
        create_table(
            conn,
            '''CREATE TABLE IF NOT EXISTS nodes(
                    id integer PRIMARY KEY, 
                    name text NOT NULL UNIQUE,
                    location text
                    created DateTime DEFAULT CURRENT_DATE
                );
            '''
        )
        create_table(
            conn,
            '''CREATE TABLE IF NOT EXISTS sensors(
                id integer PRIMARY KEY, 
                name text NOT NULL,
                node_id integer, 
                    FOREIGN KEY (node_id) REFERENCES nodes(id) ON DELETE RESTRICT ON UPDATE CASCADE,
                UNIQUE (id, node_id)
                UNIQUE (node_id, name)     
                );                         
            '''
        )
        create_table(
            conn,
            '''CREATE TABLE IF NOT EXISTS readings (
                readingtype text, 
                data float, 
                timestamp DateTime,
                sensor_id integer NOT NULL,
                    FOREIGN KEY (sensor_id) REFERENCES sensors(id) ON DELETE RESTRICT ON UPDATE CASCADE
                );
            '''
        )
        conn.commit()
        DB_LOGGER.debug('EXIT')
        return 0
    except:
        DB_LOGGER.error('\n  Failed to create all tables, see create_table() calls for more information')
        DB_LOGGER.debug('EXIT')
        return 1
    
if __name__ == '__main__':
    DB_CONNECTION = create_connection('../shared/database/example.db')

    create_node_tables(DB_CONNECTION)
    insert_node(DB_CONNECTION, ('Node#1', 'outhouse'))
    insert_node(DB_CONNECTION, ('Node#2', 'outhouse'))
    insert_node(DB_CONNECTION, ('Node#3', 'inhouse'))
    insert_sensor(DB_CONNECTION, ('DHT11', get_node_id_by_name(DB_CONNECTION, 'Node#1')))
    insert_sensor(DB_CONNECTION, ('DHT11', get_node_id_by_name(DB_CONNECTION, 'Node#2')))
    insert_sensor(DB_CONNECTION, ('DHT11', get_node_id_by_name(DB_CONNECTION, 'Node#3')))


    insert_reading(
        DB_CONNECTION,
        (
            'temperature',
            23.43,
            datetime.now(),
            get_sensor_id_by_name(
                DB_CONNECTION,
                'DHT11',
                'Node#1'
            )
        )
    )


    insert_reading(
        DB_CONNECTION,
        (
            'temperature',
            23.43,
            datetime.now(),
            get_sensor_id_by_name(
                DB_CONNECTION,
                'DHT11',
                'Node#3'
            )
        )
    )


    print(
        get_readings_by_location(
            DB_CONNECTION,
            'outhouse'
        )
    )


    print(
        get_readings_by_location(
            DB_CONNECTION,
            'inhouse'
        )
    )


    print(
        get_nodes_by_name(
            DB_CONNECTION,
            'Node#1'
        )
    )

    print(
        get_sensors_by_name(
            DB_CONNECTION,
            'DHT11'
        )
    )

    print(
        get_readings_by_sensor_id(
            DB_CONNECTION,
            get_sensor_id_by_name(
                DB_CONNECTION,
                'DHT11',
                'Node#1'
            )
        )
    )

