'''
环境质量数据读取并写入数据库
'''

import asyncio
import os
from datetime import datetime
import time

from apscheduler.schedulers.asyncio import AsyncIOScheduler
import motor.motor_asyncio
from pymodbus.client.asynchronous.tcp import AsyncModbusTCPClient as ModbusClient
# from pymodbus.constants import Defaults as Set
from pymodbus.client.asynchronous import schedulers

import addressing as ads


import logging
logging.basicConfig(filename='env_log.log', level=logging.WARNING)
log = logging.getLogger()
# log.setLevel(logging.DEBUG)

async def env_modbus2mongodb(collection, client, bus):
    # t = time.time()
    # log.debug("Read write registers simulataneously")
    # Set.TransactionId = 0x00
    for box in range(ads.busBox[bus - 1], ads.busBox[bus]):  # 云盒编号（0开始）
        rr = await client.read_holding_registers(ads.rgs, ads.len_data, unit=box + 1)
        data_modbus = rr.registers
        for i in range(ads.box_num[box][0]):  # 二合一编号（0开始）
            pos_two = ads.two_start + ads.two_len * i
            # print('two', data_modbus[pos_two + ads.pos_name], (box+1) * 256 + i+1)
            if data_modbus[pos_two + ads.pos_name] == (box + 1) * 256 + ads.two_start + i + 1:
                data_db = {'name': '{:0>2d}{:0>2d}{:0>2d}'.format(bus, box + 1, i + 1),
                           'two_in_one': {ads.two_type[j]: data_modbus[pos_two + ads.pos_data + j] * ads.two_carry[j]
                                          for j in range(2)},
                           'datetime': datetime.now()}
            else:
                data_db = {'name': '{:0>2d}{:0>2d}{:0>2d}'.format(bus, box + 1, i + 1),
                           'data': data_modbus,
                           'err': 'Unexpected Data Received',
                           'datetime': datetime.now()}
            result = await collection.insert_one(data_db)
            # data_all.append(data_db)

        for i in range(ads.box_num[box][1]):  # 六合一编号
            pos_six = ads.six_start * ads.two_len + ads.six_len * i
            # print('six', data_modbus[pos_six + ads.pos_name], (box+1) * 256 + ads.six_start+i + ads.six_bios+1)
            if data_modbus[pos_six + ads.pos_name] == (box + 1) * 256 + ads.six_start + i + ads.six_bios + 1:
                data_db = {'name': '{:0>2d}{:0>2d}{:0>2d}'.format(bus, box + 1, ads.six_start + i + 1),
                           'six_in_one': {ads.six_type[j]: data_modbus[pos_six + ads.pos_data + j] * ads.six_carry[j]
                                          for j in range(6)},
                           'datetime': datetime.now()}
            else:
                data_db = {'name': '{:0>2d}{:0>2d}{:0>2d}'.format(bus, box + 1, ads.six_start+i + 1),
                           'data': data_modbus,
                           'err': 'Unexpected Data Received',
                           'datetime': datetime.now()}
            result = await collection.insert_one(data_db)
            # data_all.append(data_db)

        await asyncio.sleep(1)
    # print('time consuming: ', time.time() - t)


if __name__ == '__main__':

    loop = asyncio.new_event_loop()
    # assert not loop.is_running()
    asyncio.set_event_loop(loop)
    new_loop, client1 = ModbusClient(schedulers.ASYNC_IO, host='192.168.1.82', port=1039, loop=loop)
    new_loop, client2 = ModbusClient(schedulers.ASYNC_IO, host='192.168.1.82', port=1040, loop=loop)
    new_loop, client3 = ModbusClient(schedulers.ASYNC_IO, host='192.168.1.82', port=1041, loop=loop)
    new_loop, client4 = ModbusClient(schedulers.ASYNC_IO, host='192.168.1.82', port=1042, loop=loop)
    new_loop, client5 = ModbusClient(schedulers.ASYNC_IO, host='192.168.1.82', port=1043, loop=loop)
    new_loop, client6 = ModbusClient(schedulers.ASYNC_IO, host='192.168.1.82', port=1044, loop=loop)
    new_loop, client7 = ModbusClient(schedulers.ASYNC_IO, host='192.168.1.83', port=1030, loop=loop)
    new_loop, client8 = ModbusClient(schedulers.ASYNC_IO, host='192.168.1.83', port=1031, loop=loop)
    new_loop, client9 = ModbusClient(schedulers.ASYNC_IO, host='192.168.1.83', port=1032, loop=loop)
    new_loop, client10 = ModbusClient(schedulers.ASYNC_IO, host='192.168.1.83', port=1033, loop=loop)
    new_loop, client11 = ModbusClient(schedulers.ASYNC_IO, host='192.168.1.83', port=1034, loop=loop)

    DBclient = motor.motor_asyncio.AsyncIOMotorClient('mongodb://192.168.1.10/',
                                                      username='sensorManager',
                                                      password='manage123456',
                                                      authSource='admin',
                                                      authMechanism='SCRAM-SHA-256',
                                                      io_loop=loop)
    db = DBclient['sensor_management']
    # collection = db['environment']
    collection = db['data_test']
    scheduler = AsyncIOScheduler()

    scheduler.add_job(env_modbus2mongodb, 'interval', args=[collection, client1.protocol, 1], seconds=300)
    scheduler.add_job(env_modbus2mongodb, 'interval', args=[collection, client2.protocol, 2], seconds=300)
    scheduler.add_job(env_modbus2mongodb, 'interval', args=[collection, client3.protocol, 3], seconds=300)
    scheduler.add_job(env_modbus2mongodb, 'interval', args=[collection, client4.protocol, 4], seconds=300)
    scheduler.add_job(env_modbus2mongodb, 'interval', args=[collection, client5.protocol, 5], seconds=300)
    scheduler.add_job(env_modbus2mongodb, 'interval', args=[collection, client6.protocol, 6], seconds=300)
    scheduler.add_job(env_modbus2mongodb, 'interval', args=[collection, client7.protocol, 7], seconds=300)
    scheduler.add_job(env_modbus2mongodb, 'interval', args=[collection, client8.protocol, 8], seconds=300)
    scheduler.add_job(env_modbus2mongodb, 'interval', args=[collection, client9.protocol, 9], seconds=300)
    scheduler.add_job(env_modbus2mongodb, 'interval', args=[collection, client10.protocol, 10], seconds=300)
    scheduler.add_job(env_modbus2mongodb, 'interval', args=[collection, client11.protocol, 11], seconds=300)
    scheduler.start()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    # Execution will block here until Ctrl+C (Ctrl+Break on Windows) is pressed.
    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass
