from scipy.interpolate import make_interp_spline
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import leastsq
#import openpyxl
#from openpyxl.utils.dataframe import dataframe_to_rows
#from scipy.interpolate import interp1d
'''
该程序只适用于只有一种反应物的情况！！！在主函数中更改实验数据(时间t，反应浓度c)，程序自动计算出反应级数n以及反应速率常数k。
'''
#为了画出平滑曲线，在实验点之间插入额外的点
def insert_dots(t,c):
    tnew = np.linspace(min(t), max(t), 300)
    cnew = make_interp_spline(t, c)(tnew)
    return tnew,cnew

#计算斜率（反应速率）
def slope(tnew,cnew):
    return -np.diff(cnew)/np.diff(tnew)

#计算lnx
def lnx():
    return lambda x:np.log(x)

# 利用scipy的leastsq进行最小二乘法线性回归
def err(p, x, y):
        return p[0] * x + p[1] - y

def least_square(x_data, y_data):
    p0 = np.array([4.1, 4.6])
    ret = leastsq(err, p0, args=(x_data, y_data))
    print(ret)
    k, b = ret[0] #注意⚠️这里给出的b值只是截距，也就是说没有考虑实际正负的因素！！！这里容易出bug！！

    print('反应级数n =', ret[0][0])
    print('反应速率常数k = ', np.exp(-ret[0][1]))
    plt.scatter(x_data, y_data, color="red", label="Sample Point", linewidth=3)
    x = np.linspace(x_data.min(), x_data.max(), 1000)
    y = k * x + b
    plt.plot(x, y, color="orange", label="Fitting Line", linewidth=2)
    plt.legend()
    plt.show()



def main(t,c):
    tnew, cnew = insert_dots(t, c)
    reaction_rate = slope(tnew, cnew)

    # 建立DataFrame记录数据
    df1 = pd.DataFrame(
        {
            'tnew': tnew[:299],
            'cnew': cnew[:299],
            'reaction_rate': reaction_rate
        },
        columns=['tnew', 'cnew', 'reaction_rate']
    )
    df1['lnc'] = df1.cnew.apply(lnx())
    df1['lnr'] = df1.reaction_rate.apply(lnx())
    print(df1)

    #先转置，再取某一行或某一列，得到DataFrame某一列的numpy array数据，如print(df1.values.T[0])
    lnr = df1.values.T[3]
    lnc = df1.values.T[4]

    #利用公式lnr = lnk + nlnc计算反应级数n，以及对应的反应速率常数k
    least_square(x_data=lnc,y_data=lnr)

    '''
    #测试：打开excel，将数据输入excel，在excel中作图看是否与scipy计算得到的斜率一致
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    for r in dataframe_to_rows(df1, index=True, header=True):
        worksheet.append(r)
    workbook.save("/Users/apple/Downloads/pandas_openpyxl.xlsx")
    '''
    #作图
    #fig, ax = plt.subplots()
    #df1.plot(x='lnc', y='lnr',ax=ax,color='g',marker='*',kind='scatter') #当使用markevery时不仅不需要plot.scatter，而且不能用

if __name__=='__main__':
    t = [0, 4, 8, 12, 16, 20, 24]
    c = [478, 395, 329, 272, 226, 187, 155]
    main(t,c)


