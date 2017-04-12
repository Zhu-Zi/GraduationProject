# 基础数据统计
# 14级每一位学生的消费总额和消费次数以及学生的基本信息
# 详细数据见数据库 AllStudentsConsumptions 集合
import json
import os.path
import xlrd
import pymongo
import pandas as p

# 指明被遍历文件夹
# rootdir = "C:\\Users\\Keyboard\\Desktop\\毕设\\TestData\\EduceationTestData\\14yearData\\14中国语言文学"
rootdir = "C:\\Users\\Keyboard\\Desktop\\毕设\\TestData\\EduceationTestData\\14yearData"

# 自定义机器类
class Student:
    # 初始化
    def __init__(self):
        self.studentNum = '0'
        self.studentName = 'test'
        self.studentGrade = '14'
        self.studentClass = '1401'
        self.studentConsumptions = 0.00
        self.studentConsumptionTimes = 0

# 文件路径集合
filesList = []

# 学生总消费金额
StudentTotalConsumptions = p.core.series.Series()
# 学生每日消费金额
StudentTotalConsumptionTimes = []
# 学生集合
AllStudents = []

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

    fileSrt = file.split('\\')
    lastNum = len(fileSrt)
    gradeName = fileSrt[lastNum - 2]
    classData = fileSrt[lastNum - 1].split('.')
    className = classData[0]

    wb = xlrd.open_workbook(file)
    table = wb.sheet_by_index(0)

    StudentTotalConsumptions = excelData.groupby(['账号'])['发生金额'].sum()
    StudentTotalConsumptionTimes = excelData.groupby(['账号']).size()

    student = Student()

    for item in StudentTotalConsumptions.index:
        student.studentNum = str(item)
        student.studentGrade = gradeName
        student.studentClass = className
        student.studentConsumptions = float(StudentTotalConsumptions[item])
        student.studentConsumptionTimes = int(StudentTotalConsumptionTimes[item])

        for r in range(table.nrows):
            rowValue = table.cell(r, 1).value
            if rowValue == student.studentNum:
                student.studentName = table.cell(r, 2).value

        # 将对象转化为字典类型
        studentDict = student.__dict__
        # 字典对象转化为 Json
        studentJson = json.dumps(studentDict)
        # Json 对象转化为字典类型（为什么这样做？——直接存serviceDict会出现所有对象数据一样的问题）
        serviceDict = json.loads(studentJson)

        AllStudents.append(serviceDict)

print(AllStudents)
print(len(AllStudents))

# 打开 MongoDB 客户端
client = pymongo.MongoClient('127.0.0.1', 27017)
# 设置数据库名称
db = client['graduationProject']
# 设置集合名称
table = db['AllStudentsConsumptions']

table.insert_many(AllStudents)

print('Success')


