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
logging.basicConfig(filename='env_log1113.log', level=logging.INFO)  # WARNING DEBUG
log = logging.getLogger()


def env_modbus2mongodb():
    try:
        t = time()
        DBclient = MongoClient('mongodb://192.168.1.10/',
                               username='sensorManager',
                               password='manage123456',
                               authSource='admin')
        db = DBclient['sensor_management']
        # collection = db['environment']
        collection = db['data_test_1110']

        # data_all = []
        for bus in range(1, 12):
            client = ModbusClient(ads.conn[bus - 1][0], port=ads.conn[bus - 1][1], timeout=3, framer=ModbusFramer)
            client.connect()

            for box in range(ads.busBox[bus - 1], ads.busBox[bus]):  # 云盒编号（0开始）
                sleep(1)
                rr = client.read_holding_registers(ads.rgs, ads.len_data, unit=box + 1)
                if not hasattr(rr, 'registers'):
                    data_db = {'name': '{:0>2d}{:0>2d}xx'.format(bus, box + 1),
                               'message': rr.message,
                               'err': 'No Data Return',
                               'datetime': datetime.now()}
                    result = collection.insert_one(data_db)
                    continue
                data_modbus = rr.registers

                for i in range(ads.box_num[box][0]):  # 二合一编号（0开始）
                    pos_two = ads.two_start + ads.two_len * i
                    # print('two', data_modbus[pos_two + ads.pos_name], (box+1) * 256 + i+1)
                    if data_modbus[pos_two + ads.pos_name] == (box + 1) * 256 + ads.two_start + i + 1:
                        data_db = {'name': '{:0>2d}{:0>2d}{:0>2d}'.format(bus, box + 1, ads.two_start + i + 1),
                                   'two_in_one': {
                                       ads.two_type[j]: data_modbus[pos_two + ads.pos_data + j] * ads.two_carry[j]
                                       for j in range(2)},
                                   'datetime': datetime.now()}
                    else:
                        data_db = {'name': '{:0>2d}{:0>2d}{:0>2d}'.format(bus, box + 1, ads.two_start + i + 1),
                                   'data': data_modbus,
                                   'err': 'Unexpected Data Received',
                                   'datetime': datetime.now()}
                    result = collection.insert_one(data_db)
                    # data_all.append(data_db)

                for i in range(ads.box_num[box][1]):  # 六合一编号
                    pos_six = ads.six_start * ads.two_len + ads.six_len * i
                    # print('six', data_modbus[pos_six + ads.pos_name], (box+1) * 256 + ads.six_start+i + ads.six_bios+1)
                    if data_modbus[pos_six + ads.pos_name] == (box + 1) * 256 + ads.six_start + i + ads.six_bios + 1:
                        data_db = {'name': '{:0>2d}{:0>2d}{:0>2d}'.format(bus, box + 1, ads.six_start + i + 1),
                                   'six_in_one': {
                                       ads.six_type[j]: data_modbus[pos_six + ads.pos_data + j] * ads.six_carry[j]
                                       for j in range(6)},
                                   'datetime': datetime.now()}
                    else:
                        data_db = {'name': '{:0>2d}{:0>2d}{:0>2d}'.format(bus, box + 1, ads.six_start + i + 1),
                                   'data': data_modbus,
                                   'err': 'Unexpected Data Received',
                                   'datetime': datetime.now()}
                    result = collection.insert_one(data_db)
                    # data_all.append(data_db)

                # await asyncio.sleep(1)
            client.close()
        DBclient.close()
        log.info('Time Consuming: ' + str(time() - t))
    except Exception as e:
        # log.exception(e)
        client.close()
        DBclient.close()
        log.error(e)
        log.info('Time Consuming: ' + str(time() - t))


