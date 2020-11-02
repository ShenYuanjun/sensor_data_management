'''
传感器序列号
'''
import logging
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
# from pymodbus.transaction import ModbusRtuFramer as ModbusFramer
# from pymodbus.constants import Defaults as Set
# from time import sleep

# from pymodbus.client.sync import ModbusUdpClient as ModbusClient
# from pymodbus.client.sync import ModbusSerialClient as ModbusClient

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

UNIT = 0x1

try:
    client = ModbusClient('192.168.1.82', port=1036)
    client.connect()


    log.debug("Read write registers simulataneously")
    adress_register = 0x0000  # 起始寄存器
    adress_increment = 0x40
    length_data = 0x08  # 数据长度
    adress_gateway = 0x01  # 云盒地址

    serialNumber = []
    for i in range(14):
        rr = client.read_holding_registers(adress_register+adress_increment*i, length_data, unit=adress_gateway)
        serialNumber.append(['{:04X}'.format(rx) for rx in rr.registers])
        print(rr.registers)


    # rr = client.read_holding_registers(adress_register, length_data, unit=adress_gateway)
    # print(rr.registers)


    client.close()
except Exception as e:
    log.exception(e)
    client.close()