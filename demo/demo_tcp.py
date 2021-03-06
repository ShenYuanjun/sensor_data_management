import asyncio
import os
from datetime import datetime
import time

# from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
# from apscheduler.schedulers.background import BackgroundScheduler
# from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
# from apscheduler.executors.asyncio import AsyncIOExecutor
# from pymongo import MongoClient
import motor.motor_asyncio
from pymodbus.client.asynchronous.tcp import AsyncModbusTCPClient as ModbusClient
from pymodbus.client.asynchronous import schedulers
from pymodbus.transaction import ModbusRtuFramer as ModbusFramer

UNIT = 0x00

async def start_async_test(collection, client):

    # arguments = {
    #     'read_address': 1,
    #     'read_count': 8,
    #     'write_address': 1,
    #     'write_registers': [20] * 8,
    # }
    t = time.time()
    # rq = await client.readwrite_registers(unit=UNIT, **arguments)
    adress_register = 0  # 起始寄存器
    length_data = 0x40  # 数据长度 HEX=
    adress_gateway = 0x1  # 云盒地址
    rr = await client.read_holding_registers(adress_register, length_data, unit=adress_gateway)
    # rr = await client.read_holding_registers(1, 8, unit=UNIT)

    document = {'data': rr.registers, "time": datetime.now()}
    result = await collection.insert_one(document)
    print('inserted: %s' % repr(result.inserted_id))

    await asyncio.sleep(1)
    print('time consuming: ', time.time()-t)

async def countAsyn(collection):
    # collection = await DBconnect()
    all = await collection.count_documents({})
    print("There is/are " + str(all) + " document(s)")


if __name__ == '__main__':

    loop = asyncio.new_event_loop()
    # assert not loop.is_running()
    asyncio.set_event_loop(loop)
    new_loop, client = ModbusClient(schedulers.ASYNC_IO, host='192.168.1.82', port=1032, loop=loop, framer=ModbusFramer)
    DBclient = motor.motor_asyncio.AsyncIOMotorClient('mongodb://192.168.1.10/',
                                                      username='zgl',
                                                      password='123456',
                                                      authSource='admin',
                                                      authMechanism='SCRAM-SHA-256',
                                                      io_loop=loop)
    db = DBclient['cpes']
    collection = db['data_test']
    scheduler = AsyncIOScheduler()

    scheduler.add_job(start_async_test, 'interval', args=[collection, client.protocol], seconds=3)
    scheduler.add_job(countAsyn, 'interval', args=[collection], seconds=3)
    scheduler.start()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    # Execution will block here until Ctrl+C (Ctrl+Break on Windows) is pressed.
    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass
