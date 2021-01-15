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
# import addressing as ads
from datetime import datetime

import logging

logging.basicConfig(filename='power_log0115.log', level=logging.INFO)  # WARNING DEBUG
log = logging.getLogger()


def power_modbus2mongodb():
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
        collection = db['power_test_0115']

        name=['room1','room2','room4']
        gateway=[24,48,87]
        register=[0x2000,0x4000]
        length=[18,2]

        client = ModbusClient('192.168.1.146', port=12345, timeout=3, framer=ModbusFramer)
        is_connected = client.connect()
        if is_connected:  # modbus connect fail
            for i in range(3):
                data=[]
                for j in range(2):
                    sleep(1)
                    rr = client.read_holding_registers(register[j], length[j], unit=gateway[i])
                    if hasattr(rr, 'registers'):  # no data return
                        data.append(rr.registers)
                    else:
                        data.append('No Data Return')
                data_db = {'name': name[i],
                           'data': data,
                           'datetime': datetime.now()}
                result = collection.insert_one(data_db)

        else:
            data_db = {'name': '{:0>2d}xxxx'.format(bus),
                       'err': 'Modbus Connect Failed',
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
    scheduler.add_job(power_modbus2mongodb, trigger=trigger, id='env_bus2db',
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
