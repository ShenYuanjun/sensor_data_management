from pymongo import MongoClient

import datetime
import pprint

### 连接数据库 ###
# cloud = 'mongodb://120.26.160.58/'  # 阿里云的数据库
cloud = 'mongodb://192.168.1.10/'
local = 'mongodb://localhost:27017/'  # 本地数据库
# client = MongoClient(cloud)
client = MongoClient(cloud,
                     username='zgl',
                     password='123456',
                     authSource='admin',
                     authMechanism='SCRAM-SHA-256')

db = client['cpes']  # 创建数据库
# 使用时应注明自己的collection名字，如test_XXX
collection = db['crowd']  # 创建集合（collection），相当于SQL中的table
# 'test_collection'

# post = {"a": 0, "b": 0, "c": 0, "time": datetime.datetime.now()}

### Create ###
def create1():
    # insert_one()
    results = []
    for i in range(10):
        post = {"a": i, "b": i * 10, "c": i * 100, "time": datetime.datetime.now()}
        results.append(collection.insert_one(post).inserted_id)  # 插入一个document并获取其_id
    return results


def create2():
    # inster_many()
    posts = [{"a": i, "b": i + 10, "c": i + 20, "time": datetime.datetime.now()} for i in range(10)]
    results = collection.insert_many(posts).inserted_ids  # 插入多个document并获取其_id
    return results


### Read ###
def readArb():
    # find_one()
    find_result = collection.find_one()  # 任意查找一个document
    print('任意查询')
    pprint.pprint(find_result)


def readCondOne(cond):  # {"a":1}
    # find_one()
    find_result = collection.find_one(cond)  # 返回找到的第一个符合条件的document
    print('第一个' + list(cond.keys())[0] + '=' + str(list(cond.values())[0]))
    pprint.pprint(find_result)


def readCondAll(cond):
    # find()
    print('所有' + list(cond.keys())[0] + '=' + str(list(cond.values())[0]))
    for result in collection.find(cond):  # find()返回一个迭代器，含有所有满足条件的document
        pprint.pprint(result)


def readId(id):
    # find_one({"_id": id})
    print('查找id为(' + str(id) + ')的document')
    find_result = collection.find_one({"_id": id})
    pprint.pprint(find_result)
    return find_result


### Delete ###
def deleteCondOne(cond):
    # delete_one()
    all = collection.count_documents(cond)
    result = collection.delete_one(cond)  # 删除一个满足条件的document
    rest = collection.count_documents(cond)
    print('原来有' + str(all) + '个document，用delete_one删去' + str(result.deleted_count) + '个后，还剩' + str(rest) + '个')


def deleteCondAll(cond):
    # delete_many()
    all = collection.count_documents(cond)
    result = collection.delete_many(cond)  # 删除所有满足条件的document
    rest = collection.count_documents(cond)
    print('原来有' + str(all) + '个document，用delete_many删去' + str(result.deleted_count) + '个后，还剩' + str(rest) + '个')

### demo ###
# IDs = []
# IDs += create1()
# IDs += create2()
#
# readArb()
# readCondOne({"a": 1})
# readcodAll({"a": 1})
# readId(IDs[0])
#
# deleteCondOne({"a": 0})
# deleteCondAll({"a": 1})

# collection.delete_many({})

# posts = [{"area": i, "value": 0, "created_at": datetime.datetime.now()} for i in range(1,8)]
# collection.insert_many(posts).inserted_ids  # 插入多个document并获取其_id



