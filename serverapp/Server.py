import DummyServer
import sys
import threading
#import dbfunctions something

log = []

server_config = {
    'SERVER_IP': '',
    'SERVER_PORT': ''
}

"""

def post to db

def fetch from db

"""
def Populate_NODE_ID_Log():
    with open('NODEID.log', 'w') as nodeLog:
        for x in range(10): 
            nodeLog.write('NODE#' + str(x) + '\n')
    nodeLog.close()


def Read_Node_Log():
    with open('NODEID.log', 'r') as nodeLog:
        for line in nodeLog:
            line.strip('\n')
            log.append(line)
    nodeLog.close()

def Write_Node_Log(newID):
    with open('NODEID.log', 'a') as nodeLog:
        nodeLog.write(newID)
    nodeLog.close()

def Read_Server_Config():
    with open('./storage/server.conf') as conf_file:
        for element in conf_file.readlines():
            key, value = element.split(':')
            server_config[key] = value       
    conf_file.close()


    
def Get_Node_ID():

    name, num = log[len(log) - 1].split('#')
    newNodeID = name + '#' + str(int(num) + 1) 
    Write_Node_Log(newNodeID)

    return newNodeID
