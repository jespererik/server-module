#!usr/bin/env python3
from datetime import datetime
import sys
import sqlite3
import logging

FORMAT = '%(asctime)s %(module)s %(funcName)s %(levelname)s %(message)s'
logging.basicConfig(
    format = FORMAT,
    filename = '/backend/shared/database.log',
    filemode = 'w',
    level = logging.DEBUG
)

DB_LOGGER = logging.getLogger(__name__)
DB_LOGGER.propagate = True



#@Cleanup Logger messages and logging events
#@Cleanup return None on failure not the best approach?
#@Cleanup changing from specific sql queries to a more general structure

#TODO CRUD for each table
#TODO Write tests
def is_empty_nodes(conn):
    DB_LOGGER.debug('ENTER')

    sql = ('SELECT count(*) FROM nodes')
    result = execute_select_fetchone(conn, sql)

    DB_LOGGER.debug('EXIT')
    return not result['count(*)']

        

def create_connection(db_file):
    #TODO DocString
    '''Creates a connection to a the specified .db file <db_file>

        Args:
            db_file: the path of the .db file that is to be opened
        
        Return:
            conn: The sqlite3.connection object related to the specified file
        
        Raises:
            sqlite3.Error which is written to a log file
    '''
    DB_LOGGER.debug('ENTER')
    DB_LOGGER.info('\n=> CONNECTING TO: %s', db_file)
    try:
        conn = sqlite3.connect(db_file, check_same_thread = False)
        conn.row_factory = lambda cursor, row: dict(zip([col[0] for col in cursor.description], row))
        return conn
    except sqlite3.Error as e:
        DB_LOGGER.error(e)
        DB_LOGGER.debug('EXIT')
        return None


def create_table(conn, create_table_sql):
    #TODO DocString
    DB_LOGGER.debug('ENTER')

    try:
        c_cursor = conn.cursor()
        DB_LOGGER.debug('\n=> Creating table %s', create_table_sql)
        c_cursor.execute(create_table_sql)
        DB_LOGGER.info('\n=> Created table %s', create_table_sql)
        conn.commit()

        DB_LOGGER.debug('EXIT')
        return True
    except sqlite3.Error as e:
        DB_LOGGER.error(e)    
        DB_LOGGER.debug('EXIT')
        return False


def execute_insert(conn, insert_statement, tokens):
    DB_LOGGER.debug('ENTER')
    try:
        insert_cursor = conn.cursor()
        DB_LOGGER.debug('\n=> Excecuting: %s', insert_statement)

        insert_cursor.execute(insert_statement, tokens)
        conn.commit()
        
        DB_LOGGER.info('\n=> Executed: %s',insert_statement)
        return True

    except sqlite3.Error as e:
        DB_LOGGER.error(e)  
        DB_LOGGER.debug('EXIT')
    
    return False

def insert_user(conn):
    values = ("test", "python")
    sql = 'INSERT INTO users(name, password) VALUES(?, ?)'
    return execute_insert(conn, sql, values)

def insert_node(conn, values):
    sql = 'INSERT INTO nodes(name, location) VALUES (?, ?)'
    return execute_insert(conn, sql, values)


def insert_sensor(conn, values):
    sql = 'INSERT INTO sensors(name, node_id) VALUES (?, ?)'
    return execute_insert(conn, sql, values)

def insert_reading(conn, values):
    sql = 'INSERT INTO readings(type, data, timestamp, sensor_id) VALUES (?, ?, ?, ?)'
    return execute_insert(conn, sql, values)


def execute_select_fetchone(conn, select_statement, tokens = ()):
    DB_LOGGER.debug('ENTER')
    DB_LOGGER.debug('\n=> Executing: %s \nValues: %s', select_statement, tokens)
    query_result = {}
    try:
        select_cursor = conn.cursor()
        query_result = select_cursor.execute(select_statement, tokens).fetchone()
        DB_LOGGER.debug('\n=> Found: %s', query_result)

    except sqlite3.Error as e:
        DB_LOGGER.error(e)

    DB_LOGGER.debug('EXIT')
    return query_result if not None else {}

