#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask
import time
import atexit
from influxdb import InfluxDBClient
from flask import render_template
from apscheduler.schedulers.background import BackgroundScheduler

# pip3 install flask influxdb apschedulerpip

app = Flask(__name__)

##########

client = InfluxDBClient(host='api.smoglist.pl', port=8086, username='username', password='password',
                        database='database')


##########

def getListOfSOFTWAREVERSION(deviceName):
    global SWidx
    query = 'SELECT LAST("SOFTWAREVERSION") FROM "%s"' % (deviceName)
    result = str(client.query(query))
    result = result[result.find('['):result.rfind(']') + 1]
    result = result[result.find('\'last\': \'') + len("\'last\': \'"):result.find(' build ')]
    SWidx.append(result)


def getListOfPMSENSORVERSION(deviceName):
    global PMSWSensoridx
    query = 'SELECT LAST("PMSENSORVERSION") FROM "%s"' % (deviceName)
    result = str(client.query(query))
    result = result[result.find('\'last\': \'') + len("\'last\': \'"):result.rfind('\'}')]
    if "'time'" not in result:
        PMSWSensoridx.append(result)
    else:
        result = result[:result.rfind('\', \'time\': \'')]
        PMSWSensoridx.append(result)


def getListOfHARDWAREVERSION(deviceName):
    global HWidx
    query = 'SELECT LAST("HARDWAREVERSION") FROM "%s"' % (deviceName)
    result = str(client.query(query))
    result = result[result.find('\'last\': \'') + len("\'last\': \'"):result.rfind('\'}')]
    if "'time'" not in result:
        HWidx.append(result)
    else:
        result = result[:result.rfind('\', \'time\': \'')]
        HWidx.append(result)


def getListOfLUFTDATEN_ON(deviceName):
    global Luftdatenidx
    query = 'SELECT LAST("LUFTDATEN_ON") FROM "%s"' % (deviceName)
    result = str(client.query(query))
    result = result[result.find('\'last\': ') + len("\'last\': "):result.rfind('}]}')]
    if "'time'" not in result:
        Luftdatenidx.append(result)
    else:
        result = result[:result.find('\'time\': \'')-2]
        Luftdatenidx.append(result)


def getListOfAIRMONITOR_ON(deviceName):
    global AirMonitoridx
    query = 'SELECT LAST("AIRMONITOR_ON") FROM "%s"' % (deviceName)
    result = str(client.query(query))
    result = result[result.find('\'last\': ') + len("\'last\': "):result.rfind('}]}')]
    if "'time'" not in result:
        AirMonitoridx.append(result)
    else:
        result = result[:result.find('\'time\': \'')-2]
        AirMonitoridx.append(result)


def getListOfAIRMONITOR_GRAPH_ON(deviceName):
    global AirMonitorGraphidx
    query = 'SELECT LAST("AIRMONITOR_GRAPH_ON") FROM "%s"' % (deviceName)
    result = str(client.query(query))
    result = result[result.find('\'last\': ') + len("\'last\': "):result.rfind('}]}')]
    if "'time'" not in result:
        AirMonitorGraphidx.append(result)
    else:
        result = result[:result.find('\'time\': \'')-2]
        AirMonitorGraphidx.append(result)


def getListOfTHINGSPEAK_ON(deviceName):
    global ThingSpeakidx
    query = 'SELECT LAST("THINGSPEAK_ON") FROM "%s"' % (deviceName)
    result = str(client.query(query))
    result = result[result.find('\'last\': ') + len("\'last\': "):result.rfind('}]}')]
    if "'time'" not in result:
        ThingSpeakidx.append(result)
    else:
        result = result[:result.find('\'time\': \'')-2]
        ThingSpeakidx.append(result)


def getListOfTHINGSPEAK_GRAPH_ON(deviceName):
    global ThingSpeakGraphidx
    query = 'SELECT LAST("THINGSPEAK_GRAPH_ON") FROM "%s"' % (deviceName)
    result = str(client.query(query))
    result = result[result.find('\'last\': ') + len("\'last\': "):result.rfind('}]}')]
    if "'time'" not in result:
        ThingSpeakGraphidx.append(result)
    else:
        result = result[:result.find('\'time\': \'')-2]
        ThingSpeakGraphidx.append(result)


