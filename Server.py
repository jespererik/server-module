from Server_Debug_functions import *
from DummyServer import * 

from threading import Thread
config = {}
registeredNodes = []

'''
Read the config file
parse lines and put into config variable
'''
def __readServerConfig():
    DebugPrint("string", "", "Enter => __readServerConfig()")
    with open("SERVER_CONFIG.txt", "r") as serverConfig:
        for line in serverConfig:
            key, value = line.split(":")
            config[key] = value
    serverConfig.close()
    DebugPrint("dict", "config", config)

    DebugPrint("string", "", "exit => __readServerConfig()")

def __readNodeLog():
    DebugPrint("string", "", "Enter => __readNodeLog()")
    with open("NODE_LOG.txt", "r") as nodeLog:
        for line in nodeLog:
            registeredNodes.append(line)
    nodeLog.close()
    DebugPrint('list', 'registeredNodes', registeredNodes)

    DebugPrint("string", "", "Exit => __readNodeLog()")
            

''' 
get the last registered node
split into id and name
increment id, concatentate strings and new id
'''
def getNodeID():
    DebugPrint("string", "", "Enter => getNodeID()")
    name, num = registeredNodes.index(len(registeredNodes)).split("#")
    DebugPrint("varstring", "latestNodeID", (name + num))
    newNodeID = name + str(num + 1)
    DebugPrint("varstring", "newNodeID", newNodeID)

    DebugPrint("string", "", "Exit => getNodeID()")
    return newNodeID

def __init():
    ''' Read config and log'''
    __readServerConfig()
    __readNodeLog()

    ''' fork rest API '''
    serverREST = Thread(target = runServerREST)
    serverREST.start()

if __name__ == "__main__":
    __init()


        
