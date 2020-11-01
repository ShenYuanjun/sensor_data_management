'''
环境质量数据读取并写入数据库
'''

import asyncio
import os
from datetime import datetime
import time

import addressing as ads


async def env_modbus2mongodb(collection, client, bus):
    t = time.time()

    for box in range(ads.busBox(bus - 1), ads.busBox(bus)):  # 云盒编号
        rr = await client.read_holding_registers(ads.rgs, ads.len_data, unit=box)
        data_modbus = rr.registers
        for i in range(ads.box_num[box][0]):  # 二合一编号
            pos_two = ads.two_start + ads.two_len * i
            if pos_two+ads.pos_name == box*256+i:
                data_db = {'name': '{:0>2d}{:0>2d}{:0>2d}'.format(bus, box, i),
                           'two_in_one': {ads.two_type[j]: data_modbus[pos_two + ads.pos_data + j] / 10
                                          for j in range(2)},
                           'datetime': datetime.now()}
            else:
                data_db = {'name': '{:0>2d}{:0>2d}{:0>2d}'.format(bus, box, i),
                           'data': data_modbus,
                           'err': 'Unexpected Data Received',
                           'datetime': datetime.now()}
            result = await collection.insert_one(data_db)

        for i in range(ads.box_num[box][1]):  # 六合一编号
            pos_six = ads.six_start + ads.six_len * i
            if pos_six+ads.pos_name == box*256+i+ads.six_bios:
                data_db = {'name': '{:0>2d}{:0>2d}{:0>2d}'.format(bus, box, i),
                           'six_in_one': {ads.six_type[j]: data_modbus[pos_six + ads.pos_data + j] / 10
                                          for j in range(6)},
                           'datetime': datetime.now()}
            else:
                data_db = {'name': '{:0>2d}{:0>2d}{:0>2d}'.format(bus, box, i),
                           'data': data_modbus,
                           'err': 'Unexpected Data Received',
                           'datetime': datetime.now()}
            result = await collection.insert_one(data_db)

    await asyncio.sleep(1)
    print('time consuming: ', time.time() - t)




adress_register = 0x40  # 起始寄存器
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
print('time consuming: ', time.time() - t)
