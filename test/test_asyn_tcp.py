'''
tcp异步
'''
import asyncio
import logging
# ----------------------------------------------------------------------- #
# Import the required asynchronous client
# ----------------------------------------------------------------------- #
from pymodbus.client.asynchronous.tcp import AsyncModbusTCPClient as ModbusClient
# from pymodbus.client.asynchronous.udp import AsyncModbusUDPClient as ModbusClient
from pymodbus.client.asynchronous import schedulers
# from pymodbus.constants import Defaults as Set
from pymodbus.transaction import ModbusRtuFramer as ModbusFramer
# from pymodbus.transaction import ModbusSocketFramer as ModbusFramer


from threading import Thread
import time
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
# Set.TransactionId = 0x1500

async def start_async_test(client):

    # log.debug("Reading Coils")
    # rr = await client.read_coils(1, 1, unit=0x01)

    # log.debug("Write to a Coil and read back")
    # rq = await client.write_coil(0, True, unit=UNIT)
    # rr = await client.read_coils(0, 1, unit=UNIT)
    # assert(rq.function_code < 0x80)     # test that we are not an error
    # assert(rr.bits[0] == True)          # test the expected value

    # log.debug("Write to multiple coils and read back- test 1")
    # rq = await client.write_coils(1, [True]*8, unit=UNIT)
    # assert(rq.function_code < 0x80)     # test that we are not an error
    # rr = await client.read_coils(1, 21, unit=UNIT)
    # assert(rr.function_code < 0x80)     # test that we are not an error
    # resp = [True]*21
    #
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

    # arguments = {
    #     'read_address':    1,
    #     'read_count':      8,
    #     'write_address':   1,
    #     'write_registers': [20]*8,
    # }
    log.debug("Read write registeres simulataneously")
    # rq = await client.readwrite_registers(unit=UNIT, **arguments)
    # rr = await client.read_holding_registers(1, 8, unit=UNIT)
    adress_register = 0x40  # 起始寄存器
    length_data = 0x08  # 数据长度 HEX=
    adress_gateway = 0x1  # 云盒地址

    serialNumber = []
    for i in range(14):
        rr = await client.read_holding_registers(adress_register*i, length_data, unit=adress_gateway)#, transaction=0x15
        serialNumber.append(['{:04X}'.format(rx) for rx in rr.registers])
    print(serialNumber)
    # rr = await client.read_holding_registers(adress_register, length_data, unit=adress_gateway)  # , transaction=0x15
    # print('rr: %s' % repr(rr.registers))
    # print(len(rr.registers))
    # assert rr
    # assert(rq.function_code < 0x80)     # test that we are not an error
    # assert(rq.registers == [20]*8)      # test the expected value
    # assert(rr.registers == [20]*8)      # test the expected value
    await asyncio.sleep(1)


def run_with_not_running_loop():
    """
    A loop is created and is passed to ModbusClient factory to be used.

    :return:
    """
    log.debug("Running Async client with asyncio loop not yet started")
    log.debug("------------------------------------------------------")
    loop = asyncio.new_event_loop()
    assert not loop.is_running()
    asyncio.set_event_loop(loop)
    new_loop, client = ModbusClient(schedulers.ASYNC_IO, host='192.168.1.82', port=1038, loop=loop)#, framer=ModbusFramer
    loop.run_until_complete(start_async_test(client.protocol))
    loop.close()
    log.debug("--------------RUN_WITH_NOT_RUNNING_LOOP---------------")
    log.debug("")


def run_with_already_running_loop():
    """
    An already running loop is passed to ModbusClient Factory
    :return:
    """
    log.debug("Running Async client with asyncio loop already started")
    log.debug("------------------------------------------------------")

    def done(future):
        log.info("Done !!!")

    def start_loop(loop):
        """
        Start Loop
        :param loop:
        :return:
        """
        asyncio.set_event_loop(loop)
        loop.run_forever()

    loop = asyncio.new_event_loop()
    t = Thread(target=start_loop, args=[loop])
    t.daemon = True
    # Start the loop
    t.start()
    assert loop.is_running()
    asyncio.set_event_loop(loop)
    loop, client = ModbusClient(schedulers.ASYNC_IO, host='192.168.1.82', port=1030, loop=loop)
    future = asyncio.run_coroutine_threadsafe(
        start_async_test(client.protocol), loop=loop)
    future.add_done_callback(done)
    while not future.done():
        time.sleep(0.1)
    loop.stop()
    log.debug("--------DONE RUN_WITH_ALREADY_RUNNING_LOOP-------------")
    log.debug("")


def run_with_no_loop():
    """
    ModbusClient Factory creates a loop.
    :return:
    """
    log.debug("---------------------RUN_WITH_NO_LOOP-----------------")
    loop, client = ModbusClient(schedulers.ASYNC_IO, host='192.168.1.82', port=1030)
    # loop, client = ModbusClient('192.168.1.82', port=1032)
    loop.run_until_complete(start_async_test(client.protocol))
    loop.close()
    log.debug("--------DONE RUN_WITH_NO_LOOP-------------")
    log.debug("")


if __name__ == '__main__':
    # Run with No loop
    log.debug("Running Async client")
    log.debug("------------------------------------------------------")
    # print(schedulers.ASYNC_IO)
    # run_with_no_loop()

    # Run with loop not yet started
    run_with_not_running_loop()

    # Run with already running loop
    # run_with_already_running_loop()

    log.debug("")