def env_modbus2mongodb_next():
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
        # collection = db['environment']
        collection = db['data_test_1110']

        # data_all = []
        for bus in range(1, 12):
            client = ModbusClient(ads.conn[bus - 1][0], port=ads.conn[bus - 1][1], timeout=1, framer=ModbusFramer)

            is_connected = client.connect()
            if not is_connected:  # modbus连接失败
                data_db = {'name': '{:0>2d}xxxx'.format(bus),
                           'err': 'Modbus Connect Failed',
                           'datetime': datetime.now()}
                result = collection.insert_one(data_db)
                client.close()
                sleep(1)
                continue

            for box in range(ads.busBox[bus - 1], ads.busBox[bus]):  # 云盒编号（0开始）
                sleep(1)
                rr = client.read_holding_registers(ads.rgs, ads.len_data, unit=box + 1)
                if not hasattr(rr, 'registers'):  # 无返回数据
                    data_db = {'name': '{:0>2d}{:0>2d}xx'.format(bus, box + 1),
                               'message': rr.message,
                               'err': 'No Data Return',
                               'datetime': datetime.now()}
                    result = collection.insert_one(data_db)
                    continue
                data_modbus = rr.registers

                for i in range(ads.box_num[box][0]):  # 二合一编号（0开始）
                    pos_two = ads.two_start + ads.two_len * i
                    # print('two', data_modbus[pos_two + ads.pos_name], (box+1) * 256 + i+1)
                    if data_modbus[pos_two + ads.pos_name] == (box + 1) * 256 + ads.two_start + i + 1:
                        data_db = {'name': '{:0>2d}{:0>2d}{:0>2d}'.format(bus, box + 1, ads.two_start + i + 1),
                                   'two_in_one': {
                                       ads.two_type[j]: data_modbus[pos_two + ads.pos_data + j] * ads.two_carry[j]
                                       for j in range(2)},
                                   'datetime': datetime.now()}
                    else:
                        data_db = {'name': '{:0>2d}{:0>2d}{:0>2d}'.format(bus, box + 1, ads.two_start + i + 1),
                                   'data': data_modbus,
                                   'err': 'Unexpected Data Received',
                                   'datetime': datetime.now()}
                    result = collection.insert_one(data_db)
                    # data_all.append(data_db)

                for i in range(ads.box_num[box][1]):  # 六合一编号
                    pos_six = ads.six_start * ads.two_len + ads.six_len * i
                    # print('six', data_modbus[pos_six + ads.pos_name], (box+1) * 256 + ads.six_start+i + ads.six_bios+1)
                    if data_modbus[pos_six + ads.pos_name] == (box + 1) * 256 + ads.six_start + i + ads.six_bios + 1:
                        data_db = {'name': '{:0>2d}{:0>2d}{:0>2d}'.format(bus, box + 1, ads.six_start + i + 1),
                                   'six_in_one': {
                                       ads.six_type[j]: data_modbus[pos_six + ads.pos_data + j] * ads.six_carry[j]
                                       for j in range(6)},
                                   'datetime': datetime.now()}
                    else:
                        data_db = {'name': '{:0>2d}{:0>2d}{:0>2d}'.format(bus, box + 1, ads.six_start + i + 1),
                                   'data': data_modbus,
                                   'err': 'Unexpected Data Received',
                                   'datetime': datetime.now()}
                    result = collection.insert_one(data_db)
                    # data_all.append(data_db)
            client.close()
        # DBclient.close()
    except ConnectionFailure as e:
        log.error(e)
    except Exception as e:
        # log.exception(e)
        # client.close()
        # DBclient.close()
        log.error(e)
        # log.info('Time Consuming: ' + str(time() - t))
        return
    finally:
        DBclient.close()
        log.info('Time Consuming: ' + str(time() - t))



if __name__ == '__main__':

    # while ((datetime.now().minute) % 5 != 0):
    #     time.sleep(1)
    # DBclient = MongoClient('mongodb://192.168.1.10/',
    #                        username='sensorManager',
    #                        password='manage123456',
    #                        authSource='admin')
    # db = DBclient['sensor_management']
    # # collection = db['environment']
    # collection = db['data_test']
    #
    # jobstores = {
    #     'mongo': MongoDBJobStore(database='sensor_management', collection='jobs', client=DBclient),
    # }
    job_defaults = {
        'coalesce': True,
        'misfire_grace_time': 120,
        'max_instances': 2
    }
    scheduler = BackgroundScheduler(job_defaults=job_defaults)  # jobstores=jobstores
    scheduler.add_job(env_modbus2mongodb_next, 'interval', seconds=300, id='env_bus2db',
                      replace_existing=True)  # , jobstore='mongo'
    scheduler.start()
    log.info('Start Time: ' + str(datetime.now()))
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            sleep(10)
    # except (KeyboardInterrupt, SystemExit):
    except Exception as e:
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown()
        log.error(e)
        log.info('End Time: ' + str(datetime.now()))

