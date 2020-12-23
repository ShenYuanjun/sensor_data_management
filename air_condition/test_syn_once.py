'''
测试数据
'''
# import asyncio
import os
# from datetime import datetime
from time import sleep, time

# from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.schedulers.background import BackgroundScheduler
# from apscheduler.jobstores.mongodb import MongoDBJobStore
# import motor.motor_asyncio
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.transaction import ModbusRtuFramer as ModbusFramer
import addressing as ads
from datetime import datetime

import logging

logging.basicConfig(level=logging.DEBUG, filename='air_log1219.log')  # WARNING INFO
log = logging.getLogger()

try:
    t = time()

    DBclient = MongoClient('mongodb://192.168.1.10/',
                           username='sensorManager',
                           password='manage123456',
                           authSource='admin',
                           serverSelectionTimeoutMS=1000)

    # try:  # 数据库连接测试
    #     # The ismaster command is cheap and does not require auth.
    #     DBclient.admin.command('ismaster')
    # except ConnectionFailure as e:  # Exception
    #     DBclient.close()
    #     log.error(e)
    #     # print("Server not available")
    #     return

    db = DBclient['sensor_management']
    # collection = db['air_condition']
    collection = db['data_test_ac_1219']
    logger = db['air_condition_logger_1219']

    equipments = [{} for i in range(9)]
    for i in range(5):  # 12345总线读数据
        client = ModbusClient(ads.conn[i][0], port=ads.conn[i][1], timeout=3, framer=ModbusFramer)
        bus = ads.buses[i]

        is_connected = client.connect()
        if not is_connected:  # modbus连接失败
            data_db = {'name': 'bus{:0>1d}'.format(i + 1),
                       'err': 'Modbus Connect Failed',
                       'datetime': datetime.now()}
            result = logger.insert_one(data_db)
            client.close()
            sleep(1)
            continue

        sleep(1)
        rr = client.read_coils(ads.rgs_start, ads.len_data, unit=ads.box_ads)
        if hasattr(rr, 'bits'):
            checkout = rr.bits
        else:
            data_db = {'name': 'bus{:0>1d}:'.format(i + 1),
                       'message': rr.message,
                       'err': 'Checkout Failed',
                       'datetime': datetime.now()}
            result = logger.insert_one(data_db)
            checkout = [True for i in range(16)]

        for j in range(len(bus)):
            if checkout[j]:
                sleep(1)
                rr = client.read_holding_registers(ads.rgs_start + j * ads.rgs_len, ads.len_data, unit=ads.box_ads)
                if not hasattr(rr, 'registers'):  # 无返回数据
                    data_db = {'name': 'bus{:0>1d}:'.format(i + 1) + ads.equipment_index[bus[j][0]] + '-' + bus[j][1],
                               'message': rr.message,
                               'err': 'No Data Return',
                               'datetime': datetime.now()}
                    result = logger.insert_one(data_db)
                    continue
                data_modbus = rr.registers
                type = data_modbus[0] // 256  # 数据类型
                if type != bus[j][2]:
                    data_db = {'name': 'bus{:0>1d}:'.format(i + 1) + ads.equipment_index[bus[j][0]] + '-' + bus[j][1],
                               'data': data_modbus,
                               'err': 'Wrong Type Index: Should be 0x{:0X}, but accepted 0x{:0X}'.format(bus[j][2],
                                                                                                         type),
                               'datetime': datetime.now()}
                    result = logger.insert_one(data_db)
                    continue
                pos = data_modbus[0] % 16  # 小数位数
                sign_n = data_modbus[0] % 256 - pos  ## 有无符号
                if sign_n == 0x80:
                    sign = True  # 有符号
                elif sign_n == 0x00:
                    sign = False  # 无符号
                else:
                    data_db = {'name': 'bus{:0>1d}:'.format(i + 1) + ads.equipment_index[bus[j][0]] + '-' + bus[j][1],
                               'data': data_modbus,
                               'err': 'Wrong Sign Index: Should be 0x{:0X} or 0x{:0X}, but accepted 0x{:0X}'.format(
                                   0x80, 0x00, sign_n),
                               'datetime': datetime.now()}
                    result = logger.insert_one(data_db)
                    continue
                data_origin = data_modbus[1]
                if sign and data_origin >= 32767:
                    data = -(65536 - data_origin) / (10 ** pos)
                else:
                    data = data_origin / (10 ** pos)
                equipments[bus[j][0]][bus[j][1]] = data

            else:
                data_db = {'name': 'bus{:0>1d}:'.format(i + 1) + ads.equipment_index[bus[j][0]] + '-' + bus[j][1],
                           'data': checkout,
                           'err': 'The Sensor Is Outline',
                           'datetime': datetime.now()}
                result = logger.insert_one(data_db)
        client.close()

    for i in range(5, 9):  # 6789总线读数据
        client = ModbusClient(ads.conn[i][0], port=ads.conn[i][1], timeout=3, framer=ModbusFramer)
        bus = ads.buses[i]

        is_connected = client.connect()
        if not is_connected:  # modbus连接失败
            data_db = {'name': 'bus{:0>1d}'.format(i + 1),
                       'err': 'Modbus Connect Failed',
                       'datetime': datetime.now()}
            result = logger.insert_one(data_db)
            client.close()
            sleep(1)
            continue

        sleep(1)
        rr = client.read_holding_registers(ads.rgs_start, ads.len_data, unit=ads.box_ads)
        if not hasattr(rr, 'registers'):  # 无返回数据
            data_db = {'name': 'bus{:0>1d}:'.format(i + 1),
                       'message': rr.message,
                       'err': 'No Data Return',
                       'datetime': datetime.now()}
            result = logger.insert_one(data_db)
            continue
        data_modbus = rr.registers
        for j in range(len(bus)):
            type = data_modbus[2 * j] // 4096  # 数据类型 C0
            if type != 12:
                data_db = {'name': 'bus{:0>1d}:'.format(i + 1) + ads.equipment_index[bus[j][0]] + '-' + bus[j][1],
                           'data': data_modbus,
                           'err': 'Wrong Type Index: Should be 0xC0, but accepted 0x{:0X}'.format(type),
                           'datetime': datetime.now()}
                result = logger.insert_one(data_db)
                continue
            pos = data_modbus[0] % 256  # 小数位数
            data_origin = data_modbus[2 * j + 1] / (10 ** pos)
            inf0 = ads.i2v[0][0]
            sup0 = ads.i2v[0][1]
            inf1 = ads.i2v[bus[j][2]][0]
            sup1 = ads.i2v[bus[j][2]][1]
            if inf0 <= data_origin <= sup0:
                data = (data_origin - inf0) / (sup0 - inf0) * (sup1 - inf1) + inf1
            else:
                data_db = {'name': 'bus{:0>1d}:'.format(i + 1) + ads.equipment_index[bus[j][0]] + '-' + bus[j][1],
                           'data': data_modbus,
                           'err': 'Wrong Value Range: Should be 4~20, but accepted {:0X}'.format(data_origin),
                           'datetime': datetime.now()}
                result = logger.insert_one(data_db)
                continue
            equipments[bus[j][0]][bus[j][1]] = data
        client.close()

    # for eqt in range(9):  # 9个设备写入数据库
    #     data_db = {'name': ads.equipment_index[eqt],
    #                'data': equipments[eqt],
    #                'datetime': datetime.now()}
    #     result = collection.insert_one(data_db)
    data_db = []
    for eqt in range(9):  # 9个设备写入数据库
        data_db.append({'name': ads.equipment_index[eqt],
                        'data': equipments[eqt],
                        'datetime': datetime.now()})
    result = collection.insert_many(data_db)

    # meter
    client = ModbusClient(ads.conn[9][0], port=ads.conn[9][1], timeout=3, framer=ModbusFramer)
    bus = ads.bus_meter
    is_connected = client.connect()
    if is_connected:  # modbus连接失败
        data = {}
        for i in range(len(bus)):
            sleep(1)
            rr = client.read_holding_registers(bus[i][1], bus[i][2], unit=ads.box_ads)
            if not hasattr(rr, 'registers'):  # 无返回数据
                data_db = {'name': 'meter',
                           'message': rr.message,
                           'err': 'No Data Return',
                           'datetime': datetime.now()}
                result = logger.insert_one(data_db)
                continue
            data_modbus = rr.registers
            value = 0
            for j in range(bus[i][2]):
                value += data_modbus[j] * 0x10000 ** (bus[i][2] - j - 1)
            data[bus[i][0]] = value
        client.close()
        data_db = {'name': 'meter',
                   'data': data,
                   'datetime': datetime.now()}
        result = collection.insert_one(data_db)
    else:
        data_db = {'name': 'bus_meter',
                   'err': 'Modbus Connect Failed',
                   'datetime': datetime.now()}
        result = logger.insert_one(data_db)
        client.close()
        sleep(1)


    # host
    client = ModbusClient(ads.conn[10][0], port=ads.conn[10][1], timeout=3, framer=ModbusFramer)
    bus = ads.bus_host
    is_connected = client.connect()
    if is_connected:  # modbus连接失败
        data = {}
        for i in range(len(bus)):
            sleep(1)
            rr = client.read_holding_registers(bus[i][1], bus[i][2], unit=ads.box_ads)
            if not hasattr(rr, 'registers'):  # 无返回数据
                data_db = {'name': 'host',
                           'message': rr.message,
                           'err': 'No Data Return',
                           'datetime': datetime.now()}
                result = logger.insert_one(data_db)
                continue
            data_modbus = rr.registers
            data[bus[i][0]] = data_modbus
        client.close()
        # data_db = {'name': 'meter',
        #            'data': data,
        #            'datetime': datetime.now()}
        data['name'] = 'host'
        data['datetime'] = datetime.now()
        result = collection.insert_one(data)
    else:
        data_db = {'name': 'bus_host',
                   'err': 'Modbus Connect Failed',
                   'datetime': datetime.now()}
        result = logger.insert_one(data_db)
        client.close()
        sleep(1)


except ConnectionFailure as e:  # Exception
    log.error(e)
#     DBclient.close()
except Exception as e:
    # log.exception(e)
    # client.close()
    # DBclient.close()
    log.error(e)
finally:
    DBclient.close()
    log.info('Time Consuming: ' + str(time() - t))
