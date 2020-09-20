"""
Demonstrates how to use the background scheduler to schedule a job that executes on 3 second
intervals.
"""

import asyncio
import os
from datetime import datetime
# import pprint

# from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
# from pymongo import MongoClient
import motor.motor_asyncio


def tick():
    print('Tick! The time is: %s' % datetime.now())

async def createOneAsyn(collection):
    document = {'key': 'value', "time": datetime.now()}
    result = await collection.insert_one(document)
    print('inserted: %s' % repr(result.inserted_id))

async def readArbAsyn(collection):
    # find_one()
    result = await collection.find_one()
    print('found: %s' % repr(result))

async def countAsyn(collection):
    all = await collection.count_documents({})
    print("There is/are " + str(all) + " document(s)")


if __name__ == '__main__':

    client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://192.168.1.10/',
                                             username='zgl',
                                             password='123456',
                                             authSource='admin',
                                             authMechanism='SCRAM-SHA-256')

    db = client['cpes']
    collection = db['data_test']

    scheduler = AsyncIOScheduler()
    scheduler.add_job(tick, 'interval', seconds=3)
    scheduler.add_job(createOneAsyn, 'interval', args=[collection], seconds=3)
    scheduler.add_job(countAsyn, 'interval', args=[collection], seconds=3)
    scheduler.start()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    # Execution will block here until Ctrl+C (Ctrl+Break on Windows) is pressed.
    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass
