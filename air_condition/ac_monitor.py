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

logging.basicConfig(filename='ac_log1201.log', level=logging.INFO)  # WARNING DEBUG
log = logging.getLogger()

ac_N = [14, 2, 4, 14, 5]


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
        collection = db['air_condition_test_1202']

        for i in range(5):
            client = ModbusClient(ads.conn[i][0], port=ads.conn[i][1], timeout=3, framer=ModbusFramer)
            is_connected = client.connect()
            if not is_connected:  # modbus连接失败
                data_db = {'name': '{:0>2d}xx'.format(i + 1),
                           'err': 'Modbus Connect Failed',
                           'datetime': datetime.now()}
                result = collection.insert_one(data_db)
                client.close()
                sleep(1)
                continue
            for j in range(ac_N[i]):
                sleep(1)
                rr = client.read_holding_registers(ads.rgs_start + j * ads.rgs_len, ads.len_data, unit=ads.box_ads)
                if not hasattr(rr, 'registers'):  # 无返回数据
                    data_db = {'name': '{:0>2d}{:0>2d}xx:'.format(i + 1, j + 1),
                               'message': rr.message,
                               'err': 'No Data Return',
                               'datetime': datetime.now()}
                    result = collection.insert_one(data_db)
                    continue
                data_modbus = rr.registers
                err_d = True
                for k in range(4):
                    if (data_modbus[i] != 0):
                        err_d = False
                        break
                    pass
                if err_d:
                    data_db = {'name': '{:0>2d}{:0>2d}'.format(i + 1, j + 1),
                               'data': data_modbus,
                               'err': 'All Null',
                               'datetime': datetime.now()}
                else:
                    data_db = {'name': '{:0>2d}{:0>2d}'.format(i + 1, j + 1),
                               'data': data_modbus,
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
