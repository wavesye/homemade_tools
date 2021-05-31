#!/usr/bin/env python3
# coding: utf-8

# In[3]:


import pandas as pd
import numpy as np
import re, os, sys
import logging


# In[2]:


'''
本程序的设计目标是利用三维荧光数据计算分区intensity

方法一：
1. 将文本数据导入pandas dataframe（可能用到正则表达式）
2. 分列（正则表达式）
3. EX列排序，从小到大
4. 将数据分成两个区（两个dataframe？）（判断EX，200-250，250-400）
5. 分别对两个dataframe分区（EM，第一段是250-330，330-380，380-550；第二段是250-380，380-550）

方法二：
1. 将文本数据导入excel（可能用到正则表达式）
2. 分列
3. EX列排序，从小到大
4. 将数据分成两个区（两个dataframe？）（判断EX，200-250，250-400）
5. 分别对两个dataframe分区（EM，第一段是250-330，330-380，380-550；第二段是250-380，380-550）

注意事项：
txt文件中不要含有中文！！！否则utf-8解析会报错！
'''


# In[80]:



#todo 利用正则表达式识别数据
def recognize(line):
    mo = re.compile(r'^([0-9\.]+)\t([0-9\./]+)\t([0-9\.]+)$') #形式为1 1.23/1.34 1.45
    if mo.search(line) != None:
        return True
    return False

#todo 打开txt文件识别文件中的数据并存入list，返回数据list
def openfile(filename):
    try:
        fin = open(filename, 'r', encoding='utf8')
        #logging.debug('successfully open file - %s' % (filename))
    except:
        print('open file error!')
    Number = []
    EX = []
    EM = []
    Height = []
    for line in fin:
        data = line.strip()
        if recognize(data):
            str_number, str_ex_em, str_height = line.split()
            
            str_ex, str_em = str_ex_em.split('/') #将ex和em用split方法分开
                      
            number = int(str_number)
            ex = float(str_ex)
            em = float(str_em)
            height = float(str_height)
            
            Number.append(number)
            EX.append(ex)
            EM.append(em)
            Height.append(height)
    fin.close()
    #logging.debug('end of data collection from - %s'%(filename))
    return Number, EX, EM, Height

#todo 将从文件读取到的数据（list）放入pandas dataframe中
def data_input(Number, EX, EM, Height):

    data = {
        'Number':Number,
        'EX':EX,
        'EM':EM,
        'Height':Height
    }
    df = pd.DataFrame(data)
    #print(df)
    
    df_part_one = df[df.EX<=250]  #EX为200-250范围内的数据
    #print('df_part_one:')
    #print(df_part_one)
    
    df_part_two = df[df.EX>250]  #EX为250-400范围内的数据
    #print('df_part_two')
    #print(df_part_two)
    
    df_part_one_t = df_part_one.sort_values(by = 'EM') #将第一部分按EM排序
    #print('df_part_one_t')
    #print(df_part_one_t)
    
    df_part_two_t = df_part_two.sort_values(by = 'EM') #将第二部分按EM排序
    #print('df_part_two_t')
    #print(df_part_two_t)
    
    df1 = df_part_one_t[(df_part_one_t.EM<=330) & (df_part_one_t.EM>250)] #芳香蛋白一
    #print('df1')
    #print(df1)
    
    df2 = df_part_one_t[(df_part_one_t.EM<=380) & (df_part_one_t.EM>330)] #芳香蛋白二
    #print('df2')
    #print(df2)
    
    df3 = df_part_one_t[(df_part_one_t.EM<=550) & (df_part_one_t.EM>380)] #富里酸类
    #print('df3')
    #print(df3)
    
    df4 = df_part_two_t[(df_part_two_t.EM<=380) & (df_part_two_t.EM>250)] #溶解性微生物代谢产物类
    #print('df4')
    #print(df4)
    
    df5 = df_part_two_t[(df_part_two_t.EM<=550) & (df_part_two_t.EM>380)] #溶解性微生物代谢产物类
    #print('df5')
    #print(df5)
    
    ######各分区强度计算
    #Region I
    max1 = df1['Height'].max()
    sum1 = df1['Height'].sum()
    i1 = sum1*5*5
    in_value1 = i1*20.4
    '''
    print('max1 = ',max1)
    print('sum1 = ',sum1)
    print('i1 = ',i1)
    print('in_value1 = ',in_value1) 
    '''
    
    #Region II
    max2 = df2['Height'].max()
    sum2 = df2['Height'].sum()
    i2 = sum2*5*5
    in_value2 = i2*16.4
    
    
    #Region III
    max3 = df3['Height'].max()
    sum3 = df3['Height'].sum()
    i3 = sum3*5*5
    in_value3 = i3*4.81
    
    
    #Region IV
    max4 = df4['Height'].max()
    sum4 = df4['Height'].sum()
    i4 = sum4*5*5
    in_value4 = i4*8.76
    
    
    #Region V
    max5 = df5['Height'].max()
    sum5 = df5['Height'].sum()
    i5 = sum5*5*5
    in_value5 = i5*1.76
    
    
    print('Region              I          II       III          IV          V')
    print('Imax          %10.1f %10.1f %10.1f %10.1f %10.1f'%(max1,max2,max3,max4,max5))
    print('sum_intensity %10.1f %10.1f %10.1f %10.1f %10.1f'%(sum1,sum2,sum3,sum4,sum5))
    print('in            %10.1f %10.1f %10.1f %10.1f %10.1f'%(in_value1,in_value2,in_value3,in_value4,in_value5))
    
def read_folder(folder): 
    for file in sorted(os.listdir(folder)): #对文件进行排序sorted
        #print(file)
        #print(folder)
        filename = folder + '/' + file
        print('*********',filename, '*********')
        if file == '.DS_Store':
            continue
        Number, EX, EM, Height = openfile(filename)
        data_input(Number, EX, EM, Height)
        print('\n\n')
        
    
read_folder('/Users/apple/Downloads/20210121')

#Number, EX, EM, Height = openfile('/Users/apple/Downloads/20210121/1-1_20210121_103155(FD3).TXT')
#data_input(Number, EX, EM, Height)


# In[ ]:




