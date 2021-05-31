#!/usr/bin/env python
#本程序的目的是实现直接通过输入文件夹路径，读取其中的txt文件，识别数据行，并将数据储存在x_axis和y_axis变量中，用于作图。
#另外还会传出基准值、第一峰值和第十峰值到/Users/apple/Desktop/ads_data/TenTimesDecreaseRatio.txt文件中。
import logging,re,sys,os,heapq
import matplotlib.pyplot as plt
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s - %(levelname)s - %(message)s')
logging.disable(logging.CRITICAL)
plt.rcParams['font.sans-serif']=['SimSun']
plt.rcParams['axes.unicode_minus']=False

#todo 识别实验数据，并将实验数据写入一个嵌套列表
def recognize(line):
    '''
    目的是识别line是否为三个由空格间隔的数据，若真，则将第一和第三个数据写入列表中
    '''
    #mo = re.compile(r'^(\d*.\d+) \d+.\d+ \d+.\d+')
    mo = re.compile(r'^([0-9\.E-]+) ([0-9\.]+) ([0-9\.]+)$')
    if mo.search(line) != None:
        return True
    return False
def recognize_collegeTGA(line):
    '''
    目的是识别line是否为三个由空格间隔的数据，若真，则将第一和第三个数据写入列表中
    '''
    #mo = re.compile(r'((\d)+\.(\d)+)(.)+(\d+\.\d+)(.)+(\d+\.\d+)(.)+(\d+\.\d+)')
    #mo = re.compile(r'^([0-9\.]+)(.+)([0-9\.]+)(.+)([0-9\.]+)(.+)([0-9\.]+)(.+)$')
    mo = re.compile(r'^([0-9\.]+)[ \t]([0-9\.]+)[ \t]([0-9\.]+)[ \t]([0-9\.]+)$')
    if mo.search(line) != None:
        return True
    return False
'''
为了辨别txt文件中的有用数据
'''

#todo 打开对应txt文件
def openfile(filename):

    try:

        fin = open(filename, 'r', encoding='utf16')
        print('Successfully open file - %s'%(filename))
    except:
        print('open file error!')
    logging.debug('start of the data collection')
    x_axis = []
    y_axis = []

    for line in fin:
        # logging.debug(line)
        data = line.strip()
        #print(data)
        if recognize(data):
            #print('recognize',data)
            str_minute, str_temperature, str_mass = line.split(' ')
            minute = float(str_minute)
            mass = float(str_mass)
            if mass >1 and minute>0.1: #大于0.1min才把点算入
                x_axis.append(minute)
                y_axis.append(mass)
            continue
        if recognize_collegeTGA(data):
            #print('lalala')
            # print(line)
            #print(data)
            str_minute, str_temperature, str_mass, str_massPercentage = line.split()[:4]
            # str_minute, str_temperature, * = line.split()
            minute = float(str_minute)
            mass = float(str_mass)
            #if mass > 1 and mass < 20 and minute > 0.1: #Be careful of this
            if mass > 1  and minute > 0.1:
                x_axis.append(minute)
                y_axis.append(mass)



    #print(x_axis)
    #print(y_axis)

    fin.close()
    logging.debug('end of the data collection')
    return x_axis,y_axis
'''
打开文件，读取有用数据，储存在x_axis和y_axis变量中，并返回x_axis和y_axis
'''

#todo 利用matplotlib画图
def graph(x_axis,y_axis,basename_list,count):

    plt.plot(x_axis, y_axis, 'k')
    plt.xlabel('时间(min)')
    plt.ylabel('吸附量(wt%)')
    y_max = max(y_axis)
    t = heapq.nsmallest(100,y_axis)
    y_min = max(t)
    plt.axis([0, 2000, (y_min-1), (y_max+1)]) #30cycles [0,2000]
    #print('######',len(basename_list),basename_list)
    if len(basename_list) == 21:
        plt.suptitle('Mg:Al=1:1, Ca(Ac)$_2$:LDH=10:1'
                     + '\n' + '30 Cycles Cyclic Adsorption Capacity')
    if len(basename_list) == 19:
        plt.suptitle('Pure Calcium Oxide'
                     + '\n' + '30 Cycles Cyclic Adsorption Capacity')
    if len(basename_list) == 8:
        plt.suptitle('Pure Calcium Oxide'
                 +'\n' +'Cyclic Adsorption Capacity')
    if len(basename_list) == 9:
        plt.suptitle('Mg:Al=' + basename_list[0] + ':' + basename_list[1] + \
                 r',Ca(Ac)$_2$:LDH=10:' + basename_list[4] \
                 +'\n' +'Cyclic Adsorption Capacity')
    if len(basename_list) == 10:
        plt.suptitle('Mg:Al=' + basename_list[0] + basename_list[1]+':' + basename_list[2] + \
                 r',Ca(Ac)$_2$:LDH=10:' + basename_list[5] \
                 +'\n' +'Cyclic Adsorption Capacity')
    if len(basename_list) == 11:
        #print('basename_list is: ',basename_list)
        #print('basename_list[7]=',basename_list[6])
        if basename_list[6]=='2':
            plt.suptitle('Mg:Al=' + basename_list[0] +':' + basename_list[1] + \
                 r',Ca(Ac)$_2$:LDH=10:' + basename_list[4] \
                 +'\n' +'Cyclic Adsorption Capacity Second test')
        if basename_list[6]=='3':
            plt.suptitle('Mg:Al=' + basename_list[0] +':' + basename_list[1] + \
                 r',Ca(Ac)$_2$:LDH=10:' + basename_list[4] \
                 +'\n' +'Cyclic Adsorption Capacity Third test')
        if basename_list[6]=='4':
            plt.suptitle('Mg:Al=' + basename_list[0] +':' + basename_list[1] + \
                 r',Ca(Ac)$_2$:LDH=10:' + basename_list[4] \
                 +'\n' +'Cyclic Adsorption Capacity Fourth test')
    if len(basename_list) == 16: #11101-2020-1.txt
        if basename_list[11] == '1':
            plt.suptitle('Mg:Al=' + basename_list[0] + ':' + basename_list[1] + \
                         r',Ca(Ac)$_2$:LDH=10:' + basename_list[4] \
                         + '\n' + 'Cyclic Adsorption Capacity 2020 First test')
        if basename_list[11] == '2':
            plt.suptitle('Mg:Al=' + basename_list[0] + ':' + basename_list[1] + \
                             r',Ca(Ac)$_2$:LDH=10:' + basename_list[4] \
                             + '\n' + 'Cyclic Adsorption Capacity 2020 Second test')
        if basename_list[11] == '4':
            plt.suptitle('Mg:Al=' + basename_list[0] + ':' + basename_list[1] + \
                             r',Ca(Ac)$_2$:LDH=10:' + basename_list[4] \
                             + '\n' + 'Cyclic Adsorption Capacity 2020 Fourth test')
    if len(basename_list) == 23:
        plt.suptitle('Li$_4$SiO$_4$-'+basename_list[8]+'-1-600-100')

    plt.show()

