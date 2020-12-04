from pymongo import MongoClient
import json
from time import sleep

client = MongoClient('mongodb://192.168.1.10/',
                     username='sensorTester',
                     password='test123456',
                     authSource='admin')
db = client['sensor_management']
collection = db['data_test_1201']

# ln = ['010121', '010201', '010601', '010721', '010801', '020904', '021001', '031122', '031222', '031301', '031401',
#       '041801', '052002', '052101', '052201', '052301', '062421', '062522', '062702', '072802', '073001', '073301',
#       '083501', '083601', '093701', '093805', '103905', '104001', '114102', '1141xx', '114201', '1142xx']
#
#
# ln_DTU = ['010201', '010601', '010801', '021001', '031301', '031401', '041801', '052101', '052201', '052301', '073001',
#           '073301', '083501', '083601', '093701', '104001', '114201']

busBox = [0, 8, 10, 14, 19, 23, 27, 34, 36, 38, 40, 42]

filename = 'err_time1201.json'

data_all = {}
for bus in range(1, 12):
    for box in range(busBox[bus - 1], busBox[bus]):
        data_n = []
        sleep(1)
        name = '{:0>2d}{:0>2d}'.format(bus, box+1)
        for post in collection.find({"name": name, "err": {"$ne": None}}):
            data_n.append(str(post['datetime']))
        if data_n:
            data_all[name] = data_n




# for n in ln_DTU:
#     data_n = []
#     sleep(1)
#     for post in collection.find({"name": n, "err": {"$ne": None}}):
#         data_n.append(str(post['datetime']))
#     data_all[n[2:4]] = data_n


with open(filename, 'w') as f:
    json.dump(data_all,f)
# data_all = []
# for post in collection.find({"name": "010601", "err": {"$ne": None}}):
#     data_all.append(post['datetime'])