def getListOfINFLUXDB_ON(deviceName):
    global InfluxDBidx
    query = 'SELECT LAST("INFLUXDB_ON") FROM "%s"' % (deviceName)
    result = str(client.query(query))
    result = result[result.find('\'last\': ') + len("\'last\': "):result.rfind('}]}')]
    if "'time'" not in result:
        InfluxDBidx.append(result)
    else:
        result = result[:result.find('\'time\': \'')-2]
        InfluxDBidx.append(result)


def getListOfMQTT_ON(deviceName):
    global MQTTidx
    query = 'SELECT LAST("MQTT_ON") FROM "%s"' % (deviceName)
    result = str(client.query(query))
    result = result[result.find('\'last\': ') + len("\'last\': "):result.rfind('}]}')]
    if "'time'" not in result:
        MQTTidx.append(result)
    else:
        result = result[:result.find('\'time\': \'')-2]
        MQTTidx.append(result)


def getListOfDEEPSLEEP_ON(deviceName):
    global DeepSleepidx
    query = 'SELECT LAST("DEEPSLEEP_ON") FROM "%s"' % (deviceName)
    result = str(client.query(query))
    result = result[result.find('\'last\': ') + len("\'last\': "):result.rfind('}]}')]
    if "'time'" not in result:
        DeepSleepidx.append(result)
    else:
        result = result[:result.find('\'time\': \'')-2]
        DeepSleepidx.append(result)


def getListOfAUTOUPDATE_ON(deviceName):
    global AutoUpdateidx
    query = 'SELECT LAST("AUTOUPDATE_ON") FROM "%s"' % (deviceName)
    result = str(client.query(query))
    result = result[result.find('\'last\': ') + len("\'last\': "):result.rfind('}]}')]
    if "'time'" not in result:
        AutoUpdateidx.append(result)
    else:
        result = result[:result.find('\'time\': \'')-2]
        AutoUpdateidx.append(result)


def getListOfCalibrationMethods(deviceName):
    global CalibrationMethodsidx
    query = 'SELECT LAST("MODEL") FROM "%s"' % (deviceName)
    result = str(client.query(query))
    result = result[result.find('\'last\': \'') + len("\'last\': \'"):result.rfind('\'}]}')]
    if "'time'" not in result:
        CalibrationMethodsidx.append(result)
    else:
        result = result[:result.rfind('\', \'time\': \'')]
        CalibrationMethodsidx.append(result)


def getListOfDUST_MODEL(deviceName):
    global PMSensoridx
    query = 'SELECT LAST("DUST_MODEL") FROM "%s"' % (deviceName)
    result = str(client.query(query))
    result = result[result.find('\'last\': \'') + len("\'last\': \'"):result.rfind('\'}]}')]
    if "'time'" not in result:
        PMSensoridx.append(result)
    else:
        result = result[:result.rfind('\', \'time\': \'')]
        PMSensoridx.append(result)


def getListOfTHP_MODEL(deviceName):
    global THPSensoridx
    query = 'SELECT LAST("THP_MODEL") FROM "%s"' % (deviceName)
    result = str(client.query(query))
    result = result[result.find('\'last\': \'') + len("\'last\': \'"):result.rfind('\'}]}')]
    if "'time'" not in result:
        THPSensoridx.append(result)
    else:
        result = result[:result.rfind('\', \'time\': \'')]
        THPSensoridx.append(result)


def getListOfFREQUENTMEASUREMENT(deviceName):
    global FrequentMesurementONidx
    query = 'SELECT LAST("FREQUENTMEASUREMENT") FROM "%s"' % (deviceName)
    result = str(client.query(query))
    result = result[result.find('\'last\': ') + len("\'last\': "):result.rfind('}]}')]
    if "'time'" not in result:
        FrequentMesurementONidx.append(result)
    else:
        result = result[:result.find('\'time\': \'')-2]
        FrequentMesurementONidx.append(result)


def getListOfDISPLAY_PM1(deviceName):
    global DisplayPM1idx
    query = 'SELECT LAST("DISPLAY_PM1") FROM "%s"' % (deviceName)
    result = str(client.query(query))
    result = result[result.find('\'last\': ') + len("\'last\': "):result.rfind('}]}')]
    if "'time'" not in result:
        DisplayPM1idx.append(result)
    else:
        result = result[:result.find('\'time\': \'')-2]
        DisplayPM1idx.append(result)


def getListOfDUST_TIME(deviceName):
    global DustTimeidx
    query = 'SELECT LAST("DUST_TIME") FROM "%s"' % (deviceName)
    result = str(client.query(query))
    result = result[result.find('\'last\': ') + len("\'last\': "):result.rfind('}]}')]
    if "'time'" not in result:
        DustTimeidx.append(result)
    else:
        result = result[:result.find('\'time\': \'')-2]
        DustTimeidx.append(result)


