""" Operates towards the database without relations """

""" Imports """
from sqlalchemy         import create_engine, MetaData, Table
from ReadingDB          import *
from sqlalchemy.orm     import *
from datetime           import datetime, timedelta
from random             import randint
from time               import sleep
""" Establish Connection to the database """
engine      = create_engine('sqlite:///database/SensorData.db')
connection  = engine.connect()

""" Create a session object and bind it """
initSession = sessionmaker(bind = engine) #Create session object
session     = initSession() #Bind session object

DEBUG = True

""" Auxiallary Functions """
#Returns the timestamp closests to the input <timestamp> from the input <timestamps>
def _ClosestTimestamp(timestamp, timestamps):
    return min(timestamps, key=lambda x:timedelta(x-timestamp))

def postDataEntry(nID, sID, rType, timestmp, idata):
    session.add(DataEntry(
        nodeID      = nID,
        sensorID    = sID,
        readingType = rType,
        timestamp   = timestmp,
        data        = idata
    ))
    session.commit()

def getDataEntries(nodeID, sensorID, readingType):
    return session.query(DataEntry).filter(DataEntry.nodeID == nodeID and DataEntry.sensorID == sensorID and DataEntry.readingType == readingType).all().

def 



if __name__ == '__main__':
    '''
    for x in range (20):
        postDataEntry(
            'nodeX',
            'sensorX',
            'temperature',
            datetime.now(),
            float(randint(-15, 40))
        )
        postDataEntry(
            'nodeX',
            'sensorX',
            'humidity',
            datetime.now(),
            float(randint(0, 100))
        )
        sleep(1)
    '''
    for entry in getDataEntry('nodeX', 'sensorY', 'temperature'):
        print entry
    for entry in getDataEntry('nodeX', 'sensorY', 'humidity'):
        print entry


#postSensorReading('testNode#1', 'testSesnor#1', datetime.now(), 24.235)


