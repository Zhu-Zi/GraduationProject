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

# 统计函数
def collection_list(table_data):
    all_workday_time_consumptions = []
    all_weekend_time_consumptions = []

    for item in table_data:
        datalist = []
        datalist.append(item['timeConsumption'])
        datalist.append(item['studentNum'])
        datalist.append(item['studentName'])
        datalist.append(item['studentConsumptions'])
        datalist.append(item['studentBalance'])
        datalist.append(item['consumptionTime'])
        datalist.append(item['machineNum'])

        time_tuple = float_tuple(item['consumptionTime'])
        # 统计工作日消费信息
        if time_tuple.tm_wday != 0 and time_tuple.tm_wday != 6:
            all_workday_time_consumptions.append(datalist)
        else:
            all_weekend_time_consumptions.append(datalist)

    return all_workday_time_consumptions, all_weekend_time_consumptions

# 打开 MongoDB 客户端
client = pymongo.MongoClient('127.0.0.1', 27017)
# 设置数据库名称
db = client['graduationProject']
# 设置集合名称
table = db['AllTimeConsumptions']
tableData = table.find()

allData = collection_list(tableData)
allWorkDayTimeConsumptions = allData[0]
allWeekendTimeConsumptions = allData[1]

workdayConsumptionData = p.DataFrame(allWorkDayTimeConsumptions)
weekendConsumptionData = p.DataFrame(allWeekendTimeConsumptions)

workDayTimeConsumption = workdayConsumptionData.groupby([0]).size()
print('工作日一天内各时间段消费情况')
print(workDayTimeConsumption)

weekendTimeConsumptions = weekendConsumptionData.groupby([0]).size()
print('周末一天内各时间段消费情况')
print(weekendTimeConsumptions)
# # *************** part1,part2 *************************************************************************************

# timeAData = table.find({'timeConsumption': 'time_A'})
# allData = collection_list(timeAData)
# allWorkDayTimeConsumptions = allData[0]
# allWeekendTimeConsumptions = allData[1]
#
# workdayConsumptionData = p.DataFrame(allWorkDayTimeConsumptions)
# weekendConsumptionData = p.DataFrame(allWeekendTimeConsumptions)
#
# workdayConsumption = workdayConsumptionData.groupby([3]).size()
# print('工作日早餐消费额度情况')
# print(workdayConsumption)
# weekendConsumption = weekendConsumptionData.groupby([3]).size()
# print('周末早餐消费额度情况')
# print(weekendConsumption)
# # ******************** 早餐情况统计 *******************************************************************************

# timeFData = table.find({'timeConsumption': 'time_F'})
# allData = collection_list(timeFData)
# allWorkDayTimeConsumptions = allData[0]
# allWeekendTimeConsumptions = allData[1]
#
# workdayConsumptionData = p.DataFrame(allWorkDayTimeConsumptions)
# weekendConsumptionData = p.DataFrame(allWeekendTimeConsumptions)
#
# workdayConsumption = workdayConsumptionData.groupby([3]).size()
# print('工作日中午12:00-13:00消费额度情况')
# print(workdayConsumption)
# weekendConsumption = weekendConsumptionData.groupby([3]).size()
# print('周末中午12:00-13:00消费额度情况')
# print(weekendConsumption)
#
# timeGData = table.find({'timeConsumption': 'time_G'})
# allData = collection_list(timeGData)
# allWorkDayTimeConsumptions = allData[0]
# allWeekendTimeConsumptions = allData[1]
#
# workdayConsumptionData = p.DataFrame(allWorkDayTimeConsumptions)
# weekendConsumptionData = p.DataFrame(allWeekendTimeConsumptions)
#
# workdayConsumption = workdayConsumptionData.groupby([3]).size()
# print('工作日中午13:00-14:00消费额度情况')
# print(workdayConsumption)
# weekendConsumption = weekendConsumptionData.groupby([3]).size()
# print('周末中午13:00-14:00消费额度情况')
# print(weekendConsumption)
# # ******************** 午餐情况统计 *******************************************************************************

# timeJData = table.find({'timeConsumption': 'time_J'})
# allData = collection_list(timeJData)
# allWorkDayTimeConsumptions = allData[0]
# allWeekendTimeConsumptions = allData[1]
#
# workdayConsumptionData = p.DataFrame(allWorkDayTimeConsumptions)
# weekendConsumptionData = p.DataFrame(allWeekendTimeConsumptions)
#
# workdayConsumption = workdayConsumptionData.groupby([3]).size()
# print('工作日中午16:00-17:00消费额度情况')
# print(workdayConsumption)
# weekendConsumption = weekendConsumptionData.groupby([3]).size()
# print('周末中午16:00-17:00消费额度情况')
# print(weekendConsumption)
#
# timeKData = table.find({'timeConsumption': 'time_K'})
# allData = collection_list(timeKData)
# allWorkDayTimeConsumptions = allData[0]
# allWeekendTimeConsumptions = allData[1]
#
# workdayConsumptionData = p.DataFrame(allWorkDayTimeConsumptions)
# weekendConsumptionData = p.DataFrame(allWeekendTimeConsumptions)
#
# workdayConsumption = workdayConsumptionData.groupby([3]).size()
# print('工作日中午17:00-18:00消费额度情况')
# print(workdayConsumption)
# weekendConsumption = weekendConsumptionData.groupby([3]).size()
# print('周末中午17:00-18:00消费额度情况')
# print(weekendConsumption)
#
# timeLData = table.find({'timeConsumption': 'time_L'})
# allData = collection_list(timeLData)
# allWorkDayTimeConsumptions = allData[0]
# allWeekendTimeConsumptions = allData[1]
#
# workdayConsumptionData = p.DataFrame(allWorkDayTimeConsumptions)
# weekendConsumptionData = p.DataFrame(allWeekendTimeConsumptions)
#
# workdayConsumption = workdayConsumptionData.groupby([3]).size()
# print('工作日中午18:00-19:00消费额度情况')
# print(workdayConsumption)
# weekendConsumption = weekendConsumptionData.groupby([3]).size()
# print('周末中午18:00-19:00消费额度情况')
# print(weekendConsumption)
# # ******************** 晚餐情况统计 *******************************************************************************