def execute_select_fetchall(conn, select_statement, tokens = ()):
    DB_LOGGER.debug('ENTER')
    DB_LOGGER.debug('\n=> Executing: %s with Values: %s', select_statement, tokens)
    query_result = {}
    try:
        select_cursor = conn.cursor()
        query_result = select_cursor.execute(select_statement, tokens).fetchall()

        DB_LOGGER.debug('\n=> Found: %s', query_result)

        return query_result
    except sqlite3.Error as e:
        DB_LOGGER.error('\n%s', e)

    DB_LOGGER.debug('EXIT')
    return query_result if not None else {}
    
#####################################################################
#Select Statements for users                                     
##################################################################### 
def select_user_name(conn, username):
    DB_LOGGER.debug('ENTER')
    
    tokens = (username,)
    sql = 'SELECT name FROM users WHERE name = ?'
    result = execute_select_fetchone(conn, sql, tokens)

    DB_LOGGER.debug('EXIT')
    return result

def select_user_password(conn, username):
    DB_LOGGER.debug('ENTER')
    
    tokens = (username,)
    sql = 'SELECT password FROM users WHERE name = ?'
    result = execute_select_fetchone(conn, sql, tokens)

    DB_LOGGER.debug('EXIT')
    return result

#####################################################################
#Select Statements for nodes                                     
#####################################################################
def select_all_nodes(conn):
    DB_LOGGER.debug('ENTER')

    sql = 'SELECT * FROM nodes'
    result = execute_select_fetchall(conn, sql)

    DB_LOGGER.debug('EXIT')
    return result


def select_all_locations(conn):
    DB_LOGGER.debug("ENTER")

    sql = 'SELECT DISTINCT location FROM nodes'
    result = execute_select_fetchall(conn, sql)

    DB_LOGGER.debug("EXIT")
    return result


def select_nodes_by_location(conn, node_location):
    DB_LOGGER.debug('ENTER')

    sql = 'SELECT * FROM nodes WHERE location = ?'
    tokens = (node_location,)
    result = execute_select_fetchall(conn, sql, tokens)

    DB_LOGGER.debug('EXIT')
    return result


def select_latest_node_name(conn):
    DB_LOGGER.debug('ENTER')

    sql = 'SELECT name FROM nodes ORDER BY name DESC LIMIT 1;'    
    result = execute_select_fetchone(conn, sql)

    DB_LOGGER.debug('EXIT')
    return result


def select_node_by_name(conn, node_name):
    DB_LOGGER.debug('ENTER')

    sql = 'SELECT id FROM nodes WHERE name = ?'
    tokens = (node_name,) 
    result = execute_select_fetchone(conn, sql, tokens)

    DB_LOGGER.debug('EXIT')
    return result


#####################################################################
#Select Statements for sensors                                     
#####################################################################
def select_all_sensors(conn):
    DB_LOGGER.debug('ENTER')

    sql = 'SELECT * FROM sensors, nodes'
    result = execute_select_fetchall(conn, sql)
    
    DB_LOGGER.debug('EXIT')
    return result


def select_all_node_sensors(conn, node_name):
    DB_LOGGER.debug('ENTER')

    sql = 'SELECT * FROM sensors WHERE node_id IN(SELECT id FROM nodes WHERE name = ?)'
    tokens = (node_name,)
    result = execute_select_fetchall(conn, sql, tokens)

    DB_LOGGER.debug('EXIT')
    return result

def select_all_location_sensors(conn, sensor_location):
    DB_LOGGER.debug('ENTER')

    sql = 'SELECT * FROM sensors WHERE node_id IN(SELECT id FROM nodes WHERE location = ?)'
    tokens = (sensor_location,)
    result = execute_select_fetchall(conn, sql, tokens)

    DB_LOGGER.debug('EXIT')
    return result


def select_sensor_by_name(conn, sensor_name):
    DB_LOGGER.debug('ENTER')

    sql = 'SELECT id FROM sensors WHERE name = ?'
    tokens = (sensor_name,)
    result = execute_select_fetchone(conn, sql, tokens)
    
    DB_LOGGER.debug('EXIT')
    return result

def select_sensor_by_name_and_node(conn, sensor_name, node_name):
    DB_LOGGER.debug('ENTER')

    sql = 'SELECT id FROM sensors WHERE name = ? AND node_id IN (SELECT id FROM nodes WHERE name = ?)'
    tokens = (sensor_name, node_name,)
    result = execute_select_fetchone(conn, sql, tokens)

    DB_LOGGER.debug('EXIT')
    return result


