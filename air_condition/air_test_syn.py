'''
测试数据
'''
# import asyncio
import os
# from datetime import datetime
from time import sleep, time

# from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.schedulers.background import BackgroundScheduler
# from apscheduler.jobstores.mongodb import MongoDBJobStore
# import motor.motor_asyncio
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.transaction import ModbusRtuFramer as ModbusFramer
import addressing as ads
from datetime import datetime

import logging

logging.basicConfig(filename='air_log1111.log', level=logging.INFO)  # WARNING DEBUG
log = logging.getLogger()

def air_modbus2mongodb_next():
    try:
        t = time()

        DBclient = MongoClient('mongodb://192.168.1.10/',
                               username='sensorManager',
                               password='manage123456',
                               authSource='admin',
                               serverSelectionTimeoutMS=2000)

        try:  # 数据库连接测试
            # The ismaster command is cheap and does not require auth.
            DBclient.admin.command('ismaster')
        except ConnectionFailure as e:  # Exception
            DBclient.close()
            log.error(e)
            # print("Server not available")
            return

        db = DBclient['sensor_management']
        # collection = db['air_condition']
        collection = db['data_test_air_']
        logger = db['air_condition_logger']

        equipments = [{} for i in range(9)]
        for i in range(9):  # 9根总线读数据
            client = ModbusClient(ads.conn[i][0], port=ads.conn[i][1], timeout=3)
            bus = ads.buses[i]

            is_connected = client.connect()
            if not is_connected:  # modbus连接失败
                data_db = {'name': 'bus{:0>1d}'.format(i + 1),
                           'err': 'Modbus Connect Failed',
                           'datetime': datetime.now()}
                result = logger.insert_one(data_db)
                client.close()
                sleep(1)
                continue

            for j in range(ads.bus_sensor_number[i]):
                rr = client.read_holding_registers(ads.rgs_start + j * ads.rgs_len, ads.len_data, unit=ads.box_ads)
                if not hasattr(rr, 'registers'):  # 无返回数据
                    data_db = {'name': 'bus{:0>1d}:'.format(i + 1) + ads.equipment_index[i] + '-' + bus[j][1],
                               'message': rr.message,
                               'err': 'No Data Return',
                               'datetime': datetime.now()}
                    result = logger.insert_one(data_db)
                    continue

                data_modbus = rr.registers
                type = data_modbus[0] // 256  # 数据类型
                if type != bus[j][2]:
                    data_db = {'name': 'bus{:0>1d}:'.format(i + 1) + ads.equipment_index[i] + '-' + bus[j][1],
                               'data': data_modbus,
                               'err': 'Wrong Type Index: Should be 0x{:0X}, but accepted 0x{:0X}'.format(bus[j][2],
                                                                                                         type),
                               'datetime': datetime.now()}
                    result = logger.insert_one(data_db)
                    continue
                pos = data_modbus[0] % 16  # 小数位数
                sign_n = data_modbus[0] % 256 - pos  ## 有无符号
                if sign_n == 0x80:
                    sign = True  # 有符号
                elif sign_n == 0x00:
                    sign = False  # 无符号
                else:
                    data_db = {'name': 'bus{:0>1d}:'.format(i + 1) + ads.equipment_index[i] + '-' + bus[j][1],
                               'data': data_modbus,
                               'err': 'Wrong Sign Index: Should be 0x{:0X} or 0x{:0X}, but accepted 0x{:0X}'.format(
                                   0x80, 0x00, sign_n),
                               'datetime': datetime.now()}
                    result = logger.insert_one(data_db)
                    continue

                data_origin = data_modbus[1]
                if sign and data_origin >= 32767:
                    data = -(65536 - data_origin) / (10 ** pos)
                else:
                    data = data_origin / (10 ** pos)

                # equipments[bus[j][1]] = data
                # equipments[ads.equipment_index[bus[j][0]]][bus[j][1]] = data
                equipments[bus[j][0]][bus[j][1]] = data
            client.close()

        for eqt in range(9):  # 9个设备写入数据库
            data_db = {'name': ads.equipment_index[eqt],
                       'data': equipments[eqt],
                       'datetime': datetime.now()}
            result = collection.insert_one(data_db)

        DBclient.close()
        log.info('Time Consuming: ' + str(time() - t))
    except Exception as e:
        # log.exception(e)
        # client.close()
        # DBclient.close()
        log.error(e)
        log.info('Time Consuming: ' + str(time() - t))
        return


if __name__ == '__main__':

    # while ((datetime.now().minute) % 5 != 0):
    #     time.sleep(1)

    # jobstores = {
    #     'mongo': MongoDBJobStore(database='sensor_management', collection='jobs', client=DBclient),
    # }
    job_defaults = {
        'coalesce': True,
        'misfire_grace_time': 120,
        'max_instances': 3
    }
    scheduler = BackgroundScheduler(job_defaults=job_defaults)  # jobstores=jobstores
    scheduler.add_job(air_modbus2mongodb_next, 'interval', seconds=300, id='env_bus2db',
                      replace_existing=True)  # , jobstore='mongo'
    scheduler.start()
    log.info('Start Time: ' + str(datetime.now()))
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            sleep(10)
    # except (KeyboardInterrupt, SystemExit):
    except Exception as e:
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown()
        log.error(e)
        log.info('End Time: ' + str(datetime.now()))