def getListOfNUMBEROFMEASUREMENTS(deviceName):
    global NumberOfMeasurementsidx
    query = 'SELECT LAST("NUMBEROFMEASUREMENTS") FROM "%s"' % (deviceName)
    result = str(client.query(query))
    result = result[result.find('\'last\': ') + len("\'last\': "):result.rfind('}]}')]
    if "'time'" not in result:
        NumberOfMeasurementsidx.append(result)
    else:
        result = result[:result.find('\'time\': \'')-2]
        NumberOfMeasurementsidx.append(result)


def getListOfSENDING_FREQUENCY(deviceName):
    global SendingFrequencyidx
    query = 'SELECT LAST("SENDING_FREQUENCY") FROM "%s"' % (deviceName)
    result = str(client.query(query))
    result = result[result.find('\'last\': ') + len("\'last\': "):result.rfind('}]}')]
    if "'time'" not in result:
        SendingFrequencyidx.append(result)
    else:
        result = result[:result.find('\'time\': \'')-2]
        SendingFrequencyidx.append(result)


def getListOfSENDING_DB_FREQUENCY(deviceName):
    global SendingDBFrequencyidx
    query = 'SELECT LAST("SENDING_DB_FREQUENCY") FROM "%s"' % (deviceName)
    result = str(client.query(query))
    result = result[result.find('\'last\': ') + len("\'last\': "):result.rfind('}]}')]
    if "'time'" not in result:
        SendingDBFrequencyidx.append(result)
    else:
        result = result[:result.find('\'time\': \'')-2]
        SendingDBFrequencyidx.append(result)


##########

def most_frequent(List):
    return max(set(List), key=List.count)


##########

def callForData():
    global devicesList, devicesNumber, updateTime
    global SWidx, HWidx, PMSWSensoridx, PMSensoridx, THPSensoridx, Luftdatenidx, AirMonitoridx, ThingSpeakidx, InfluxDBidx, MQTTidx, DeepSleepidx, AutoUpdateidx, AirMonitorGraphidx, ThingSpeakGraphidx, CalibrationMethodsidx, FrequentMesurementONidx, DisplayPM1idx, DustTimeidx, NumberOfMeasurementsidx, SendingFrequencyidx, SendingDBFrequencyidx

    devicesList = []
    devicesNumber = 0

    (SWidx, HWidx, PMSWSensoridx, PMSensoridx, THPSensoridx, Luftdatenidx, AirMonitoridx, ThingSpeakidx, InfluxDBidx,
     MQTTidx, DeepSleepidx, AutoUpdateidx, AirMonitorGraphidx, ThingSpeakGraphidx, CalibrationMethodsidx,
     FrequentMesurementONidx, DisplayPM1idx, DustTimeidx, NumberOfMeasurementsidx, SendingFrequencyidx,
     SendingDBFrequencyidx) = ([] for i in range(21))

    devicesList = client.get_list_measurements()
    devicesNumber = len(devicesList)
    devicesList = str(devicesList)
    devicesList = devicesList[devicesList.find(': \'') + 3:devicesList.rfind('\'}')]
    devicesList = devicesList.split("\'}, {\'name\': \'")

    for i in range(devicesNumber):
        getListOfSOFTWAREVERSION(devicesList[i])
        getListOfPMSENSORVERSION(devicesList[i])
        getListOfHARDWAREVERSION(devicesList[i])

        getListOfLUFTDATEN_ON(devicesList[i])
        getListOfAIRMONITOR_ON(devicesList[i])
        getListOfAIRMONITOR_GRAPH_ON(devicesList[i])
        getListOfTHINGSPEAK_ON(devicesList[i])
        getListOfTHINGSPEAK_GRAPH_ON(devicesList[i])
        getListOfINFLUXDB_ON(devicesList[i])
        getListOfMQTT_ON(devicesList[i])
        getListOfDEEPSLEEP_ON(devicesList[i])
        getListOfAUTOUPDATE_ON(devicesList[i])

        getListOfCalibrationMethods(devicesList[i])
        getListOfDUST_MODEL(devicesList[i])
        getListOfTHP_MODEL(devicesList[i])

        getListOfFREQUENTMEASUREMENT(devicesList[i])
        getListOfDISPLAY_PM1(devicesList[i])

        getListOfDUST_TIME(devicesList[i])
        getListOfNUMBEROFMEASUREMENTS(devicesList[i])
        getListOfSENDING_FREQUENCY(devicesList[i])
        getListOfSENDING_DB_FREQUENCY(devicesList[i])
    client.close()
    ts = time.localtime()
    updateTime = time.strftime("%d/%m/%Y %X %Z", ts)
    print("New Data!")

