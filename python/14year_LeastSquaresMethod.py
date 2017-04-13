# 最小二乘法
# 对学生消费金额和消费次数散点图的拟合

import numpy as np
import pymongo
from scipy.optimize import leastsq  # 引入最小二乘法算法

# 打开 MongoDB 客户端
client = pymongo.MongoClient('127.0.0.1', 27017)

# 设置数据库名称
db = client['graduationProject']
# 设置集合名称
table = db['AllStudentsConsumptions']
data = table.find()
xAxis = []
yAxis = []

for item in data:
    xAxis.append(item['studentConsumptionTimes'])
    yAxis.append(item['studentConsumptions'])

Xi = np.array(xAxis)
Yi = np.array(yAxis)

# 需要拟合的函数func :指定函数的形状
def func(p, x):
    k, b = p
    return k * x + b
# 偏差函数：x,y都是列表:这里的x,y更上面的Xi,Yi中是一一对应的
def error(p, x, y):
    return func(p, x) - y

# k,b的初始值，可以任意设定,经过几次试验，发现p0的值会影响cost的值：Para[1]
p0 = [1, 20]

# 把error函数中除了p0以外的参数打包到args中(使用要求)
Para = leastsq(error, p0, args=(Xi, Yi))

# 读取结果
k, b = Para[0]
print("k=", k, "b=", b)
print("cost：" + str(Para[1]))
print("求解的拟合直线为:")
print("y=" + str(round(k, 2)) + "x+" + str(round(b, 2)))