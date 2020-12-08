#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask
from flask import request
import time
import logging
import datetime
from influxdb import InfluxDBClient

# logging.basicConfig(filename='parsingJSON.log', filemode='w', level=logging.DEBUG)
# logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %H:%M:%S')

app = Flask(__name__)


def saveToInfluxDB(receivedData):
    client = InfluxDBClient(host='api.smoglist.pl', port=8086, username='username', password='password', database='database')
    client.write_points([receivedData])
    client.close()

@app.route('/postjson', methods=['POST'])
def postJsonHandler():
    try:
        content = request.get_json()
        # print (content)
        # logging.debug(content)
        receivedData = {}
        receivedData['measurement'] = str(content['CHIPID'])
        receivedData['timestamp'] = str(datetime.datetime.utcnow().isoformat())
        receivedData["fields"] = {}  # this is required by python
        receivedData["fields"] = {
            "SOFTWAREVERSION": str(content['SOFTWAREVERSION']),
            "HARDWAREVERSION": str(content['HARDWAREVERSION']),
            "PMSENSORVERSION": str(content['PMSENSORVERSION']),
            "FREQUENTMEASUREMENT": bool(content['FREQUENTMEASUREMENT']),
            "DISPLAY_PM1": bool(content['DISPLAY_PM1']),
            "DUST_TIME": int(content['DUST_TIME']),
            "NUMBEROFMEASUREMENTS": int(content['NUMBEROFMEASUREMENTS']),
            "SENDING_FREQUENCY": int(content['SENDING_FREQUENCY']),
            "SENDING_DB_FREQUENCY": int(content['SENDING_DB_FREQUENCY']),
            "LUFTDATEN_ON": bool(content['LUFTDATEN_ON']),
            "AIRMONITOR_ON": bool(content['AIRMONITOR_ON']),
            "AIRMONITOR_GRAPH_ON": bool(content['AIRMONITOR_GRAPH_ON']),
            "THINGSPEAK_ON": bool(content['THINGSPEAK_ON']),
            "THINGSPEAK_GRAPH_ON": bool(content['THINGSPEAK_GRAPH_ON']),
            "INFLUXDB_ON": bool(content['INFLUXDB_ON']),
            "MQTT_ON": bool(content['MQTT_ON']),
            "DEEPSLEEP_ON": bool(content['DEEPSLEEP_ON']),
            "AUTOUPDATE_ON": bool(content['AUTOUPDATE_ON']),
            "MODEL": str(content['MODEL']),
            "LATITUDE": str(content['LATITUDE']),
            "LONGITUDE": str(content['LONGITUDE']),
            "MYALTITUDE": int(content['MYALTITUDE']),
            "DUST_MODEL": str(content['DUST_MODEL']),
            "PM1": float(content['PM1']),
            "PM25": float(content['PM25']),
            "PM4": float(content['PM4']),
            "PM10": float(content['PM10']),
            "THP_MODEL": str(content['THP_MODEL']),
            "Temperature": float(content['Temperature']),
            "Humidity": float(content['Humidity']),
            "Pressure": float(content['Pressure'])
        }
        # print (receivedData)
        # logging.debug(receivedData)
        # logging.debug('\n')
        saveToInfluxDB(receivedData)
        content.clear()
        receivedData.clear()
    except:
        # logging.debug('ERROR!\n')
        print('ERROR!')
    return 'data received!'

app.run(host='0.0.0.0', port=8090)
