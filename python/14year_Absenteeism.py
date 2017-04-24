# 统计出学生的缺课信息作为缺课原始数据
import pymongo
import numpy
from datetime import *
import time
import json

# 旷课类
class Absenteeism:
    def __init__(self):
        self.collageName = 'collage'
        self.className = 'className'
        self.studentName = 'studentName'
        self.datetime = 0.00
        self.week = 'Monday'
        self.classNum = 0
        self.studentConsumptions = 0.00

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

# 判断是否为同一天
def is_same_day(w_day, week):
    if w_day == 0 or w_day == 6:
        return False
    if w_day == 1 and week == '星期一':
        return True
    else:
        False
    if w_day == 2 and week == '星期二':
        return True
    else:
        False
    if w_day == 3 and week == '星期三':
        return True
    else:
        False
    if w_day == 4 and week == '星期四':
        return True
    else:
        False
    if w_day == 5 and week == '星期五':
        return True
    else:
        False

# 判断是否旷课
def is_absenteeism(m_hour, m_min, class_num):
    if class_num == '1':
        if m_hour == 8:
            if m_min >= 0 and m_min <= 50:
                return True
            else:
                return False
        else:
            False
    if class_num == '2':
        if m_hour == 9:
            if m_min >= 0 and m_min <= 50:
                return True
            else:
                return False
        else:
            return False
    if class_num == '3':
        if m_hour == 10 and m_min >= 10:
            return True
        else:
            return False
    if class_num == '4':
        if m_hour == 11 and m_min >= 10:
            return True
        else:
            return False
    if class_num == '5':
        if m_hour == 14 and m_min >= 30:
            return True
        else:
            if m_hour == 15 and m_min <= 30:
                return True
            else:
                return True
    if class_num == '6':
        if m_hour == 15 and m_min >= 40:
            return True
        else:
            if m_hour == 16 and m_min <= 30:
                return True
            else:
                return True
    if class_num == '7':
        if m_hour == 16 and m_min >= 50:
            return True
        else:
            if m_hour == 17 and m_min <= 40:
                return True
            else:
                return True
    if class_num == '8':
        if m_hour == 17 and m_min >= 50:
            return True
        else:
            if m_hour == 18 and m_min <= 40:
                return True
            else:
                return True

# 打开 MongoDB 客户端
client = pymongo.MongoClient('127.0.0.1', 27017)
# 设置数据库名称
db = client['graduationProject']
# 设置集合名称
curriculumTable = db['AllCurriculum']
rawDataTable = db['AllRawData']

rawData = rawDataTable.find()

allAbsenteeismData = []
symbol = 1

for item in rawData:
    className = item['studentClass']
    curriculumData = curriculumTable.find({'className': className})
    itemDateFloat = item['settlementDateTime']
    timeTuple = float_tuple(itemDateFloat)
    for curriculum in curriculumData:
        flag = is_same_day(timeTuple.tm_wday, curriculum['week'])
        if flag:
            isAbsenteeism = is_absenteeism(timeTuple.tm_hour, timeTuple.tm_min, curriculum['classNum'])
            if isAbsenteeism:
                absenteeism = Absenteeism()
                absenteeism.collageName = curriculum['collageName']
                absenteeism.className = curriculum['className']
                absenteeism.studentName = item['studentName']
                absenteeism.datetime = item['settlementDateTime']
                absenteeism.week = curriculum['week']
                absenteeism.classNum = curriculum['classNum']
                absenteeism.studentConsumptions = item['studentConsumptions']

                symbol += 1
                print(symbol)
                allAbsenteeismData.append(dict_helper(absenteeism))

# 设置集合名称
absenteeismTable = db['Absenteeism']
absenteeismTable.insert_many(allAbsenteeismData)
print('success')
