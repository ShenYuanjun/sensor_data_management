# import motor.motor_tornado
# from tornado.ioloop import IOLoop
#
# client = motor.motor_tornado.MotorClient('mongodb://192.168.1.10/',
#                                          username='zgl',
#                                          password='123456',
#                                          authSource='admin',
#                                          authMechanism='SCRAM-SHA-256')
# db = client['cpes']
# collection = db['data_test']
#
# async def do_insert():
#     document = {'key': 'value'}
#     result = await collection.insert_one(document)
#     print('result %s' % repr(result.inserted_id))
#
# if __name__ == '__main__':
#
#     # client = motor.motor_tornado.MotorClient('mongodb://192.168.1.10/',
#     #                                          username='zgl',
#     #                                          password='123456',
#     #                                          authSource='admin',
#     #                                          authMechanism='SCRAM-SHA-256')
#     # db = client['cpes']
#     # collection = db['data_test']
#
#     IOLoop.current().run_sync(do_insert)

#
# from datetime import datetime
# import os
#
# from tornado.ioloop import IOLoop
# from apscheduler.schedulers.tornado import TornadoScheduler
# import motor.motor_tornado
#
#
# def tick():
#     print('Tick! The time is: %s' % datetime.now())
#
# async def do_insert(collection):
#     document = {'key': 'value', "time": datetime.now()}
#     result = await collection.insert_one(document)
#     print('result %s' % repr(result.inserted_id))
#
#
# if __name__ == '__main__':
#
#     client = motor.motor_tornado.MotorClient('mongodb://192.168.1.10/',
#                                              username='zgl',
#                                              password='123456',
#                                              authSource='admin',
#                                              authMechanism='SCRAM-SHA-256')
#     db = client['cpes']
#     collection = db['data_test']
#
#     scheduler = TornadoScheduler()
#     # scheduler.add_job(tick, 'interval', seconds=3)
#     scheduler.add_job(do_insert, 'interval', args=[collection], seconds=3)
#     scheduler.start()
#     print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
#
#     # Execution will block here until Ctrl+C (Ctrl+Break on Windows) is pressed.
#     try:
#         IOLoop.instance().start()
#     except (KeyboardInterrupt, SystemExit):
#         pass


from pymodbus.client.sync import ModbusTcpClient as ModbusClient

# from pymodbus.client.sync import ModbusUdpClient as ModbusClient
# from pymodbus.client.sync import ModbusSerialClient as ModbusClient

UNIT = 0x1

client = ModbusClient('192.168.1.82', port=1032)
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

adress_register = 0  # 起始寄存器
length_data = 64  # 数据长度 HEX=40
adress_gateway = 0x1  # 云盒地址
rr = client.read_holding_registers(adress_register, length_data, unit=adress_gateway)
# rr = client.read_input_registers(adress_register, length_data, unit=adress_gateway)
# rr = client.read_discrete_inputs(adress_register, length_data, unit=adress_gateway)

# rr = client.read_holding_registers(1, 8, unit=UNIT)
# assert(not rq.isError())     # test that we are not an error
# assert(rq.registers == [20]*8)      # test the expected value
# assert(rr.registers == [20]*8)      # test the expected value

client.close()
