# import asyncio
# import os
#
# # import modbus_tk
# import modbus_tk.defines as cst
# from modbus_tk import modbus_tcp
#
#
# from apscheduler.schedulers.asyncio import AsyncIOScheduler
#
# async def readMB(master):
#     red = await master.execute(1, cst.READ_HOLDING_REGISTERS, 0, 3)
#     print('read: %s' % repr(red))
#
#
# master = modbus_tcp.TcpMaster("127.0.0.1", 5020)
# master.set_timeout(5.0)
#
# scheduler = AsyncIOScheduler()
#
# scheduler.add_job(readMB, 'interval', args=[master], seconds=3)
# scheduler.start()
# print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
# try:
#     asyncio.get_event_loop().run_forever()
# except (KeyboardInterrupt, SystemExit):
#     pass

# import threading
# import time
# from datetime import datetime
#
# def hello():
#     print(datetime.now())
# try:
#     while True:
#         t = threading.Timer(3, hello)
#         # time.sleep(2)
#         t.start()
# except (KeyboardInterrupt, SystemExit):
#     pass

import asyncio
import os
from datetime import datetime
from time import time
# import pprint

# from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.executors.asyncio import AsyncIOExecutor
# from pymongo import MongoClient
import motor.motor_asyncio
from pymodbus.client.asynchronous.tcp import AsyncModbusTCPClient as ModbusClient
from pymodbus.client.asynchronous import schedulers

UNIT = 0x00


async def start_async_test(client):
    # rq = await MBclient.write_register(1, 10, unit=UNIT)
    # rr = await MBclient.read_holding_registers(1, 1, unit=UNIT)
    # # assert(rq.function_code < 0x80)     # test that we are not an error
    # # assert(rr.registers[0] == 10)       # test the expected value
    #
    # rq = await MBclient.write_registers(1, [10]*8, unit=UNIT)
    # rr = await MBclient.read_holding_registers(1, 8, unit=UNIT)
    # # assert(rq.function_code < 0x80)     # test that we are not an error
    # # assert(rr.registers == [10]*8)      # test the expected value

    arguments = {
        'read_address': 1,
        'read_count': 8,
        'write_address': 1,
        'write_registers': [20] * 8,
    }
    rq = await client.readwrite_registers(unit=UNIT, **arguments)
    rr = await client.read_holding_registers(1, 8, unit=UNIT)
    # await writeDB(collection, rr)
    # await asyncio.sleep(3)
    collection = await DBconnect()
    document = {'data': rr.registers, "time": datetime.now()}
    result = await collection.insert_one(document)
    print('inserted: %s' % repr(result.inserted_id))
    # print(rr.registers)
    # print(datetime.now())
    await asyncio.sleep(1)


async def writeDB(collection, rr):
    document = {'data': rr.registers, "time": datetime.now()}
    result = await collection.insert_one(document)
    print('inserted: %s' % repr(result.inserted_id))


async def countAsyn():
    collection = await DBconnect()
    all = await collection.count_documents({})
    print("There is/are " + str(all) + " document(s)")


async def DBconnect():
    t = time()
    client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://192.168.1.10/',
                                                    username='zgl',
                                                    password='123456',
                                                    authSource='admin',
                                                    authMechanism='SCRAM-SHA-256')

    db = client['cpes']
    collection = db['data_test']
    print('consum time:' + str(time() - t))
    return collection


if __name__ == '__main__':

    # loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(loop)
    # DBclient = motor.motor_asyncio.AsyncIOMotorClient('mongodb://192.168.1.10/',
    #                                                   username='zgl',
    #                                                   password='123456',
    #                                                   authSource='admin',
    #                                                   authMechanism='SCRAM-SHA-256')
    #
    # db = DBclient['cpes']
    # collection = db['data_test']

    executors1 = {
        'default': ThreadPoolExecutor(20),
        'processpool': ProcessPoolExecutor(5)
    }

    executors2 = {
        'default': AsyncIOExecutor()
    }

    loop, client = ModbusClient(schedulers.ASYNC_IO, port=5020)

    scheduler = AsyncIOScheduler()  # executors=executors1
    # scheduler = BackgroundScheduler(executors=executors2)
    # scheduler.add_job(tick, 'interval', seconds=3)
    # scheduler.add_job(createOneAsyn, 'interval', args=[collection], seconds=3)
    scheduler.add_job(start_async_test, 'interval', args=[client.protocol], seconds=3)
    scheduler.add_job(countAsyn, 'interval', seconds=3)
    scheduler.start()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    # Execution will block here until Ctrl+C (Ctrl+Break on Windows) is pressed.
    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass
