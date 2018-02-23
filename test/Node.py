import json
import threading
import requests
import sys
import logging
import SensorSimulator
import RestfulNode

node_logger = logging.getLogger(__name__)
logging.basicConfig(
    filename = 'storage/log/' + __name__ + ".log"
)

node_config = {
   'NODE_ID': '',
   'SERVER_IP': '',
   'SERVER_PORT': ''
}

def Try_File_Open(filepath):
    try: 
        open(filepath)
    except IOError:
        print("File does not appear to exist {}".format(filepath))
        sys.exit(1)

def Read_Node_Config():
    Try_File_Open("./storage/node.conf")
    with open("./storage/node.conf", "r") as conf_file:
        for element in conf_file.readlines():
            key, value = element.strip('\n').split(":")
            node_config[key] = value
    conf_file.close()
    node_logger.info('Read config: {}'.format(node_config))

def Write_Node_Config(new_key, new_value):
    Try_File_Open("./storage/node.conf")
    with open("./storage/node.conf", "w") as conf_file:
        for key, value in zip(node_config.keys(), node_config.values()):
            if new_key == key:
                conf_file.write(key + ':' + new_value + '\n')
                node_logger.info('new value in node.conf => key: {}, value: {}'.format(key, new_value)) 
            else:
                conf_file.write(key + ':' + value + '\n')
                node_logger.info('wrote value in node.conf => key: {}, value: {}'.format(key, value))
    conf_file.close()


def Start_Threads():
    restThread = threading.Thread(target = RestfulNode.Run_Rest, args = node_config.values())
    DHT11Thread = threading.Thread(target = SensorSimulator.DHT11DataStream)
    
    restThread.start()
    DHT11Thread.start()


def __init():
    Read_Node_Config()
    url = "http://" + node_config['SERVER_IP'] + ":" + node_config['SERVER_PORT'] + "/init"
    while True:
        try:
            response = requests.post(url, json = node_config)
            response.raise_for_status()
            node_logger.info('Server Init Complete')
            responseData = json.loads(response.content)
            if (responseData['NODE_ID'] !=  node_config['NODE_ID']):
                Write_Node_Config('NODE_ID', responseData['NODE_ID'])
            else:
                pass
            break
        except requests.exceptions.ConnectionError as err:
            node_logger.error('{} {}'.format(url, err))
            node_logger.info('Retry connection {}'.format(url))
            sleep(10)
            continue
            #sys.exit(1)
    Start_Threads()   
    
__init()