# try:
#     t = time.time()
#
#     # equipments = {ix:{} for ix in ads.equipment_index}
#     equipments = [{} for i in range(9)]
#     for i in range(9):  # 9根总线读数据
#         client = ModbusClient(ads.conn[i][0], port=ads.conn[i][1], timeout=3)
#         bus = ads.buses[i]
#
#     for eqt in range(9):  # 9个设备写入数据库
#         pass
#
#     print('time consuming: ', time.time() - t)
# except Exception as e:
#     log.exception(e)
#
#
# async def air_modbus2mongodb(collection, clients, set):
#     equipments = {}
#     for i in ads.equipmentN[set]:
#         equipments[ads.equipment_index[i]] = {}
#
#     for i in range(len(clients)):
#         client = clients[i]
#         bus_i = ads.busN[set][i]
#         bus = ads.buses[bus_i]
#
#         for j in range(ads.bus_sensor_number[bus_i]):
#             rr = await client.read_holding_registers(ads.rgs_start + j * ads.rgs_len, ads.len_data, unit=ads.box_ads)
#
#             if not hasattr(rr, 'registers'):
#                 # err
#                 continue
#
#             data_modbus = rr.registers
#             type = data_modbus[0] // 256  # 数据类型
#             if type != bus[j][2]:
#                 # err
#                 continue
#
#             pos = data_modbus[0] % 16  # 小数位数
#             sign_n = data_modbus[0] % 256 - pos  ## 有无符号
#             if sign_n == 0x80:
#                 sign = True  # 有符号
#             elif sign_n == 0x00:
#                 sign = False  # 无符号
#             else:
#                 # err
#                 continue
#
#             data_origin = data_modbus[1]
#             if sign and data_origin >= 32767:
#                 data = -(65536 - data_origin) / (10 ** pos)
#             else:
#                 data = data_origin / (10 ** pos)
#
#             # equipments[bus[j][1]] = data
#             equipments[ads.equipment_index[bus[j][0]]][bus[j][1]] = data
#
#     for i in ads.equipmentN[set]:
#         data_db = {'equipment': ads.equipment_index[bus_i],
#                    'data': data_modbus,
#                    'err': 'Unexpected Data Received',
#                    'datetime': datetime.now()}
#
#         # if sign == '0':
#         #     #     data['data'] = rr.registers[1]/(10**pos)
#         #     # elif sign == '8':
#         #     #     data_origin = rr.registers[1]
#         #     #     if data_origin >= 32767:
#         #     #         data['d ata'] = -(65536 - rr.registers[1]) / (10 ** pos)
#         #     #     # data['data'] = -(65536-rr.registers[1])/(10**pos)
#         #     #     else:
#         #     #         data['data'] = rr.registers[1] / (10 ** pos)
#         #     # else:
#         #     #     print('illegal sign')
#         #     #     # raise ValueError
#
#
# try:
#     timConsuming = []
#     # 水箱
#     client1 = ModbusClient('192.168.1.82', port=1030, timeout=3)
#     client1.connect()
#     log.debug("tank")
#
#     t = time.time()
#     timConsuming.append(time.time() - t)
#
#     # 房间1
#     client2 = ModbusClient('192.168.1.82', port=1031, timeout=3)
#     client2.connect()
#     client6 = ModbusClient('192.168.1.82', port=1035, timeout=3)
#     client6.connect()
#     log.debug("room1")
#
#     t = time.time()
#     timConsuming.append(time.time() - t)
#
#     # 房间3 房间4
#     client3 = ModbusClient('192.168.1.82', port=1032, timeout=3)
#     client3.connect()
#     client7 = ModbusClient('192.168.1.82', port=1036, timeout=3)
#     client7.connect()
#     log.debug("room3&room4")
#
#     t = time.time()
#     timConsuming.append(time.time() - t)
#
#     # 压缩机 VIP室 调度室 会议室前后
#     client4 = ModbusClient('192.168.1.82', port=1033, timeout=3)
#     client4.connect()
#     client5 = ModbusClient('192.168.1.82', port=1034, timeout=3)
#     client5.connect()
#     client8 = ModbusClient('192.168.1.82', port=1037, timeout=3)
#     client8.connect()
#     client9 = ModbusClient('192.168.1.82', port=1038, timeout=3)
#     client9.connect()
#     log.debug("compressor & roomVIP & roomControl & conference(front&back)")
#
#     t = time.time()
#     timConsuming.append(time.time() - t)
#
#     # for box in range(ads.busBox[bus - 1], ads.busBox[bus]):  # 云盒编号（0开始）
#     #     # UNIT = box + 0x01
#     #     # Set.TransactionId = 0x00
#     #     rr = client.read_holding_registers(ads.rgs, ads.len_data, unit=box+1)
#     #     data_modbus = rr.registers
#     #     for i in range(ads.box_num[box][0]):  # 二合一编号（0开始）
#     #         pos_two = ads.two_start + ads.two_len * i
#     #         # print('two', data_modbus[pos_two + ads.pos_name], (box+1) * 256 + i+1)
#     #         if data_modbus[pos_two + ads.pos_name] == (box+1) * 256 + ads.two_start+i+1:
#     #             data_db = {'name': '{:0>2d}{:0>2d}{:0>2d}'.format(bus, box+1, i+1),
#     #                        'two_in_one': {ads.two_type[j]: data_modbus[pos_two + ads.pos_data + j] / 10
#     #                                       for j in range(2)},
#     #                        'datetime': datetime.now()}
#     #         else:
#     #             data_db = {'name': '{:0>2d}{:0>2d}{:0>2d}'.format(bus, box+1, i+1),
#     #                        'data': data_modbus,
#     #                        'err': 'Unexpected Data Received',
#     #                        'datetime': datetime.now()}
#     #         # result = await collection.insert_one(data_db)
#     #         data_all.append(data_db)
#     #
#     #     for i in range(ads.box_num[box][1]):  # 六合一编号
#     #         pos_six = ads.six_start*ads.two_len + ads.six_len * i
#     #         # print('six', data_modbus[pos_six + ads.pos_name], (box+1) * 256 + ads.six_start+i + ads.six_bios+1)
#     #         if data_modbus[pos_six + ads.pos_name] == (box+1) * 256 + ads.six_start+i + ads.six_bios+1:
#     #             data_db = {'name': '{:0>2d}{:0>2d}{:0>2d}'.format(bus, box+1, i+1),
#     #                        'six_in_one': {ads.six_type[j]: data_modbus[pos_six + ads.pos_data + j] / 10
#     #                                       for j in range(6)},
#     #                        'datetime': datetime.now()}
#     #         else:
#     #             data_db = {'name': '{:0>2d}{:0>2d}{:0>2d}'.format(bus, box+1, i+1),
#     #                        'data': data_modbus,
#     #                        'err': 'Unexpected Data Received',
#     #                        'datetime': datetime.now()}
#     #         # result = await collection.insert_one(data_db)
#     #         data_all.append(data_db)
#     #
#     #     sleep(1)
#     print('time consuming: ', time.time() - t)
#
#     client1.close()
#     client2.close()
#     client3.close()
#     client4.close()
#     client5.close()
#     client6.close()
#     client7.close()
#     client8.close()
#     client9.close()
# except Exception as e:
#     log.exception(e)
#     client1.close()
#     client2.close()
#     client3.close()
#     client4.close()
#     client5.close()
#     client6.close()
#     client7.close()
#     client8.close()
#     client9.close()
#
#
# # log.debug("Read write registers simulataneously")
# # adress_register = 64  # 起始寄存器
# # length_data = 0x04  # 数据长度
# # adress_gateway = 0x01  # 云盒地址
# # # rr = client.read_holding_registers(adress_register, length_data, unit=adress_gateway)
# # data_all = []
# # for i in range(14):
# #     rr = client.read_holding_registers(adress_register*i, length_data, unit=adress_gateway)
# #     # rr_hex = hex(rr.registers[0])
# #     # type = rr_hex[2:4]
# #     # sign = rr_hex[4:5]
# #     # pos = int(rr_hex[5:6])
# #
# #     # rr_hex = '{:04X}'.format(rr.registers[0])
# #     rr_hex = ['{:04X}'.format(rx) for rx in rr.registers]
# #     # type = rr_hex[0:2]
# #     # sign = rr_hex[2:3]
# #     # pos = int(rr_hex[3:4])
# #     # data = {}
# #     # if type == '81':
# #     #     data['type'] = 'level'
# #     # elif type == '01':
# #     #     data['type'] = 'temperature'
# #     # else:
# #     #     print(' illegal type')
# #     #     # Exception
# #     # if sign == '0':
# #     #     data['data'] = rr.registers[1]/(10**pos)
# #     # elif sign == '8':
# #     #     data_origin = rr.registers[1]
# #     #     if data_origin >= 32767:
# #     #         data['d ata'] = -(65536 - rr.registers[1]) / (10 ** pos)
# #     #     # data['data'] = -(65536-rr.registers[1])/(10**pos)
# #     #     else:
# #     #         data['data'] = rr.registers[1] / (10 ** pos)
# #     # else:
# #     #     print('illegal sign')
# #     #     # raise ValueError
# #     # data_all.append(data)
# #     print('rr'+str(i)+': %s' % repr(rr_hex))
# #     sleep(1)



