import DummyServer
import sys

log = []

def pList(variable):
    print('*******************************')
    for element in variable:
        print element
    print('*******************************')

def populatelog():
    with open('NODEID.log', 'w') as nodeLog:
        for x in range(10): 
            nodeLog.write('NODE#' + str(x) + '\n')
    nodeLog.close()


def ReadNodeLog():
    with open('NODEID.log', 'r') as nodeLog:
        for line in nodeLog:
            line.strip('\n')
            log.append(line)
    nodeLog.close()

def WriteNodeLog(newID):
    with open('NODEID.log', 'a') as nodeLog:
        nodeLog.write(newID)
    nodeLog.close()
    
 

def getNodeID():

    name, num = log[len(log) - 1].split('#')
    newNodeID = name + '#' + str(int(num) + 1) 
    WriteNodeLog(newNodeID)

    return newNodeID


if __name__ == "__main__":
    populatelog()
    ReadNodeLog()
    #1
    pList(log)
    print getNodeID()
    
    #2
    log = []
    pList(log)
    ReadNodeLog()

    #3
    pList(log)