'''
tcp同步
'''
import logging
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.transaction import ModbusRtuFramer as ModbusFramer
# from pymodbus.transaction import ModbusSocketFramer as ModbusFramer
from pymodbus.constants import Defaults as Set
from time import sleep

# from pymodbus.client.sync import ModbusUdpClient as ModbusClient
# from pymodbus.client.sync import ModbusSerialClient as ModbusClient

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

UNIT = 0x1
# Set.TransactionId = 0x1500
# Set.ProtocolId = 0

try:
    client = ModbusClient('192.168.1.82', port=1035, timeout=3, framer=ModbusFramer)#
    # from pymodbus.transaction import ModbusRtuFramer
    # client = ModbusClient('localhost', port=5020, framer=ModbusRtuFramer)
    # client = ModbusClient(method='binary', port='/dev/ptyp0', timeout=1)
    # client = ModbusClient(method='ascii', port='/dev/ptyp0', timeout=1)
    # client = ModbusClient(method='rtu', port='COM2', timeout=1,
    #                       baudrate=115200)
    # client = ModbusClient(method='rtu', port='COM2', timeout=1, baudrate=115200)
    client.connect()

    # log.debug("Write to a Coil and read back")
    # rq = client.write_coil(0, True, unit=UNIT)
    # rr = client.read_coils(0, 1, unit=UNIT)
    # assert(not rq.isError())     # test that we are not an error
    # assert(rr.bits[0] == True)          # test the expected value

    # log.debug("Write to multiple coils and read back- test 1")
    # rq = client.write_coils(1, [True]*8, unit=UNIT)
    # assert(not rq.isError())     # test that we are not an error
    # rr = client.read_coils(1, 21, unit=UNIT)
    # assert(not rr.isError())     # test that we are not an error
    # resp = [True]*21

    # resp.extend([False]*3)
    # assert(rr.bits == resp)         # test the expected value

    # log.debug("Write to multiple coils and read back - test 2")
    # rq = client.write_coils(1, [False]*8, unit=UNIT)
    # rr = client.read_coils(1, 8, unit=UNIT)
    # assert(not rq.isError())     # test that we are not an error
    # assert(rr.bits == [False]*8)         # test the expected value

    # log.debug("Read discrete inputs")
    # rr = client.read_discrete_inputs(0, 8, unit=UNIT)
    # assert(not rq.isError())     # test that we are not an error

    # log.debug("Write to a holding register and read back")
    # rq = client.write_register(1, 10, unit=UNIT)
    # rr = client.read_holding_registers(1, 1, unit=UNIT)
    # assert(not rq.isError())     # test that we are not an error
    # assert(rr.registers[0] == 10)       # test the expected value

    # log.debug("Write to multiple holding registers and read back")
    # rq = client.write_registers(1, [10]*8, unit=UNIT)
    # rr = client.read_holding_registers(1, 8, unit=UNIT)
    # assert(not rq.isError())     # test that we are not an error
    # assert(rr.registers == [10]*8)      # test the expected value

    # log.debug("Read input registers")
    # rr = client.read_input_registers(1, 8, unit=UNIT)
    # assert(not rq.isError())     # test that we are not an error

    # arguments = {
    #     'read_address': 1,
    #     'read_count': 8,
    #     'write_address': 1,
    #     'write_registers': 8,
    # }
    # log.debug("Read write registeres simulataneously")
    # rq = client.readwrite_registers(unit=UNIT, **arguments)

    # log.debug("Read write registers simulataneously")
    adress_register = 0x00  # 起始寄存器
    length_data = 0x06 # 数据长度
    adress_gateway = 0x01  # 通讯地址
    rr = client.read_holding_registers(adress_register, length_data, unit=adress_gateway)
    # rr = client.read_coils(adress_register, length_data, unit=adress_gateway)
    print(['{:04X}'.format(rx) for rx in rr.registers])
    print(rr.registers)
    # print([int(rx) for rx in rr.bits])

    # data_all = []
    # for gate in range(8):
    #     rr = client.read_holding_registers(adress_register, length_data, unit=gate+1)
    #     data_all.append(rr.registers)
    #     sleep(1)




    # log.debug("Read write registers simulataneously")
    # adress_register = 64  # 起始寄存器
    # length_data = 0x04  # 数据长度
    # adress_gateway = 0x01  # 云盒地址
    # # rr = client.read_holding_registers(adress_register, length_data, unit=adress_gateway)
    # data_all = []
    # for i in range(14):
    #     rr = client.read_holding_registers(adress_register*i, length_data, unit=adress_gateway)
    #     # rr_hex = hex(rr.registers[0])
    #     # type = rr_hex[2:4]
    #     # sign = rr_hex[4:5]
    #     # pos = int(rr_hex[5:6])
    #
    #     # rr_hex = '{:04X}'.format(rr.registers[0])
    #     rr_hex = ['{:04X}'.format(rx) for rx in rr.registers]
    #     # type = rr_hex[0:2]
    #     # sign = rr_hex[2:3]
    #     # pos = int(rr_hex[3:4])
    #     # data = {}
    #     # if type == '81':
    #     #     data['type'] = 'level'
    #     # elif type == '01':
    #     #     data['type'] = 'temperature'
    #     # else:
    #     #     print(' illegal type')
    #     #     # Exception
    #     # if sign == '0':
    #     #     data['data'] = rr.registers[1]/(10**pos)
    #     # elif sign == '8':
    #     #     data_origin = rr.registers[1]
    #     #     if data_origin >= 32767:
    #     #         data['d ata'] = -(65536 - rr.registers[1]) / (10 ** pos)
    #     #     # data['data'] = -(65536-rr.registers[1])/(10**pos)
    #     #     else:
    #     #         data['data'] = rr.registers[1] / (10 ** pos)
    #     # else:
    #     #     print('illegal sign')
    #     #     # raise ValueError
    #     # data_all.append(data)
    #     print('rr'+str(i)+': %s' % repr(rr_hex))
    #     sleep(1)





        # print(len(rr.registers))
    # rr = client.read_input_registers(adress_register, length_data, unit=adress_gateway)
    # rr = client.read_discrete_inputs(adress_register, length_data, unit=adress_gateway)

    # rr = client.read_holding_registers(1, 8, unit=UNIT)
    # assert(not rq.isError())     # test that we are not an error
    # assert(rq.registers == [20]*8)      # test the expected value
    # assert(rr.registers == [20]*8)      # test the expected value

    client.close()
except Exception as e:
    log.exception(e)
    client.close()