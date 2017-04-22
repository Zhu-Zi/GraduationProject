# 统计出各个时间段的消费信息并存入数据库
# 数据集合为 AllTimeConsumptions
# 消费时段: beforeAM8 为 “时段A” ，AM8_to_AM9 为 “时段B” 以此类推直至 lastPM7 为 “时段M”
import pymongo
from datetime import *
import time
import json

# 消费时间段类
class TimeConsumption:
    # 初始化
    def __init__(self):
        self.timeConsumption = 'X'
        self.studentNum = '0'
        self.studentName = 'test'
        self.studentConsumptions = 0.00
        self.studentBalance = 0.00
        self.consumptionTime = 0.00
        self.settlementDate = 0.00
        self.settlementDateTime = 0.00
        self.machineNum = 0

# Float 时间转化为 时间元组（timetuple）
def float_tuple(raw_data):
    raw_data_datetime = datetime.fromtimestamp(raw_data)
    raw_data_tuple = time.strptime(str(raw_data_datetime), '%Y-%m-%d %H:%M:%S')
    return raw_data_tuple

# 字典类型存入数据库前的类型转换（后期优化可以优化）
def dict_helper(info):
    # 将对象转化为字典类型
    data_dict = info.__dict__
    # 字典对象转化为 Json
    data_json = json.dumps(data_dict)
    # Json 对象转化为字典类型（为什么这样做？——直接存serviceDict会出现所有对象数据一样的问题）
    data_dict = json.loads(data_json)
    return data_dict

# 打开 MongoDB 客户端
client = pymongo.MongoClient('127.0.0.1', 27017)
# 设置数据库名称
db = client['graduationProject']
# 设置集合名称
table = db['AllRawData']
data = table.find()

allTimeConsumptions = []
for item in data:
    itemDateFloat = item['settlementDateTime']
    itemDateTuple = float_tuple(itemDateFloat)
    timeConsumption = TimeConsumption()
    flag = itemDateTuple

    if flag.tm_hour < 8:
        timeConsumption.timeConsumption = 'time_A'
    if flag.tm_hour >= 8:
        if flag.tm_hour < 9:
            timeConsumption.timeConsumption = 'time_B'
    if flag.tm_hour >= 9:
        if flag.tm_hour < 10:
            timeConsumption.timeConsumption = 'time_C'
    if flag.tm_hour >= 10:
        if flag.tm_hour < 11:
            timeConsumption.timeConsumption = 'time_D'
    if flag.tm_hour >= 11:
        if flag.tm_hour < 12:
            timeConsumption.timeConsumption = 'time_E'
    if flag.tm_hour >= 12:
        if flag.tm_hour < 13:
            timeConsumption.timeConsumption = 'time_F'
    if flag.tm_hour >= 13:
        if flag.tm_hour < 14:
            timeConsumption.timeConsumption = 'time_G'
    if flag.tm_hour >= 14:
        if flag.tm_hour < 15:
            timeConsumption.timeConsumption = 'time_H'
    if flag.tm_hour >= 15:
        if flag.tm_hour < 16:
            timeConsumption.timeConsumption = 'time_I'
    if flag.tm_hour >= 16:
        if flag.tm_hour < 17:
            timeConsumption.timeConsumption = 'time_J'
    if flag.tm_hour >= 17:
        if flag.tm_hour < 18:
            timeConsumption.timeConsumption = 'time_K'
    if flag.tm_hour >= 18:
        if flag.tm_hour < 19:
            timeConsumption.timeConsumption = 'time_L'
    if flag.tm_hour >= 19:
            timeConsumption.timeConsumption = 'time_M'

    timeConsumption.studentNum = item['settlementDate']
    timeConsumption.studentName = item['studentName']
    timeConsumption.studentConsumptions = item['studentConsumptions']
    timeConsumption.studentBalance = item['studentBalance']
    timeConsumption.consumptionTime = item['settlementDateTime']
    timeConsumption.settlementDate = item['settlementDate']
    timeConsumption.settlementDateTime = item['settlementDateTime']
    timeConsumption.machineNum = item['machineNum']

    allTimeConsumptions.append(dict_helper(timeConsumption))

# 设置集合名称
table = db['AllTimeConsumptions']
table.insert_many(allTimeConsumptions)

print('success')