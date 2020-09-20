# import asyncio
# import os
# from datetime import datetime
# # import logging
#
# from apscheduler.schedulers.asyncio import AsyncIOScheduler
# import motor.motor_asyncio
# import asyncio
# from pymodbus.client.asynchronous.serial import AsyncModbusSerialClient as ModbusClient
# from pymodbus.client.asynchronous import schedulers
#
# UNIT = 0x01
#
# async def start_async_test(client):
#     try:
#
#         rq = await client.write_register(1, 10, unit=UNIT)
#         rr = await client.read_holding_registers(1, 1, unit=UNIT)
#         # assert(rq.function_code < 0x80)     # test that we are not an error
#         # assert(rr.registers[0] == 10)       # test the expected value
#
#         rq = await client.write_registers(1, [10]*8, unit=UNIT)
#         rr = await client.read_holding_registers(1, 8, unit=UNIT)
#         # assert(rq.function_code < 0x80)     # test that we are not an error
#         # assert(rr.registers == [10]*8)      # test the expected value
#
#         arguments = {
#             'read_address':    1,
#             'read_count':      8,
#             'write_address':   1,
#             'write_registers': [20]*8,
#         }
#         # log.debug("Read write registers simulataneously")
#         rq = await client.readwrite_registers(unit=UNIT, **arguments)
#         rr = await client.read_holding_registers(1, 8, unit=UNIT)
#         print(rr.registers)
#     except Exception as e:
#         client.transport.close()
#     await asyncio.sleep(1)
#
# async def start_async_demo(client):
#     try:
#         arguments = {
#             'read_address':    1,
#             'read_count':      8,
#             'write_address':   1,
#             'write_registers': [20]*8,
#         }
#         rq = await client.readwrite_registers(unit=UNIT, **arguments)
#         rr = await client.read_holding_registers(1, 8, unit=UNIT)
#         document = {'rq': rq.registers, 'rr': rr.registers, "time": datetime.now()}
#         print('rq: %s' % repr(rq.registers))
#         print('rr: %s' % repr(rr.registers))
#         # result = await collection.insert_one(document)
#         # print('inserted: %s' % repr(result.inserted_id))
#     except Exception as e:
#         client.transport.close()
#     await asyncio.sleep(1)
#
# async def countAsyn(collection):
#     # collection = await DBconnect()
#     all = await collection.count_documents({})
#     print("There is/are " + str(all) + " document(s)")
#
# if __name__ == '__main__':
#
#     loop, client = ModbusClient(schedulers.ASYNC_IO, port='COM2', baudrate=115200, method="rtu")
#     # DBclient = motor.motor_asyncio.AsyncIOMotorClient('mongodb://192.168.1.10/',
#     #                                                   username='zgl',
#     #                                                   password='123456',
#     #                                                   authSource='admin',
#     #                                                   authMechanism='SCRAM-SHA-256'
#     #                                                   )#io_loop=loop
#     # db = DBclient['cpes']
#     # collection = db['data_test']
#     scheduler = AsyncIOScheduler()
#
#     scheduler.add_job(start_async_test, 'interval', args=[client.protocol], seconds=3, max_instances=10)
#     # scheduler.add_job(countAsyn, 'interval', args=[collection], seconds=3)
#     scheduler.start()
#     print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
#
#     # Execution will block here until Ctrl+C (Ctrl+Break on Windows) is pressed.
#     try:
#         asyncio.get_event_loop().run_forever()
#     except (KeyboardInterrupt, SystemExit):
#         pass




import logging
import asyncio
from pymodbus.client.asynchronous.serial import (
    AsyncModbusSerialClient as ModbusClient)
from pymodbus.client.asynchronous import schedulers

# --------------------------------------------------------------------------- #
# configure the client logging
# --------------------------------------------------------------------------- #
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)


# --------------------------------------------------------------------------- #
# specify slave to query
# --------------------------------------------------------------------------- #
# The slave to query is specified in an optional parameter for each
# individual request. This can be done by specifying the `unit` parameter
# which defaults to `0x00`
# --------------------------------------------------------------------------- #


UNIT = 0x01


