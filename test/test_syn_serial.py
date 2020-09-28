'''
    串口同步
'''
import logging
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.constants import Defaults as Set

# from pymodbus.client.sync import ModbusUdpClient as ModbusClient
# from pymodbus.client.sync import ModbusSerialClient as ModbusClient

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

UNIT = 0x1
Set.TransactionId = 0x1500

client = ModbusClient('192.168.1.82', port=1032, method='rtu')
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

arguments = {
    'read_address': 1,
    'read_count': 8,
    'write_address': 1,
    'write_registers': 8,
}
# log.debug("Read write registeres simulataneously")
# rq = client.readwrite_registers(unit=UNIT, **arguments)
log.debug("Read registers")
adress_register = 0  # 起始寄存器
length_data = 64  # 数据长度 HEX=40
adress_gateway = 0x1  # 云盒地址
rr = client.read_holding_registers(adress_register, length_data, unit=adress_gateway)
print('rr: %s' % repr(rr.registers))
print(len(rr.registers))
# rr = client.read_input_registers(adress_register, length_data, unit=adress_gateway)
# rr = client.read_discrete_inputs(adress_register, length_data, unit=adress_gateway)

# rr = client.read_holding_registers(1, 8, unit=UNIT)
# assert(not rq.isError())     # test that we are not an error
# assert(rq.registers == [20]*8)      # test the expected value
# assert(rr.registers == [20]*8)      # test the expected value

client.close()