#####################################################################
#Select Statements for readings                                     
#####################################################################
def select_readings_by_sensor(conn, sensor_name):
    DB_LOGGER.debug('ENTER')

    sql = 'SELECT data, timestamp FROM readings WHERE sensor_id IN (SELECT id FROM sensors WHERE name = ?)'
    tokens = (sensor_name,)
    result = execute_select_fetchall(conn, sql, tokens)

    DB_LOGGER.debug('EXIT')
    return result


def select_readings_by_sensor_and_node(conn, sensor_name, node_name):
    DB_LOGGER.debug('ENTER')
    
    sql = 'SELECT data, timestamp FROM readings WHERE sensor_id IN\
            (SELECT id FROM sensors WHERE name = ? AND node_id IN\
                (SELECT id FROM nodes WHERE name = ?))'
    tokens = (sensor_name, node_name,)
    result = execute_select_fetchall(conn, sql, tokens)

    DB_LOGGER.debug('EXIT')
    return result

def select_latest_reading_by_sensor_and_node(conn, node_name, sensor_name):
    DB_LOGGER.debug('ENTER')
    
    sql = 'SELECT data, timestamp, type FROM readings WHERE sensor_id IN\
            (SELECT id FROM sensors WHERE name = ? AND node_id IN\
                (SELECT id FROM nodes WHERE name = ?)) ORDER BY timestamp DESC LIMIT 1'
    tokens = (sensor_name, node_name,)
    result = execute_select_fetchall(conn, sql, tokens)

    DB_LOGGER.debug('EXIT')
    return result


def select_readings_by_type(conn, reading_type):
    DB_LOGGER.debug('ENTER')

    sql = 'SELECT data, timestamp FROM readings WHERE type = ?'
    tokens = (reading_type,)
    result = execute_select_fetchall(conn, sql, tokens)

    DB_LOGGER.debug('EXIT')
    return result

def select_readings_by_node_location(conn, node_location):
    DB_LOGGER.debug('ENTER')

    sql = 'SELECT data, timestamp FROM readings WHERE sensor_id IN\
            (SELECT id FROM sensors WHERE node_id IN\
                (SELECT id FROM nodes WHERE location = ?))'
    tokens = (node_location,)
    result = execute_select_fetchall(conn, sql, tokens)

    DB_LOGGER.debug('EXIT')
    return result


#CRUD
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
                    name text NOT NULL UNIQUE ,
                    location text,
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
                type text, 
                data float, 
                timestamp DateTime,
                sensor_id integer NOT NULL,
                    FOREIGN KEY (sensor_id) REFERENCES sensors(id) ON DELETE RESTRICT ON UPDATE CASCADE
                );
            '''
        )
        create_table(
            conn,
            '''CREATE TABLE IF NOT EXISTS users(
                    id integer PRIMARY KEY, 
                    name text NOT NULL UNIQUE,
                    password text
                );
            '''
        )
        conn.commit()
        DB_LOGGER.debug('EXIT')
        return True
    except:
        DB_LOGGER.error('\n=> Failed to create all tables, see create_table() calls for more information')
        DB_LOGGER.debug('EXIT')
        return False

'''
if __name__ == '__main__':

    DB_CONNECTION = create_connection(':memory:')
    print(is_empty_nodes(DB_CONNECTION))
    if sys.argv[1]:
        create_node_tables(DB_CONNECTION)

        insert_node(DB_CONNECTION, ('NODE#1', 'Inhouse'))
        insert_sensor(DB_CONNECTION, ('DHT11', select_node_by_name(DB_CONNECTION, 'NODE#1')['id']))
        insert_reading(
            DB_CONNECTION, 
            (
                "temperature", 
                12.34, 
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
                select_sensor_by_name_and_node(DB_CONNECTION, 'DHT11', 'NODE#1')['id']
            )
        )
    [print(x) for x in select_readings_by_sensor(DB_CONNECTION, 'DHT11')]
    [print(x) for x in select_readings_by_sensor_and_node(DB_CONNECTION, 'DHT11', 'NODE#1')]
    [print(x) for x in select_readings_by_node_location(DB_CONNECTION, 'Inhouse')]
    print(is_empty_nodes(DB_CONNECTION))
'''