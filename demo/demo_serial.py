import asyncio
import os
from datetime import datetime
# import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
import motor.motor_asyncio
import asyncio
from pymodbus.client.asynchronous.serial import AsyncModbusSerialClient as ModbusClient
from pymodbus.client.asynchronous import schedulers

UNIT = 0x01

async def start_async_test(client):
    try:

        rq = await client.write_register(1, 10, unit=UNIT)
        rr = await client.read_holding_registers(1, 1, unit=UNIT)
        # assert(rq.function_code < 0x80)     # test that we are not an error
        # assert(rr.registers[0] == 10)       # test the expected value

        rq = await client.write_registers(1, [10]*8, unit=UNIT)
        rr = await client.read_holding_registers(1, 8, unit=UNIT)
        # assert(rq.function_code < 0x80)     # test that we are not an error
        # assert(rr.registers == [10]*8)      # test the expected value

        arguments = {
            'read_address':    1,
            'read_count':      8,
            'write_address':   1,
            'write_registers': [20]*8,
        }
        # log.debug("Read write registers simulataneously")
        rq = await client.readwrite_registers(unit=UNIT, **arguments)
        rr = await client.read_holding_registers(1, 8, unit=UNIT)
        print(rr.registers)
    except Exception as e:
        client.transport.close()
    await asyncio.sleep(1)

async def start_async_demo(collection, client):
    try:
        arguments = {
            'read_address':    1,
            'read_count':      8,
            'write_address':   1,
            'write_registers': [20]*8,
        }
        rq = await client.readwrite_registers(unit=UNIT, **arguments)
        rr = await client.read_holding_registers(1, 8, unit=UNIT)
        document = {'rq': rr.registers, 'rr': rr.registers, "time": datetime.now()}
        result = await collection.insert_one(document)
        print('inserted: %s' % repr(result.inserted_id))
    except Exception as e:
        client.transport.close()
    await asyncio.sleep(1)

async def countAsyn(collection):
    # collection = await DBconnect()
    all = await collection.count_documents({})
    print("There is/are " + str(all) + " document(s)")

if __name__ == '__main__':

    loop, client = ModbusClient(schedulers.ASYNC_IO, port='COM2', baudrate=9600, method="rtu")
    DBclient = motor.motor_asyncio.AsyncIOMotorClient('mongodb://192.168.1.10/',
                                                      username='zgl',
                                                      password='123456',
                                                      authSource='admin',
                                                      authMechanism='SCRAM-SHA-256'
                                                      )#io_loop=loop
    db = DBclient['cpes']
    collection = db['data_test']
    scheduler = AsyncIOScheduler()

    scheduler.add_job(start_async_demo, 'interval', args=[collection, client.protocol], seconds=3)
    scheduler.add_job(countAsyn, 'interval', args=[collection], seconds=3)
    scheduler.start()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    # Execution will block here until Ctrl+C (Ctrl+Break on Windows) is pressed.
    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass
