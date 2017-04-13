# 获取单个学生信息的所有信息
# 统计出各机器消费金额及次数
# 统计出消费总额

import os
import os.path
import xlrd
import pandas as p
import json
from datetime import *
import time

# 自定义机器类
class Student:
    # 初始化
    def __init__(self):
        self.studentNum = '0'
        self.studentName = 'test'
        self.studentConsumptions = 0.00
        self.studentBalance = 0.00
        self.settlementTime = 0.00
        self.machineNum = '0'

# 指明被遍历文件夹
rootdir = "C:\\Users\\Keyboard\\Desktop\\毕设\\TestData\\EduceationTestData\\14yearData\\14中国语言文学"
# 文件路径集合
filesList = []
# 学生姓名
stuName = '董星'
# 学生数据集合
stuDataList = []

# 三个参数： 分别返回1.父目录，2.所有文件夹名字（不含路径）3.所有文件名字
for parent, dirnames, filenames in os.walk(rootdir):
    # 输出文件信息
    for filename in filenames:
        # 文件路径信息
        fullPath = os.path.join(parent, filename)
        # 文件路径集合
        filesList.append(fullPath)

    # 文件路劲集合（测试是否录入全部文件路径）
    # for file in filesList:
    #     print("the full name is :" + file)

for file in filesList:
    excelData = p.read_excel(file, names=['系统流水', '账号', '姓名', '业务类型', '发生金额', '账户余额', '结算时间',
                                          '发生时间', '营业号', '业务员'])

    wb = xlrd.open_workbook(file)
    table = wb.sheet_by_index(0)

    for r in range(table.nrows):
        rowValue = table.cell(r, 2).value
        if type(rowValue) == (type('str')):
            if rowValue == stuName:
                student = Student()
                student.studentNum = table.cell(r, 1).value
                student.studentName = table.cell(r, 2).value
                student.studentConsumptions = table.cell(r, 4).value
                student.studentBalance = table.cell(r, 5).value
                student.settlementTime = table.cell(r, 6).value
                student.machineNum = table.cell(r, 8).value

                # 将对象转化为字典类型
                studentDict = student.__dict__
                # 字典对象转化为 Json
                studentJson = json.dumps(studentDict)
                # Json 对象转化为字典类型（为什么这样做？——直接存serviceDict会出现所有对象数据一样的问题）
                studentDict = json.loads(studentJson)
                stuDataList.append(studentDict)

# for item in stuDataList:
#     print(item['studentNum'])
#     print(item['studentName'])
#     print(item['studentConsumptions'])
#     print(item['machineNum'])

data = p.DataFrame(stuDataList)
# 各机器消费次数统计
time = data.groupby(['machineNum']).size()
print(time)
# 各机器消费金额统计
consumptions = data.groupby(['machineNum'])['studentConsumptions'].sum()
print(consumptions)
# 消费总额
totalConsumption = data['studentConsumptions'].sum()
print('消费总额为: %.2f' % totalConsumption)

