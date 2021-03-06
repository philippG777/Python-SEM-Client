# coding: utf8
import requests

__version__ = "0.1"


class Device(object):
    def __init__(self, raw):
        self.raw = raw


    def __repr__(self):
        return "ID: %d | Name: %s | Location: %s" % (self.get("deviceId"), self.get("name"), self.get("room"))


    def get(self, field):
        return self.raw[field]



class Client(object):
    apiVersion = "vX"   # test-version??
    def __init__(self, ip):
        self.ip = ip
        self.apiAddress = "http://" + ip + "/api/" + self.apiVersion
    

    def __repr__(self):
        system = self.getSystem()
        return "%s @ Version %s | serial-number: %s" % (system["system"], system["version"], system["serialNumber"])


    def getDeviceIds(self):
        req = requests.get(self.apiAddress + "/device")
        return (req.json())["deviceIds"]


    def getDevice(self, id):
        req = requests.get(self.apiAddress + "/device/" + str(id))
        return Device(req.json())


    def getDevices(self):
        deviceIds = self.getDeviceIds()
        devices = []
        for id in deviceIds:
            devices.append(self.getDevice(id))
        return devices
    

    def getDeviceByName(self, name):
        devices = self.getDevices()
        for dev in devices:
            if dev.get("name") == name:
                return dev

    def getStatusFields(self):
        req = requests.get(self.apiAddress + "/status/")
        return (req.json())["availableDataNames"]


    def getStatus(self, field):
        req = requests.get(self.apiAddress + "/status/" + field)
        return req.json()

    def getConsumption(self):
        return float((self.getStatus("consumption"))["valueNumeric"])

    
    def getProduction(self):
        return int((self.getStatus("production"))["valueNumeric"])
    

    def getMeter(self):
        return float((self.getStatus("meter"))["valueNumeric"])

    
    def getSystem(self):
        req = requests.get(self.apiAddress + "/system/")
        return req.json()

    def getBuild(self):
        req = requests.get(self.apiAddress + "/system/build")
        return req.json()