# coding=utf-8

# import asyncio
import os
# from datetime import datetime
from time import sleep, time

# from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.combining import OrTrigger
from apscheduler.triggers.cron import CronTrigger
# from apscheduler.jobstores.mongodb import MongoDBJobStore
# import motor.motor_asyncio
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.transaction import ModbusRtuFramer as ModbusFramer
import addressing as ads
from datetime import datetime

import logging

logging.basicConfig(filename='env_log1212.log', level=logging.INFO)  # WARNING DEBUG
log = logging.getLogger()


def env_modbus2mongodb():
    try:
        t = time()

        DBclient = MongoClient('mongodb://192.168.1.10/',
                               username='sensorManager',
                               password='manage123456',
                               authSource='admin',
                               serverSelectionTimeoutMS=1000)

        # try:  # test db connect
        #     # The ismaster command is cheap and does not require auth.
        #     DBclient.admin.command('ismaster')
        # except ConnectionFailure as e:  # Exception
        #     DBclient.close()
        #     log.error(e)
        #     # print("Server not available")
        #     return

        db = DBclient['sensor_management']
        collection = db['data_test_1212']

        for bus in range(1, 12):
            client = ModbusClient(ads.conn[bus - 1][0], port=ads.conn[bus - 1][1], timeout=3, framer=ModbusFramer)

            is_connected = client.connect()
            if not is_connected:  # modbus connect fail
                data_db = {'name': '{:0>2d}xxxx'.format(bus),
                           'err': 'Modbus Connect Failed',
                           'datetime': datetime.now()}
                result = collection.insert_one(data_db)
                client.close()
                sleep(1)
                continue

            for box in range(ads.busBox[bus - 1], ads.busBox[bus]):  # box index (begin from 0)
                sleep(3)
                rr = client.read_holding_registers(ads.rgs, ads.len_data, unit=box + 1)
                if not hasattr(rr, 'registers'):  # no data return
                    data_db = {'name': '{:0>2d}{:0>2d}xx'.format(bus, box + 1),
                               'message': rr.message,
                               'err': 'No Data Return',
                               'datetime': datetime.now()}
                    result = collection.insert_one(data_db)
                    continue
                data_modbus = rr.registers

                err_d = True
                for k in range(112):
                    if (data_modbus[k] != 0):
                        err_d = False
                        break
                    pass

                if err_d:
                    data_db = {'name': '{:0>2d}{:0>2d}'.format(bus, box + 1),
                               'data': data_modbus,
                               'err': 'All Null',
                               'datetime': datetime.now()}
                    result = collection.insert_one(data_db)
                else:
                    # data_db = {'name': '{:0>2d}{:0>2d}'.format(bus, box + 1),
                    #            'data': data_modbus,
                    #            'datetime': datetime.now()}

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
                    for i in range(ads.box_num[box][1]):  # 六合一编号
                        pos_six = ads.six_start * ads.two_len + ads.six_len * i
                        # print('six', data_modbus[pos_six + ads.pos_name], (box+1) * 256 + ads.six_start+i + ads.six_bios+1)
                        if data_modbus[pos_six + ads.pos_name] == (
                                box + 1) * 256 + ads.six_start + i + ads.six_bios + 1:
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

            client.close()
    except ConnectionFailure as e:
        log.error(e)
    except Exception as e:
        # log.exception(e)
        # client.close()
        # DBclient.close()
        log.error(e)
        return
    finally:
        DBclient.close()
        # log.info('Time Consuming: ' + str(time() - t))


if __name__ == '__main__':

    job_defaults = {
        'coalesce': True,
        'misfire_grace_time': 120,
        'max_instances': 2
    }
    trigger = OrTrigger([CronTrigger(minute=i) for i in range(0, 60, 5)])
    scheduler = BackgroundScheduler(job_defaults=job_defaults)  # jobstores=jobstores
    # scheduler.add_job(env_modbus2mongodb_next, 'interval', seconds=300, id='env_bus2db',
    #                   replace_existing=True)
    scheduler.add_job(env_modbus2mongodb, trigger=trigger, id='env_bus2db',
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
