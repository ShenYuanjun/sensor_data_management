'''
tcp同步
'''
import logging
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from pymodbus.transaction import ModbusRtuFramer as ModbusFramer
from pymodbus.constants import Defaults as Set
from time import sleep, time

# from pymodbus.client.sync import ModbusUdpClient as ModbusClient
# from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from datetime import datetime

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

UNIT = 0x1
# Set.TransactionId = 0x1500
# Set.ProtocolId = 0


# client = ModbusClient('192.168.1.83', port=1040, timeout=3)#, framer=ModbusFramer
# client.connect()
#
#
# log.debug("Read write registers simulataneously")
# adress_register = 0x00  # 起始寄存器
# length_data = 0x08  # 数据长度
# adress_gateway = 0x01  # 云盒地址
# rr = client.read_holding_registers(adress_register, length_data, unit=adress_gateway)
# print(['{:04X}'.format(rx) for rx in rr.registers])
#
#
# client.close()
# flag = False


# for i in range(3):
#     client = ModbusClient('192.168.1.83', port=1037 + i, timeout=1)  # , framer=ModbusFramer
#     cf = client.connect()
#     # print(client.socket)
#     if not cf:
#         print('connect failed ', i)
#         client.close()
#         continue
#     print('connect successed ', i)
#     client.close()


def do():
    try:
        t = time()
        DBclient = MongoClient('mongodb://192.168.1.10/',
                               username='zgl',
                               password='123456',
                               authSource='admin',
                               serverSelectionTimeoutMS=3000,
                               socketTimeoutMS=4000)



        # DBclient.admin.command('ismaster')

        db = DBclient['cpes']
        collection = db['foo']
        data_db = {'err': 'No Data Return',
                   'datetime': datetime.now()}
        result = collection.insert_one(data_db)
        print('writed')

    except ConnectionFailure as e:  #
        log.info(e)
        print("Server not available")
        return
    except Exception as e:
        log.info(e)
    finally:
        print(time() - t)




do()