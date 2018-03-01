from flask import Flask, jsonify, make_response, request
from SensorSimulator import *
from datetime import datetime
import threading
import requests
import sys

#app = Flask(__name__)

sensorData = {
        'NODE_NAME': '',
        'SENSOR_NAME': '',
        'TYPE': '',
        'TIMESTAMP':'',
        'DATA': ''
    }

def tryFileOpen(filepath):
    try: 
        open(filepath)
    except IOError:
        print "Error: file does not appear to exist {}.".format(filepath)
        sys.exit(1)

def errorLog(url, err):
    tryFileOpen("./storage/log/errorLog.log")
    logfile = open("./storage/log/errorLog.log", "a")
    logfile.write("Failed to connect to {0}: {1}\n".format(str(url), str(err)))
    logfile.close()

def postTemp(addr): 
    sensorData['TYPE'] = "Temperature"
    sensorData['SENSOR_NAME'] = 'DHT12'
    url = addr + '/Temp'
    while True:
        try:
            sensorData['DATA'] = getTemperature()
            sensorData['timestamp'] = str(datetime.now())
            requests.post(url, json=sensorData)
        except requests.exceptions.ConnectionError as err:
            errorLog(url, err)
            print 'Retry'
            sleep(10)
            continue
        sleep(5)
'''
@app.route('/Temp', methods=['GET'])
def getTemp(): 
    sensorData['data'] = getTemperature()
    sensorData['dataType'] = "Temperature"
    sensorData['timestamp'] = str(datetime.now())
    return jsonify(sensorData)


@app.route('/Humidity', methods=['GET'])
def getHumi(): 
    sensorData['data'] = getHumidity()
    sensorData['dataType'] = "Humidity"
    sensorData['timestamp'] = str(datetime.now())
    return jsonify(sensorData)

@app.route('/Test', methods=['GET'])
def getTest(): 
    return jsonify(sensorData)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
'''
def Run_Rest():
    sensorData['NODE_NAME'] = 'Node#1'
    server_addr = 'http://127.0.0.1:5000'
    #app.run(port = 5005)    
    postTemp(server_addr)
