'''
空调数据读取并写入数据库
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

logging.basicConfig(filename='air_log1111.log', level=logging.INFO)  # WARNING DEBUG
log = logging.getLogger()


def air_modbus2mongodb():
    try:
        t = time()

        DBclient = MongoClient('mongodb://192.168.1.10/',
                               username='sensorManager',
                               password='manage123456',
                               authSource='admin',
                               serverSelectionTimeoutMS=2000)

        try:  # 数据库连接测试
            # The ismaster command is cheap and does not require auth.
            DBclient.admin.command('ismaster')
        except ConnectionFailure as e:  # Exception
            DBclient.close()
            log.error(e)
            # print("Server not available")
            return

        db = DBclient['sensor_management']
        # collection = db['air_condition']
        collection = db['data_test_air_']
        logger = db['air_condition_logger']

        equipments = [{} for i in range(9)]
        for i in range(9):  # 9根总线读数据
            client = ModbusClient(ads.conn[i][0], port=ads.conn[i][1], timeout=3)
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

            for j in range(ads.bus_sensor_number[i]):
                rr = client.read_holding_registers(ads.rgs_start + j * ads.rgs_len, ads.len_data, unit=ads.box_ads)
                if not hasattr(rr, 'registers'):  # 无返回数据
                    data_db = {'name': 'bus{:0>1d}:'.format(i + 1) + ads.equipment_index[i] + '-' + bus[j][1],
                               'message': rr.message,
                               'err': 'No Data Return',
                               'datetime': datetime.now()}
                    result = logger.insert_one(data_db)
                    continue

                data_modbus = rr.registers
                type = data_modbus[0] // 256  # 数据类型
                if type != bus[j][2]:
                    data_db = {'name': 'bus{:0>1d}:'.format(i + 1) + ads.equipment_index[i] + '-' + bus[j][1],
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
                    data_db = {'name': 'bus{:0>1d}:'.format(i + 1) + ads.equipment_index[i] + '-' + bus[j][1],
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
            client.close()

        for eqt in range(9):  # 9个设备写入数据库
            data_db = {'name': ads.equipment_index[eqt],
                       'data': equipments[eqt],
                       'datetime': datetime.now()}
            result = collection.insert_one(data_db)

        DBclient.close()
        log.info('Time Consuming: ' + str(time() - t))
    except Exception as e:
        # log.exception(e)
        # client.close()
        # DBclient.close()
        log.error(e)
        log.info('Time Consuming: ' + str(time() - t))
        return


if __name__ == '__main__':

    # while ((datetime.now().minute) % 5 != 0):
    #     time.sleep(1)

    # jobstores = {
    #     'mongo': MongoDBJobStore(database='sensor_management', collection='jobs', client=DBclient),
    # }
    job_defaults = {
        'coalesce': True,
        'misfire_grace_time': 120,
        'max_instances': 3
    }
    scheduler = BackgroundScheduler(job_defaults=job_defaults)  # jobstores=jobstores
    scheduler.add_job(air_modbus2mongodb, 'interval', seconds=300, id='air_bus2db',
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