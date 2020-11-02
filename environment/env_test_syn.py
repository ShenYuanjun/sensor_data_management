'''
测试数据
'''
import logging
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from time import sleep
import time
import addressing as ads
from datetime import datetime
# from pymodbus.constants import Defaults as Set

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

# UNIT = 0x1
# Set.TransactionId = 0x00

try:
    # bus = 6
    # client = ModbusClient('192.168.1.82', port=1038+bus, timeout=3)
    bus = 11
    client = ModbusClient('192.168.1.83', port=1030 + bus-7, timeout=3)
    client.connect()


    data_all = []

    log.debug("Read write registers simulataneously")
    t = time.time()

    for box in range(ads.busBox[bus - 1], ads.busBox[bus]):  # 云盒编号（0开始）
        # UNIT = box + 0x01
        # Set.TransactionId = 0x00
        rr = client.read_holding_registers(ads.rgs, ads.len_data, unit=box+1)
        data_modbus = rr.registers
        for i in range(ads.box_num[box][0]):  # 二合一编号（0开始）
            pos_two = ads.two_start + ads.two_len * i
            # print('two', data_modbus[pos_two + ads.pos_name], (box+1) * 256 + i+1)
            if data_modbus[pos_two + ads.pos_name] == (box+1) * 256 + ads.two_start+i+1:
                data_db = {'name': '{:0>2d}{:0>2d}{:0>2d}'.format(bus, box+1, i+1),
                           'two_in_one': {ads.two_type[j]: data_modbus[pos_two + ads.pos_data + j] / 10
                                          for j in range(2)},
                           'datetime': datetime.now()}
            else:
                data_db = {'name': '{:0>2d}{:0>2d}{:0>2d}'.format(bus, box+1, i+1),
                           'data': data_modbus,
                           'err': 'Unexpected Data Received',
                           'datetime': datetime.now()}
            # result = await collection.insert_one(data_db)
            data_all.append(data_db)

        for i in range(ads.box_num[box][1]):  # 六合一编号
            pos_six = ads.six_start*ads.two_len + ads.six_len * i
            # print('six', data_modbus[pos_six + ads.pos_name], (box+1) * 256 + ads.six_start+i + ads.six_bios+1)
            if data_modbus[pos_six + ads.pos_name] == (box+1) * 256 + ads.six_start+i + ads.six_bios+1:
                data_db = {'name': '{:0>2d}{:0>2d}{:0>2d}'.format(bus, box+1, i+1),
                           'six_in_one': {ads.six_type[j]: data_modbus[pos_six + ads.pos_data + j] / 10
                                          for j in range(6)},
                           'datetime': datetime.now()}
            else:
                data_db = {'name': '{:0>2d}{:0>2d}{:0>2d}'.format(bus, box+1, i+1),
                           'data': data_modbus,
                           'err': 'Unexpected Data Received',
                           'datetime': datetime.now()}
            # result = await collection.insert_one(data_db)
            data_all.append(data_db)

        sleep(1)
    print('time consuming: ', time.time() - t)

    client.close()
except Exception as e:
    log.exception(e)
    client.close()
