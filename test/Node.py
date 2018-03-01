import json
import threading
import requests
import sys
import logging
import SensorSimulator
import RestfulNode
import time

#Add errorhandling to all functions which have a request to the server
#Where they could get a invalid packet structure response

node_config = {
   'NODE_NAME': '',
   'LOCATION': ''
}

def Try_File_Open(filepath):
    try: 
        open(filepath)
    except IOError:
        print("File does not appear to exist {}".format(filepath))
        sys.exit(1)

def Read_Node_Config():
    Try_File_Open("../shared/node.conf")
    with open("../shared/node.conf", "r") as conf_file:
        for element in conf_file.readlines():
            key, value = element.strip('\n').split(":")
            node_config[key] = value
    conf_file.close()

def Write_Node_Config(new_key, new_value):
    Try_File_Open("../shared/node.conf")
    with open("../shared/node.conf", "w") as conf_file:
        for key, value in node_config.iteritems():
            if new_key == key:
                conf_file.write(key + ':' + new_value + '\n')
            else:
                conf_file.write(key + ':' + value + '\n')
    conf_file.close()


def Start_Threads():
    restThread = threading.Thread(target = RestfulNode.Run_Rest)
    DHT11Thread = threading.Thread(target = SensorSimulator.DHT11DataStream)
    
    restThread.start()
    DHT11Thread.start()


def __init():
    Read_Node_Config()
    url = "http://127.0.0.1:5000/init"
    while True:
        try:
            response = requests.post(url, json = node_config)
            response.raise_for_status()
            #node_logger.info('Server Init Complete')
            response_data = json.loads(response.content)
            print(response_data)
            if (response_data['NODE_NAME'] !=  node_config['NODE_NAME']):
                Write_Node_Config('NODE_NAME', response_data['NODE_NAME'])
            else:
                pass
            break
        except requests.exceptions.ConnectionError as err:
            #node_logger.error('{} {}'.format(url, err))
            #node_logger.info('Retry connection {}'.format(url))
            time.sleep(10)
            continue
            #sys.exit(1)
    Start_Threads()   
    
__init()