async def start_async_test(client):
    # ----------------------------------------------------------------------- #
    # specify slave to query
    # ----------------------------------------------------------------------- #
    # The slave to query is specified in an optional parameter for each
    # individual request. This can be done by specifying the `unit` parameter
    # which defaults to `0x00`
    # ----------------------------------------------------------------------- #
    try:
    # ----------------------------------------------------------------------- #
        # example requests
    # ----------------------------------------------------------------------- #
        # simply call the methods that you would like to use.
        # An example session is displayed below along with some assert checks.
        # Note that some modbus implementations differentiate holding/
        # input discrete/coils and as such you will not be able to write to
        # these, therefore the starting values are not known to these tests.
        # Furthermore, some use the same memory blocks for the two sets,
        # so a change to one is a change to the other.
        # Keep both of these cases in mind when testing as the following will
        # _only_ pass with the supplied asynchronous modbus server (script supplied).
    # ----------------------------------------------------------------------- #
    #     log.debug("Write to a Coil and read back")
    #     rq = await client.write_coil(0, True, unit=UNIT)
    #     rr = await client.read_coils(0, 1, unit=UNIT)
    #     assert(rq.function_code < 0x80)     # test that we are not an error
    #     assert(rr.bits[0] == True)          # test the expected value

        # log.debug("Write to multiple coils and read back- test 1")
        # rq = await client.write_coils(1, [True]*8, unit=UNIT)
        # assert(rq.function_code < 0x80)     # test that we are not an error
        # rr = await client.read_coils(1, 21, unit=UNIT)
        # assert(rr.function_code < 0x80)     # test that we are not an error
        # resp = [True]*21

        # If the returned output quantity is not a multiple of eight,
        # the remaining bits in the final data byte will be padded with zeros
        # (toward the high order end of the byte).

        # resp.extend([False]*3)
        # assert(rr.bits == resp)         # test the expected value

        # log.debug("Write to multiple coils and read back - test 2")
        # rq = await client.write_coils(1, [False]*8, unit=UNIT)
        # rr = await client.read_coils(1, 8, unit=UNIT)
        # assert(rq.function_code < 0x80)     # test that we are not an error
        # assert(rr.bits == [False]*8)         # test the expected value

        # log.debug("Read discrete inputs")
        # rr = await client.read_discrete_inputs(0, 8, unit=UNIT)
        # assert(rq.function_code < 0x80)     # test that we are not an error

        # log.debug("Write to a holding register and read back")
        # rq = await client.write_register(1, 10, unit=UNIT)
        # rr = await client.read_holding_registers(1, 1, unit=UNIT)
        # assert(rq.function_code < 0x80)     # test that we are not an error
        # assert(rr.registers[0] == 10)       # test the expected value

        # log.debug("Write to multiple holding registers and read back")
        # rq = await client.write_registers(1, [10]*8, unit=UNIT)
        # rr = await client.read_holding_registers(1, 8, unit=UNIT)
        # assert(rq.function_code < 0x80)     # test that we are not an error
        # assert(rr.registers == [10]*8)      # test the expected value

        # log.debug("Read input registers")
        # rr = await client.read_input_registers(1, 8, unit=UNIT)
        # assert(rq.function_code < 0x80)     # test that we are not an error

        arguments = {
            'read_address':    1,
            'read_count':      8,
            'write_address':   1,
            'write_registers': [20]*8,
        }
        log.debug("Read write registers simulataneously")
        # rq = await client.readwrite_registers(unit=UNIT, **arguments)
        # rr = await client.read_holding_registers(1, 8, unit=UNIT)
        adress_register = 0  # 起始寄存器
        length_data = 64  # 数据长度 HEX=40
        adress_gateway = 0x1  # 云盒地址
        rr = await client.read_holding_registers(adress_register, length_data, unit=adress_gateway)
        print('rr: %s' % repr(rr.registers))
        print(len(rr.registers))
        # assert(rq.function_code < 0x80)     # test that we are not an error
        # assert(rq.registers == [20]*8)      # test the expected value
        # assert(rr.registers == [20]*8)      # test the expected value
    except Exception as e:
        log.exception(e)
        client.transport.close()
    await asyncio.sleep(1)


if __name__ == '__main__':
    # ----------------------------------------------------------------------- #
    # For testing on linux based systems you can use socat to create serial
    # ports
    # ----------------------------------------------------------------------- #
    # socat -d -d PTY,link=/tmp/ptyp0,raw,echo=0,ispeed=9600 PTY,
    # link=/tmp/ttyp0,raw,echo=0,ospeed=9600
    loop, client = ModbusClient(schedulers.ASYNC_IO, port='COM2',
                                baudrate=115200, method="rtu")
    loop.run_until_complete(start_async_test(client.protocol))
    loop.close()


