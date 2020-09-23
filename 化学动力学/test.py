from scipy.interpolate import make_interp_spline
from scipy.interpolate import interp1d
import numpy as np
import matplotlib.pyplot as plt
'''
采用微分法测定反应级数：计算不同时间点处反应的速率、反应物的浓度，带入反应速率公式ln(-dc/dt) = lnk + nlnc，两式相减消去lnk后即可计算出反应级数n。
ps:该程序只考虑了一种反应物的情形。也就是说，多于一种反应物的情形是不能采用该程序进行计算的。程序会给出计算的n值和反应的浓度变化图像。
'''

#画图、拟合并计算浓度和斜率
def plotting(t,c,DATA):
    '''
    该函数输入反应时间和对应的浓度水平，输出各个时间点的反应速率和对应的浓度水平。
    :param t: float, time，时间
    :param c: float, concentration，反应物a的浓度
    :param DATA: 两个时间点[t1,t2]，程序分别计算两个时间点的浓度和反应速率
    :return:  反应速率（导数值）和对应浓度
    '''
    # 差值后的时间和浓度，以及导数值
    tnew = np.linspace(t.min(), t.max(), 300)  # np.linspace()用于插入等差数列，其中参数300代表插值的数量。若修改，记得后面也要改！！
    cnew = make_interp_spline(t, c)(tnew)
    slope_c = np.diff(cnew) / np.diff(tnew)

    # 生成画布
    fig, ax1 = plt.subplots()

    # 设置ax1
    color = 'tab:red'
    ax1.set_xlabel('t')
    ax1.set_ylabel('c', color=color)
    ax1.scatter(t, c, color='tab:red')
    ax1.plot(tnew, cnew, color=color)
    time1, concentration = plt.gca().lines[0].get_xydata()[DATA]
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.set_title('Homework 1-1')
    ax1.grid(True)

    # 建立双坐标轴
    ax2 = ax1.twinx()

    # f = interp1d(t,c,kind='cubic')
    # ax.plot(tnew,f(tnew),'r')
    color = 'tab:blue'
    ax2.set_ylabel('derivative', color=color)  # we already handled the x-label with ax1
    ax2.plot(tnew[:299], slope_c, color=color) #为了使xy数量相同
    time2, derivative = plt.gca().lines[-1].get_xydata()[DATA]
    ax2.tick_params(axis='y', labelcolor=color)
    print('(时间，浓度，斜率) = ','({0}，{1}，{2})'.format(time2,concentration,derivative))

    fig.tight_layout()
    plt.show()

    return (concentration,derivative,time2)

#计算反应级数
def reaction_order():
    count = 0
    for i in calculating_points:
        count = count + 1
        if count == 1:
            c1, r1, time1 = plotting(t, c, i)
        if count == 2:
            c2, r2, time2 = plotting(t, c, i)
    n = np.log10(r2/r1) / np.log10(c2/c1)

    print('反应级数n='+str(n))
    return n,time2,r2,c2

#对于一级反应
def k(time,concentration,r,initial_concentration):
    #k = -r/np.power(concentration,n)
    #print('反应速率k=',k)
    k2 = 1/time * np.log(initial_concentration/concentration) #478是c0
    print('一级反应的反应速率k2=',k2)

if __name__=='__main__':
    '''
    用户请修改以下的三个参数！！！！！！
    '''
    # 选择计算斜率的时间
    calculating_points = [10, 100]  # 意味着在10和200两个位置计算斜率（分别对应两个时间t的位置）
    # 时间
    t = np.array([0, 184, 319, 526, 867, 1198, 1877, 2315, 3144])
    # 对应时间的浓度
    c = np.array([2.33, 2.08, 1.91, 1.67, 1.36, 1.11, 0.72, 0.55, 0.34])

    n,time,r,concentration = reaction_order()
    print('当时间t={0}时，反应速率为{1}，反应物浓度为{2}'.format(time,r,concentration))

    print('c[0]:',c[0])
    k(time=time,concentration=concentration,r=r,initial_concentration=c[0])
    plt.show()
'''
    #计算k值
    concentration, r = plotting(t, c, calculating_points[0])
    k = -r/np.power(concentration,n)
    print('反应速率k=', k)
'''
