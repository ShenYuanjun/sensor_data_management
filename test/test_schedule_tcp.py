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

UNIT = 0x00

async def start_async_test(collection, clients):

    # arguments = {
    #     'read_address': 1,
    #     'read_count': 8,
    #     'write_address': 1,
    #     'write_registers': [20] * 8,
    # }
    t = time.time()
    # rq = await client.readwrite_registers(unit=UNIT, **arguments)

    adress_register = 64  # 起始寄存器
    length_data = 0x04  # 数据长度
    adress_gateway = 0x01  # 云盒地址
    data_all = []
    for client in clients:
        for i in range(14):
            rr = await client.read_holding_registers(adress_register * i, length_data, unit=adress_gateway)
            # print('rr: %s' % repr(rr))
            rr_hex = ['{:04X}'.format(rx) for rx in rr.registers]
            data_all.append(rr_hex)
    document = {'data': data_all, "time": datetime.now()}
    result = await collection.insert_one(document)
    # adress_register = 0  # 起始寄存器
    # length_data = 0x40  # 数据长度 HEX=
    # adress_gateway = 0x1  # 云盒地址
    # rr = await client.read_holding_registers(adress_register, length_data, unit=adress_gateway)
    # # rr = await client.read_holding_registers(1, 8, unit=UNIT)
    #
    # document = {'data': rr.registers, "time": datetime.now()}
    # result = await collection.insert_one(document)
    # print('inserted: %s' % repr(result.inserted_id))

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
    new_loop, client1 = ModbusClient(schedulers.ASYNC_IO, host='192.168.1.82', port=1030, loop=loop, method='tcp')
    new_loop, client2 = ModbusClient(schedulers.ASYNC_IO, host='192.168.1.82', port=1031, loop=loop, method='tcp')
    new_loop, client3 = ModbusClient(schedulers.ASYNC_IO, host='192.168.1.82', port=1032, loop=loop, method='tcp')
    new_loop, client4 = ModbusClient(schedulers.ASYNC_IO, host='192.168.1.82', port=1033, loop=loop, method='tcp')
    new_loop, client5 = ModbusClient(schedulers.ASYNC_IO, host='192.168.1.82', port=1034, loop=loop, method='tcp')
    clients1 = [client1.protocol, client2.protocol, client3.protocol]
    clients2 = [client4.protocol, client5.protocol]
    DBclient = motor.motor_asyncio.AsyncIOMotorClient('mongodb://192.168.1.10/',
                                                      username='zgl',
                                                      password='123456',
                                                      authSource='admin',
                                                      authMechanism='SCRAM-SHA-256',
                                                      io_loop=loop)
    db = DBclient['cpes']
    collection = db['data_test']
    scheduler = AsyncIOScheduler()

    scheduler.add_job(start_async_test, 'interval', args=[collection, clients1], seconds=5)
    scheduler.add_job(start_async_test, 'interval', args=[collection, clients2], seconds=5)
    scheduler.add_job(countAsyn, 'interval', args=[collection], seconds=10)
    scheduler.start()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    # Execution will block here until Ctrl+C (Ctrl+Break on Windows) is pressed.
    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass
