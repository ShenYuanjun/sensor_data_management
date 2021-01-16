# # h='41360000'
# # b=bin()
# B = '{:0>16b}{:0>16b}'.format(0x4365, 0x4CCD)
# # c='{:0>16b}{:0>16b}'.format(rr.registers[0],rr.registers[1])
# # c = '01000011011001010100110011001101'
# s = int(B[0])
# e = int(B[1:9], 2) - 127
# M = B[9:32]
# Mi = int('1' + M[0:e], 2)
# Mf = M[e:]
# # Mf='011'
# xm = 0.0
# for k in range(len(Mf)):
#     xm += int(Mf[k]) / 2 ** (k + 1)
# # x = (-1) ** s * M * 2 ** e
# x = (-1) ** s * (Mi + xm)

import os
from time import sleep, time
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.transaction import ModbusRtuFramer as ModbusFramer
from datetime import datetime

name = ['room1', 'room2', 'room4']
gateway = [24, 48, 87]
register = [0x2000, 0x4000]
length = [18, 2]

var_n = [
    [
        ['voltage', 0],
        ['electric_current', 2],
        ['instant_total_active_power', 4],
        ['instant_useless_total_power', 6],
        ['instant_apparent_total_power', 8],
        ['power_factor_total', 10],
        ['grid_frequency', 14],
    ],
    [
        ['total_active_energy', 0]
    ]
]

client = ModbusClient('192.168.1.146', port=12345, timeout=3, framer=ModbusFramer)
is_connected = client.connect()
if is_connected:  # modbus connect fail
    for i in range(3):
        data = {}
        for j in range(2):
            sleep(1)
            rr = client.read_holding_registers(register[j], length[j], unit=gateway[i])
            if hasattr(rr, 'registers'):
                # data_modbus = {}
                for v in var_n[j]:

                    # IEEE-754 hex to float
                    B = '{:0>16b}{:0>16b}'.format(rr.registers[v[1]], rr.registers[v[1] + 1])
                    s = int(B[0])
                    e = int(B[1:9], 2) - 127
                    M = B[9:32]
                    if e > 0:
                        Mi = int('1' + M[0:e], 2)
                        Mf = M[e:23]
                    elif e == 0:
                        Mi = 1.0
                        Mf = M
                    else:
                        Mi = 0.0
                        Mf = '1' + M
                        for k in range(-e - 1):
                            Mf = '0' + Mf
                    xm = 0.0
                    for k in range(len(Mf)):
                        xm += int(Mf[k]) / 2 ** (k + 1)
                    x = (-1) ** s * (Mi + xm)

                    data[v[0]] = x

                # data.append(data_modbus)
                print(['{:04X}'.format(rx) for rx in rr.registers])
                print([x for x in data.values()])
            else:  # no data return
                # data.append('No Data Return')
                data['0x{:4x}'.format(register[j])] = 'No Data Return'
        data_db = {'name': name[i],
                   'data': data,
                   'datetime': datetime.now()}
        # result = collection.insert_one(data_db)

else:
    data_db = {'name': '{:0>2d}xxxx'.format(bus),
               'err': 'Modbus Connect Failed',
               'datetime': datetime.now()}
    # result = collection.insert_one(data_db)
client.close()
