from flask import Flask
from datetime import datetime
from sqlalchemy import Column, Date, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database

Base = declarative_base()


""" Tabel Definitons """
class DataEntry(Base):
    __tablename__   = 'DataEntry'
    id              = Column(Integer, primary_key = True)
    nodeID          = Column(String(20), nullable = False)
    sensorID        = Column(String(20), nullable = False)
    readingType     = Column(String(20), nullable = False)
    timestamp       = Column(DateTime, nullable = False)
    data            = Column(Float, nullable = False)


""" If this file is run separetly we want """
if __name__ == '__main__':
    engine = create_engine('sqlite:///database/SensorData.db', echo=True)

    #If we can't find a the .db file, we create one at the given path
    if not database_exists(engine.url): create_database(engine.url) 
    
    Base.metadata.create_all(engine)