#todo 目的是找目标横坐标对应的索引，从而找到对应的纵坐标值
def decrease_ratio(x_axis,y_axis,file):

    for increment in range (0,10000):
        '''
        print(111111)
        print(increment)
        print(80 in x_axis)
        '''
        if (80 + 0.00001 * increment) in x_axis:
            print(222222)
            value = 80 + 0.00001 * increment
            baseline_index = x_axis.index(value)
            print('baseline_index = %d'%baseline_index)
            print('x_axis[baseline_index] =%f '% x_axis[baseline_index])
            break
    for increment in range(1,10000):
        if (100+0.00001*increment) in x_axis:
            first_left = x_axis.index(100+0.00001*increment)
            print('first_left = %d'% first_left)
            print('x_axis[first_left] = %f'% x_axis[first_left])
            break
    for increment in range(1,10000):
        if (200+0.00001*increment) in x_axis:
            first_right = x_axis.index(200+0.00001*increment)
            logging.debug('first_right %d= '% first_right)
            logging.debug('x_axis[first_right] = %f'% x_axis[first_right])
            break
    for increment in range(1,10000):
        if (650+0.00001*increment) in x_axis:
            tenth_left = x_axis.index(650+0.00001*increment)
            logging.debug('tenth_left %d= '% tenth_left)
            logging.debug('x_axis[tenth_left] = %f'% x_axis[tenth_left])
            break
    for increment in range(1,10000):
        if (699+0.00001*increment) in x_axis:
            tenth_right = x_axis.index(699+0.00001*increment)
            logging.debug('tenth_right = %d'%tenth_right)
            logging.debug('x_axis[tenth_right] = %f'% x_axis[tenth_right])
            break

    baseline = y_axis[baseline_index]
    print('baseline y_axis is: ', baseline)
    first_pinnacle = max(y_axis[first_left:first_right])
    tenth_pinnacle = max(y_axis[tenth_left:tenth_right])
    dr = (tenth_pinnacle - baseline) / (first_pinnacle - baseline)
    print('decrease ratio is: ', dr)
    first_to_base_ratio = first_pinnacle / baseline
    tenth_to_base_ratio = tenth_pinnacle / baseline
    print('first_to_base_ratio: ',first_to_base_ratio)
    print('tenth_to_base_ratio: ', tenth_to_base_ratio)
    return baseline
    '''
    #把数据写入txt文件
    fin = open('/Users/apple/Desktop/ads_data/TenTimesDecreaseRatio.txt','a')
    fin.write(file)
    fin.write(' ')
    fin.write(str(dr))
    fin.write(' ')
    fin.write(str(first_to_base_ratio))
    fin.write('\n')
    fin.close()##
    '''
'''
目的是找目标横坐标对应的索引，从而找到对应的纵坐标值
'''
################################################################################################

#todo 从多个文件中打开数据并画图
if __name__ == "__main__":
    os.chdir('/Users/apple/Desktop/ads_data/ads_raw_data')
    folder = '/Users/apple/Desktop/ads_data/ads_raw_data'

    count = 1
    for file in os.listdir(folder):
        if file == '.DS_Store':
            continue
        basename = os.path.basename(file)
        basename_list = list(basename)

        print('filename = ', file)
        t = openfile(file)
        print('Done!')
        x_axis, y_axis = t

        baseline = decrease_ratio(x_axis, y_axis, file)
        new_y_axis = [(i - baseline) / baseline * 100 for i in y_axis]
        graph(x_axis, new_y_axis, basename_list, count)

        count += 1

