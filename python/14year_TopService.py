# 从数据库的 AllServicesList 和 TopServices 集合获取数据并处理
# 得到一下集合
# timesSort 按照使用次数排序的机器
# consumptionSort 按照消费金额排序的机器
# topTimesServices = [] 使用次数前十的机器
# topConsumptionServices = [] 消费金额前十的机器

import pymongo
import json

# 自定义机器类
class Service:
    # 初始化
    def __init__(self):
        self.serviceNum = '0'
        self.serviceConsumption = '0'
        self.serviceTimes = 0

# 打开 MongoDB 客户端
client = pymongo.MongoClient('127.0.0.1', 27017)

# 设置数据库名称
db = client['graduationProject']

# 设置集合名称
table = db['AllServicesList']

# 所有机器集合
allServices = table.find()
# 所有机器号集合
allServiceNums = []
# 所有数据处理后机器集合
allServiceList = []

for item in allServices:
    # 获取所有消费机器的机器号
    allServiceNums.append(item['serviceNum'])

# 设置集合名称
table = db['TopServices']

for item in allServiceNums:
    serviceList = table.find({'serviceNum': item})
    times = 0
    consumption = 0.0
    # 创建 Service 对象
    service = Service()
    for info in serviceList:
        times = info['serviceTimes'] + times
        consumption = info['serviceConsumption'] + consumption

    service.serviceNum = item
    service.serviceTimes = times
    service.serviceConsumption = consumption

    # 将对象转化为字典类型
    serviceDict = service.__dict__
    # 字典对象转化为 Json
    serviceJson = json.dumps(serviceDict)
    # Json 对象转化为字典类型（为什么这样做？——直接存serviceDict会出现所有对象数据一样的问题）
    serviceDict = json.loads(serviceJson)

    allServiceList.append(serviceDict)

print(allServiceList)
timesSort = sorted(allServiceList, key=lambda x: x['serviceTimes'], reverse=True)
consumptionSort = sorted(allServiceList, key=lambda x: x['serviceConsumption'], reverse=True)

topTimesServices = []
topConsumptionServices = []

count = 0
while count < 10:
    topTimesServices.append(timesSort[count])
    topConsumptionServices.append(consumptionSort[count])
    count = count + 1

print(topTimesServices)
print(len(topTimesServices))
# 设置集合名称
table = db['TopTimesServices']
table.insert_many(timesSort)

print(topConsumptionServices)
print(len(topConsumptionServices))
# 设置集合名称
table = db['TopConsumptionServices']
table.insert_many(consumptionSort)

