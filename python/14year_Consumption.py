import os
import os.path
import xlrd
import pandas as p

# 指明被遍历文件夹
# rootdir = "C:\\Users\\Keyboard\\Desktop\\毕设\\TestData\\EduceationTestData\\15yearData"
rootdir = "C:\\Users\\Keyboard\\Desktop\\毕设\\TestData\\EduceationTestData\\14yearData\\14环境"

# 文件路径集合
filesList = []

# 消费金额
consumption = 0.0
student = "s"

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
    wb = xlrd.open_workbook(file)
    table = wb.sheet_by_index(0)

    for r in range(table.nrows):
        # consumption = table.cell(r, 4).value + consumption
        rowValue = table.cell(r, 4).value
        if type(rowValue) == float:
            consumption = rowValue + consumption

print("Total consumptions are %f" % consumption)

