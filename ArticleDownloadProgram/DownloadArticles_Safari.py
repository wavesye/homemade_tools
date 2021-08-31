from selenium import webdriver
from selenium.webdriver.common.by import By  # To locate element
from selenium.webdriver.support.ui import WebDriverWait

'''An expectation to locate an element and check if the selection state specified 
is in that state. locator is a tuple of (by, path) is_selected is a boolean'''
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys  # 模拟键盘
import pandas as pd
import re, time

'''
根据文档中的doi，批量自动化下载文献

1. 直接从web of science导出excel表格，其中就有doi的列
2. 将doi放入/Users/apple/Downloads/相关文献doi汇总.txt文件中
3. 用selenium自动打开sci-hub网站，输入doi并搜索和下载

存在问题：
1. 成功下载的点击save后，网页还没反应过来就被跳转会搜索页面了
2. 有的时候因为网速问题，页面一直没有打开，导致本来能打开的文件也download failure了
解决办法：
1. 提高网速（根本）
2. 在点击save之后，再等待几秒钟
3. 对于没有弹出"无法查找"的doi，延长等待时间
具体：
加入条件控制语句
    if save页面出现:
        save.click()
        等待几秒钟
        
    else if 无法查找页面出现:
        跳过下一个doi
        
    else if save页面未出现且无法查找页面未出现：
        等待几秒钟
'''


class Article:
    def __init__(self):
        scihub_url = 'https://sci-hub.shop/'
        self.scihub_url = scihub_url

        # safaridriver_path = "/Users/apple/Downloads/chromedriver 3"
        self.browser = webdriver.Safari()
        self.wait = WebDriverWait(self.browser, 10)  # 超时时长为10s

    def gain_article(self, doi):
        self.browser.get(self.scihub_url)
        search = WebDriverWait(self.browser, 20).until(
            EC.presence_of_element_located((By.XPATH, '''//*[@id="input"]/form/input[2]''')))
        search.send_keys(doi)

        # 点击完search按钮后等待2秒钟，保证网页能加载
        time.sleep(2)

        submit = WebDriverWait(self.browser, 20).until(
            EC.presence_of_element_located((By.XPATH, '''//*[@id="open"]/p''')))
        submit.click()

        # 点击完submit按钮后等待2秒钟，保证网页能加载
        time.sleep(2)

        # 如果submit之后找不到save的按钮，直接raise ValueError并跳出该循环
        if len(self.browser.find_elements_by_xpath('''//*[@id="buttons"]/ul/li[2]/a''')) == 0\
            and len(self.browser.find_elements_by_xpath('''//*[@id="buttons"]/button''')) == 0:
            raise ValueError('Save button is not found')

        # 判断save出现的位置，要是出现在if语句的位置，则点击if语句的save；反之则点击else语句的save（save有两个xpath）
        if len(self.browser.find_elements_by_xpath('''//*[@id="buttons"]/ul/li[2]/a''')) != 0:
            save = WebDriverWait(self.browser, 5).until(
                EC.presence_of_element_located((By.XPATH, '''//*[@id="buttons"]/ul/li[2]/a''')))
            save.click()
        else:
            save = WebDriverWait(self.browser, 5).until(
                EC.presence_of_element_located((By.XPATH, '''//*[@id="buttons"]/button''')))
            save.click()
        # 若出现save按钮，点击完后等待3秒钟，以免网页还没有反应过来就跳转
        time.sleep(3)

    def download_from_df(self, df):
        for index, row in df.iterrows():
            #print(row['Number'], end=' ')
            #print(row['DOI'])
            try:
                self.gain_article(row['DOI'])
                print('Successfully download: ' + row['Number'] + ' ' + row['DOI'])
            except:
                print(row['Number'] + ' ' + row['DOI'] + ' ' + 'Download failure')
            print()  # 添加空行


# Readfile文件的作用是：将包含DOI数据的txt文件转换为Pandas.DataFrame，以便于使用selenium和Chromedriver逐一下载
class Readfile:
    # 输入文件路径filepath以及正则表达式的pattern
    def __init__(self, filepath, pattern):
        self.filepath = filepath
        self.pattern = pattern
        self.mo = re.compile(pattern)

    # 输入文件中每一行line
    def recognition(self, line):
        if self.mo.search(line) != None:
            return True
        else:
            return False

    def loading_data(self):
        # 打开文件
        try:
            fin = open(self.filepath, 'r', encoding='utf8')
        # logging.debug('successfully open file - %s' % (filename))
        except:
            print('open file error!')

        # 生成两个list记录文件中的内容（两列）
        numList = []
        doiList = []
        for line in fin:
            line = line.strip()
            if self.recognition(line):
                number, doi = line.split()
                numList.append(number)
                doiList.append(doi)
        fin.close()

        data = {
            'Number': numList,
            'DOI': doiList,
        }

        df = pd.DataFrame(data)
        return df


if __name__ == "__main__":
    filepath = '/Users/apple/Downloads/Second Desktop/2020暑-水中氨基酸类有机物的分类和检测方法/doi.txt'  # 相关文献doi汇总.txt
    pattern = r'^(([0-9\.]+) .+)$'
    # pattern = r'^(([0-9\.]+)\t.+)$'
    r = Readfile(filepath, pattern)
    df = r.loading_data()
    # print(df)
    a = Article()
    a.download_from_df(df)
