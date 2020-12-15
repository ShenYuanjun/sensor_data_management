# import asyncio
import json
import os
# from datetime import datetime
from math import ceil
from time import sleep, time
from apscheduler.schedulers.background import BackgroundScheduler
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.transaction import ModbusRtuFramer as ModbusFramer
from datetime import datetime, timedelta
# import json
import xlwt
import logging

filename = 'totaldata.json'
logging.basicConfig(filename='air_log1211.log', level=logging.INFO)  # WARNING DEBUG
log = logging.getLogger()

A = 24*4  # 循环次数
v = 15  # 循环间隔分钟数 需大于等于1

bus1 = [0, 1, 2, 3, 4]  # 总线12345
ads1 = [
    [
        ['tank_heat_level', 1, 0x81],
        ['tank_heat_temperature2', 2, 0x01],
        ['tank_heat_temperature1', 3, 0x01],
        ['tank_heat_temperature3', 4, 0x01],
        ['tank_heat_temperature5', 5, 0x01],
        ['tank_heat_temperature4', 9, 0x01],
        ['tank_heat_temperature6', 10, 0x01],
    ],
    [
        ['room1_inlet_pip_temperature', 0, 0x01],
        ['room1_return_pip_temperature', 1, 0x01]
    ],
    [
        ['room3_inlet_pip_temperature', 0, 0x01],
        ['room3_return_pip_temperature', 1, 0x01],
        ['room4_inlet_pip_temperature', 2, 0x01],
        ['room4_return_pip_temperature', 3, 0x01],

    ],
    [
        ['roomVIP_inlet_pip_temperature', 5, 0x01],
        ['roomVIP_return_pip_temperature', 6, 0x01],
        ['roomControl_inlet_pip_temperature', 7, 0x01],
        ['roomControl_return_pip_temperature', 8, 0x01],
        ['terminal_supply_return_pip_temperature', 9, 0x01],
        ['terminal_supply_inlet_pip_temperature', 10, 0x01],
        ['pump_inlet_pip_temperature', 11, 0x01],
        ['domestic_hot_water_inlet_pip_temperature', 12, 0x01],
        ['pump_return_pip_temperature', 13, 0x01]
    ],
    [
        ['conference_front_inlet_pip_temperature', 0, 0X01],
        ['conference_front_return_pip_temperature', 1, 0X01],
        ['conference_back_inlet_pip_temperature', 2, 0X01],
        ['conference_back_return_pip_temperature', 3, 0X01]
    ]

]
# bus2 = []         #总线5678
# ads2 = [
#     [
#         []
#     ]
# ]

i2v = [
    [4, 20],  # 电流范围(mA)
    [-20, 60],  # 温度(℃)
    [0, 100],  # 相对湿度(RH)
    [0, 20],  # 风速(m/s)
]

# 电表
ads3 = [
    ['current_combine_total_active_energy', 0x0000, 2],
    ['instant_total_active_power', 0x0309, 1]
]

# 主机
ads4 = [
    ['total_output_water_temperature', 101],
    ['outdoor_ambient_temperature', 3012]
]

# 表头
name = ['datetime',
        'tank_heat_level',
        'tank_heat_temperature2',
        'tank_heat_temperature1',
        'tank_heat_temperature3',
        'tank_heat_temperature5',
        'tank_heat_temperature4',
        'tank_heat_temperature6',
        'room1_inlet_pip_temperature',
        'room1_return_pip_temperature',
        'room3_inlet_pip_temperature',
        'room3_return_pip_temperature',
        'room4_inlet_pip_temperature',
        'room4_return_pip_temperature',
        'roomVIP_inlet_pip_temperature',
        'roomVIP_return_pip_temperature',
        'roomControl_inlet_pip_temperature',
        'roomControl_return_pip_temperature',
        'terminal_supply_return_pip_temperature',
        'terminal_supply_inlet_pip_temperature',
        'pump_inlet_pip_temperature',
        'domestic_hot_water_inlet_pip_temperature',
        'pump_return_pip_temperature',
        'conference_front_inlet_pip_temperature',
        'conference_front_return_pip_temperature',
        'conference_back_inlet_pip_temperature',
        'conference_back_return_pip_temperature',
        'current_combine_total_active_energy',
        'instant_total_active_power',
        'total_output_water_temperature',
        'outdoor_ambient_temperature']

