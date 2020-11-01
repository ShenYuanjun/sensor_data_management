'''
空调数据读取并写入数据库
'''

import asyncio
import os
from datetime import datetime
import time

import addressing as ads


async def airCdt_modbus2mongodb(collection, clients):
    t = time.time()



    await asyncio.sleep(1)
    print('time consuming: ', time.time() - t)