# async def env_modbus2mongodb(collection):
#     try:
#         # bus = 6
#         # client = ModbusClient('192.168.1.82', port=1038+bus, timeout=3)
#         # t = time.time()
#         # data_all = []
#         for bus in range(1, 12):
#             client = ModbusClient(ads.conn[bus - 1][0], port=ads.conn[bus - 1][1], timeout=3)
#             client.connect()
#
#             for box in range(ads.busBox[bus - 1], ads.busBox[bus]):  # 云盒编号（0开始）
#                 await asyncio.sleep(1)
#                 rr = client.read_holding_registers(ads.rgs, ads.len_data, unit=box + 1)
#                 if not hasattr(rr, 'registers'):
#                     data_db = {'name': '{:0>2d}{:0>2d}xx'.format(bus, box + 1),
#                                'message': rr.message,
#                                'err': 'No Data Return',
#                                'datetime': datetime.now()}
#                     result = await collection.insert_one(data_db)
#                     continue
#                 data_modbus = rr.registers
#
#                 for i in range(ads.box_num[box][0]):  # 二合一编号（0开始）
#                     pos_two = ads.two_start + ads.two_len * i
#                     # print('two', data_modbus[pos_two + ads.pos_name], (box+1) * 256 + i+1)
#                     if data_modbus[pos_two + ads.pos_name] == (box + 1) * 256 + ads.two_start + i + 1:
#                         data_db = {'name': '{:0>2d}{:0>2d}{:0>2d}'.format(bus, box + 1, i + 1),
#                                    'two_in_one': {ads.two_type[j]: data_modbus[pos_two + ads.pos_data + j] / 10
#                                                   for j in range(2)},
#                                    'datetime': datetime.now()}
#                     else:
#                         data_db = {'name': '{:0>2d}{:0>2d}{:0>2d}'.format(bus, box + 1, i + 1),
#                                    'data': data_modbus,
#                                    'err': 'Unexpected Data Received',
#                                    'datetime': datetime.now()}
#                     result = await collection.insert_one(data_db)
#                     # data_all.append(data_db)
#
#                 for i in range(ads.box_num[box][1]):  # 六合一编号
#                     pos_six = ads.six_start * ads.two_len + ads.six_len * i
#                     # print('six', data_modbus[pos_six + ads.pos_name], (box+1) * 256 + ads.six_start+i + ads.six_bios+1)
#                     if data_modbus[pos_six + ads.pos_name] == (box + 1) * 256 + ads.six_start + i + ads.six_bios + 1:
#                         data_db = {'name': '{:0>2d}{:0>2d}{:0>2d}'.format(bus, box + 1, i + 1),
#                                    'six_in_one': {ads.six_type[j]: data_modbus[pos_six + ads.pos_data + j] / 10
#                                                   for j in range(6)},
#                                    'datetime': datetime.now()}
#                     else:
#                         data_db = {'name': '{:0>2d}{:0>2d}{:0>2d}'.format(bus, box + 1, i + 1),
#                                    'data': data_modbus,
#                                    'err': 'Unexpected Data Received',
#                                    'datetime': datetime.now()}
#                     result = await collection.insert_one(data_db)
#                     # data_all.append(data_db)
#
#                 # await asyncio.sleep(1)
#             client.close()
#         # print('time consuming: ', time.time() - t)
#     except Exception as e:
#         # log.exception(e)
#         log.error(e)
#         client.close()
#
#
# if __name__ == '__main__':
#
#     loop = asyncio.new_event_loop()
#     # assert not loop.is_running()
#     asyncio.set_event_loop(loop)
#     DBclient = motor.motor_asyncio.AsyncIOMotorClient('mongodb://192.168.1.10/',
#                                                       username='sensorManager',
#                                                       password='manage123456',
#                                                       authSource='admin',
#                                                       authMechanism='SCRAM-SHA-256',
#                                                       io_loop=loop)
#     db = DBclient['sensor_management']
#     # collection = db['environment']
#     collection = db['data_test']
#
#     # while ((datetime.now().minute) % 5 != 0):
#     #     time.sleep(1)
#
#     scheduler = AsyncIOScheduler()
#     scheduler.add_job(env_modbus2mongodb, 'interval', args=[collection], seconds=300)
#     scheduler.start()
#     log.info('Start Time: ' + str(datetime.now()))
#     print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
#
#     # Execution will block here until Ctrl+C (Ctrl+Break on Windows) is pressed.
#     try:
#         asyncio.get_event_loop().run_forever()
#     except (KeyboardInterrupt, SystemExit):
#         log.info('End Time: ' + str(datetime.now()))
#         pass