try:
    t = time()
    totaldata = {}
    with open(filename, 'w') as f:
        json.dump(totaldata, f)
    totaldata['datetime'] = str(datetime.now())
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('1211')
    for j in range(len(name)):
        worksheet.write(0, j, name[j])

    dt = timedelta(minutes=v)


    t0 = datetime.now()
    cb = 1 if t0.minute // v >= 60 else 0
    mn = ((t0.minute // v + 1) * v) % 60
    next = datetime(t0.year, t0.month, t0.day, t0.hour + cb, mn, 0)


    print('program will begin at:' + str(next))
    for kk in range(A):
        while 1:
            if datetime.now() >= next:
                next += dt
                break
            sleep(1)

        a = datetime.now()
        print(str(kk+1) + ':' + str(a))

        totaldata = {}

        # ads1
        for i in range(len(bus1)):  # 读1234总线
            client = ModbusClient('192.168.1.82', port=1030 + bus1[i], timeout=3, framer=ModbusFramer)
            is_connected = client.connect()

            if not is_connected:  # modbus连接失败
                log.info('Modbus Connect Failed')
                client.close()
                sleep(1)
                continue
            for j in range(len(ads1[i])):
                sleep(1)
                rr = client.read_holding_registers(ads1[i][j][1] * 0x40, 0x08, unit=0x01)
                if not hasattr(rr, 'registers'):  # 无返回数据
                    log.info('No Data Return')
                    continue
                data_modbus = rr.registers
                type = data_modbus[0] // 256  # 数据类型
                if type != ads1[i][j][2]:
                    log.info('Wrong Type Index: Should be 0x{:0X}, but accepted 0x{:0X}'.format(ads1[i][j][2],
                                                                                                type))
                    continue
                pos = data_modbus[0] % 16  # 小数位数
                sign_n = data_modbus[0] % 256 - pos  ## 有无符号
                if sign_n == 0x80:
                    sign = True  # 有符号
                elif sign_n == 0x00:
                    sign = False  # 无符号
                else:
                    log.info('Wrong Sign Index: Should be 0x{:0X} or 0x{:0X}, but accepted 0x{:0X}'.format(
                        0x80, 0x00, sign_n))
                    continue
                data_origin = data_modbus[1]
                if sign and data_origin >= 32767:
                    data = -(65536 - data_origin) / (10 ** pos)
                else:
                    data = data_origin / (10 ** pos)
                # datainformation={ads1[i][j][0]:data , 'datetime':str(datetime.now())}
                # totaldata.append(datainformation)
                totaldata[ads1[i][j][0]] = data
            client.close()

        # ads2 在bus2和ads2写入内容后去掉注释即可
        # for i in range(len(bus2)):
        #     client = ModbusClient('192.168.1.82', port=1030 + bus2[i], timeout=3, framer=ModbusFramer)
        #     is_connected = client.connect()
        #
        #     if not is_connected:  # modbus连接失败
        #         log.info('Modbus Connect Failed')
        #         client.close()
        #         sleep(1)
        #         continue
        #     sleep(1)
        #     rr = client.read_holding_registers(0x00, 0x10, unit=0x01)
        #     if not hasattr(rr, 'registers'):  # 无返回数据
        #         log.info('No Data Return')
        #         continue
        #     data_modbus = rr.registers
        #     for j in range(len(ads2[i])):
        #         type = data_modbus[2 * ads2[i][j][1]] // 4096  # 数据类型 C0
        #         if type != 12:
        #             log.info('No Data Return')
        #             continue
        #         pos = data_modbus[0] % 256  # 小数位数
        #         data_origin = data_modbus[2 * ads2[i][j][1] + 1] / (10 ** pos)
        #         inf0 = i2v[0][0]
        #         sup0 = i2v[0][1]
        #         inf1 = i2v[ads2[i][j][2]][0]
        #         sup1 = i2v[ads2[i][j][2]][1]
        #
        #         if inf0 <= data_origin <= sup0:
        #             data = (data_origin - inf0) / (sup0 - inf0) * (sup1 - inf1) + inf1
        #         else:
        #             log.info('Wrong Value Range: Should be 4~20, but accepted {:0X}'.format(data_origin))
        #             continue
        #         # datainformation = {ads2[i][j][0]: data, 'datetime': str(datetime.now())}
        #         # totaldata.append(datainformation)
        #         totaldata[ads2[i][j][0]] = data
        #     client.close()

        # ads3
        client = ModbusClient('192.168.1.83', port=1035, timeout=3, framer=ModbusFramer)
        is_connected = client.connect()

        if is_connected:  # modbus连接成功
            for i in range(len(ads3)):
                sleep(1)
                rr = client.read_holding_registers(ads3[i][1], ads3[i][2], unit=0x01)
                if not hasattr(rr, 'registers'):  # 无返回数据
                    log.info('No Data Return')
                    continue
                data_modbus = rr.registers
                totaldata[ads3[i][0]] = data_modbus[ads3[i][2] - 1]

        else:
            log.info('Modbus Connect Failed')
        client.close()

        # ads4
        client = ModbusClient('192.168.1.83', port=1036, timeout=3, framer=ModbusFramer)
        is_connected = client.connect()

        if is_connected:  # modbus连接成功
            for i in range(len(ads4)):
                sleep(1)
                rr = client.read_holding_registers(ads4[i][1], 0x01, unit=0x01)
                if not hasattr(rr, 'registers'):  # 无返回数据
                    log.info('No Data Return')
                    continue
                data_modbus = rr.registers
                totaldata[ads4[i][0]] = data_modbus[0]
        else:
            log.info('Modbus Connect Failed')
        client.close()

        keys = list(totaldata.keys())
        for j in range(len(name)):
            for i in range(len(keys)):
                if name[j] == keys[i]:
                    worksheet.write(kk + 1, j, totaldata[keys[i]])
                    break
                else:
                    continue
        worksheet.write(kk + 1, 0, str(a))

    workbook.save('totaldata1210.xls')
except Exception as e:
    log.error(e)
finally:
    log.info('Time Consuming: ' + str(time() - t))
