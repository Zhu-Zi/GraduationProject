# 这个程序将所有14级消费过的机器信息统计后存入mongodb
# 存入数据结果如下自定义机器类所示，即：机器号，机器消费额度，机器消费次数 ，存入集合为 TopServices
# 统计并存入14级消费过的所有机器，集合名称为 serviceCollection ，存入集合为 AllServicesList
import os
import os.path
import xlrd
import pandas as p
from datetime import *
import time
import pymongo
import json

# 自定义机器类
class Service:
    # 初始化
    def __init__(self):
        self.serviceNum = '0'
        self.serviceConsumption = '0'
        self.serviceTimes = 0

class ServiceEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Service):
            return obj.serviceNum
        return json.JSONEncoder.default(self, obj)

# 打开 MongoDB 客户端
client = pymongo.MongoClient('127.0.0.1', 27017)
# 设置数据库名称
db = client['graduationProject']
# 设置集合名称
table = db['TopServices']

# 指明被遍历文件夹
# rootdir = "C:\\Users\\Keyboard\\Desktop\\毕设\\TestData\\EduceationTestData\\14yearData\\14历史"
rootdir = "C:\\Users\\Keyboard\\Desktop\\毕设\\TestData\\EduceationTestData\\14yearData"

# 文件路径集合
filesList = []
# 机器集合
serviceCollection = [{'serviceConsumption': 438, 'serviceNum': 1, 'serviceTimes': 59}]

# 三个参数： 分别返回1.父目录，2.所有文件夹名字（不含路径）3.所有文件名字
for parent, dirnames, filenames in os.walk(rootdir):
    # 输出文件信息
    for filename in filenames:
        # 文件路径信息
        fullPath = os.path.join(parent, filename)
        # 文件路径集合
        filesList.append(fullPath)

    # 文件路劲集合（测试是否录入全部文件路径）
    for file in filesList:
        print("the full name is :" + file)

for file in filesList:
    excelData = p.read_excel(file, names=['系统流水', '账号', '姓名', '业务类型', '发生金额', '账户余额', '结算时间',
                                          '发生时间', '营业号', '业务员'])

    serviceConsumption = excelData.groupby(['营业号'])['发生金额'].sum()
    serviceTimes = excelData.groupby(['营业号']).size()

    # 机器集合，中间变量
    servicelist = []

    # 创建 Service 对象
    service = Service()

    # 显示 series 的索引值（即'营业号'）
    for item in serviceTimes.index:
        service.serviceNum = int(item)
        service.serviceTimes = int(serviceTimes[item])
        service.serviceConsumption = int(serviceConsumption[item])

        # 将对象转化为字典类型
        serviceDict = service.__dict__
        # 字典对象转化为 Json
        serviceJson = json.dumps(serviceDict)
        # Json 对象转化为字典类型（为什么这样做？——直接存serviceDict会出现所有对象数据一样的问题）
        serviceDict = json.loads(serviceJson)

        servicelist.append(serviceDict)

    print(servicelist)
    table.insert_many(servicelist)

    oldNum = len(serviceCollection)
    newNum = len(servicelist)

    if oldNum < newNum:
        serviceCollection = servicelist

# 设置集合名称
table = db['AllServicesList']
table.insert_many(serviceCollection)

print('Success')





