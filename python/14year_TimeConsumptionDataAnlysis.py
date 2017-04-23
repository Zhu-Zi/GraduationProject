# 消费时段数据统计分析
import os
import os.path
import xlrd
import pandas as p
import json
from datetime import *
import time
import pymongo

# Float 时间转化为 时间元组（timetuple）
def float_tuple(raw_data):
    raw_data_datetime = datetime.fromtimestamp(raw_data)
    raw_data_tuple = time.strptime(str(raw_data_datetime), '%Y-%m-%d %H:%M:%S')
    return raw_data_tuple

# 打开 MongoDB 客户端
client = pymongo.MongoClient('127.0.0.1', 27017)
# 设置数据库名称
db = client['graduationProject']
# 设置集合名称
table = db['AllTimeConsumptions']
tableData = table.find()

allWorkDayTimeConsumptions = []
allWeekendTimeConsumptions = []

for item in tableData:
    datalist = []
    datalist.append(item['timeConsumption'])
    datalist.append(item['studentNum'])
    datalist.append(item['studentName'])
    datalist.append(item['studentConsumptions'])
    datalist.append(item['studentBalance'])
    datalist.append(item['consumptionTime'])
    datalist.append(item['machineNum'])

    timeTuple = float_tuple(item['consumptionTime'])
    # 统计工作日消费信息
    if timeTuple.tm_wday != 0 and timeTuple.tm_wday != 6:
        allWorkDayTimeConsumptions.append(datalist)
    else:
        allWeekendTimeConsumptions.append(datalist)

workdayConsumptionData = p.DataFrame(allWorkDayTimeConsumptions)
weekendConsumptionData = p.DataFrame(allWeekendTimeConsumptions)

workDayTimeConsumption = workdayConsumptionData.groupby([0]).size()
print('工作日一天内各时间段消费情况')
print(workDayTimeConsumption)

weekendTimeConsumptions = weekendConsumptionData.groupby([0]).size()
print('周末一天内各时间段消费情况')
print(weekendTimeConsumptions)