import re,sys,os,heapq,logging
import matplotlib.pyplot as plt
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.disable(logging.CRITICAL)

#todo 利用正则表达式识别数据
def recognize(line):
    mo = re.compile(r'^([0-9\.E-]+) ([0-9\.]+) ([0-9\.]+)$') #形式为1.55 1.23 1.45
    if mo.search(line) != None:
        return True
    return False

#todo 打开txt文件识别文件中的数据并存入list，返回数据list
def openfile(filename):
    try:
        fin = open(filename, 'r', encoding='utf16')
        logging.debug('successfully open file - %s' % (filename))
    except:
        print('open file error!')
    x_axis = []
    y_axis = []
    for line in fin:
        data = line.strip()
        if recognize(data):
            str_minute, str_temperature, str_mass = line.split(' ')
            minute = float(str_minute)
            mass = float(str_mass)
            x_axis.append(minute)
            y_axis.append(mass)
    fin.close()
    logging.debug('end of data collection from - %s'%(filename))
    return x_axis, y_axis

#todo 用matplotlib画图
def graph(x_axis, y_axis, filename):
    plt.plot(x_axis, y_axis, 'k')
    plt.xlabel('xlabel') #x轴标签
    plt.ylabel('ylabel')  # y轴标签
    #以下的y_max,y_min,x_max,x_min是用来圈定图坐标范围的参数
    y_max = max(y_axis) #数据点的最大y值
    y_min = min(y_axis) #数据点的最小y值
    x_max = max(x_axis)#数据点的最大x值
    x_min = min(x_axis)#数据点的最小x值
    plt.axis([x_min,x_max,0.8*y_min,1.2*y_max])
    plt.suptitle(filename)
    plt.show()

#todo 遍历文件夹，自动读取其中的txt文件
def read_folder(folder):
    os.chdir(folder)

    for file in os.listdir(folder):
        print(file)
        print('-'*20)

    for file in os.listdir(folder):
        if file == '.DS_Store':
            continue
        print('filename = ', file)
        x_axis, y_axis= openfile(file)
        graph(x_axis,y_axis,file)

if __name__ == "__main__":

    read_folder('/Users/apple/Desktop/test')

    """os.chdir('/Users/apple/Desktop/test')
    folder = '/Users/apple/Desktop/test'

    for file in os.listdir(folder):
        if file == '.DS_Store':
            continue
        basename = os.path.basename(file)
        print(basename)
        print('filename = ', file)
        x_axis, y_axis= openfile(file)
        print('Done!')
        graph(x_axis, y_axis, basename)"""