##########

devicesList = []
updateTime = ""
devicesNumber = 0

(SWidx, HWidx, PMSWSensoridx, PMSensoridx, THPSensoridx, Luftdatenidx, AirMonitoridx, ThingSpeakidx, InfluxDBidx,
 MQTTidx, DeepSleepidx, AutoUpdateidx, AirMonitorGraphidx, ThingSpeakGraphidx, CalibrationMethodsidx,
 FrequentMesurementONidx, DisplayPM1idx, DustTimeidx, NumberOfMeasurementsidx, SendingFrequencyidx,
 SendingDBFrequencyidx) = ([] for i in range(21))

callForData()

scheduler = BackgroundScheduler()
scheduler.add_job(func=callForData, trigger="interval", minutes=5)
scheduler.start()


##########

@app.route('/')
def index():
    global SWidx, HWidx, PMSWSensoridx, PMSensoridx, THPSensoridx, Luftdatenidx, AirMonitoridx, ThingSpeakidx, InfluxDBidx, MQTTidx, DeepSleepidx, AutoUpdateidx, AirMonitorGraphidx, ThingSpeakGraphidx, CalibrationMethodsidx, FrequentMesurementONidx, DisplayPM1idx, DustTimeidx, NumberOfMeasurementsidx, SendingFrequencyidx, SendingDBFrequencyidx
    return render_template('index.html', devicesNumber=devicesNumber, luftdatenEnableNumber=Luftdatenidx.count("True"),
                           airmonitorEnableNumber=AirMonitoridx.count("True"),
                           airmonitorGraphEnableNumber=AirMonitorGraphidx.count("True"),
                           thingspeakEnableNumber=ThingSpeakidx.count("True"),
                           thingspeakGraphEnableNumber=ThingSpeakGraphidx.count("True"),
                           influxdbEnableNumber=InfluxDBidx.count("True"), mqttEnableNumber=MQTTidx.count("True"),
                           deepsleepEnableNumber=DeepSleepidx.count("True"),
                           autoupdateEnableNumber=AutoUpdateidx.count("True"),
                           frequentmesurementEnableNumber=FrequentMesurementONidx.count("True"),
                           displaypm1EnableNumber=DisplayPM1idx.count("True"),
                           mostcommonDustMeasurements=most_frequent(DustTimeidx),
                           mostcommonDustMeasurementsNumber=DustTimeidx.count(most_frequent(DustTimeidx)),
                           mostcommonPMaveraging=most_frequent(NumberOfMeasurementsidx),
                           mostcommonPMaveragingNumber=NumberOfMeasurementsidx.count(
                               most_frequent(NumberOfMeasurementsidx)),
                           mostcommonSendingFrequency=most_frequent(SendingFrequencyidx),
                           mostcommonSendingFrequencyNumber=SendingFrequencyidx.count(
                               most_frequent(SendingFrequencyidx)),
                           mostcommonSendingDBFrequency=most_frequent(SendingDBFrequencyidx),
                           mostcommonSendingDBFrequencyNumber=SendingDBFrequencyidx.count(
                               most_frequent(SendingDBFrequencyidx)), lastupdateTime=updateTime,
                           mostcommonSW=most_frequent(SWidx), mostcommonSWNumber=SWidx.count(most_frequent(SWidx)),
                           mostcommonPMSW=most_frequent(PMSWSensoridx),
                           mostcommonPMSWNumber=PMSWSensoridx.count(most_frequent(PMSWSensoridx)),
                           mostcommonHW=most_frequent(HWidx), mostcommonHWNumber=HWidx.count(most_frequent(HWidx)),
                           mostcommonPMSensor=most_frequent(PMSensoridx),
                           mostcommonPMSensorNumber=PMSensoridx.count(most_frequent(PMSensoridx)),
                           mostcommonTHPSensor=most_frequent(THPSensoridx),
                           mostcommonTHPSensorNumber=THPSensoridx.count(most_frequent(THPSensoridx)))


@app.route('/measurements')
def measurements():
    global updateTime
    return render_template('measurements.html', lastupdateTime=updateTime)


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080, passthrough_errors=True, threaded=True)
    atexit.register(lambda: scheduler.shutdown())
