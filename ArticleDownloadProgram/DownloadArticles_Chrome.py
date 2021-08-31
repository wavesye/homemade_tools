from selenium import webdriver
from selenium.webdriver.common.by import By  # To locate element
from selenium.webdriver.support.ui import WebDriverWait

'''An expectation to locate an element and check if the selection state specified 
is in that state. locator is a tuple of (by, path) is_selected is a boolean'''
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys  # 模拟键盘
import pandas as pd
import re

'''
根据文档中的doi，批量自动化下载文献

1. 直接从web of science导出excel表格，其中就有doi的列
2. 将doi放入/Users/apple/Downloads/相关文献doi汇总.txt文件中
3. 用selenium自动打开sci-hub网站，输入doi并搜索和下载
'''


class Article:
    def __init__(self):
        scihub_url = 'https://sci-hub.shop/'
        self.scihub_url = scihub_url

        options = webdriver.ChromeOptions()
        options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})  # 不加载图片,加快访问速度
        options.add_experimental_option('excludeSwitches',
                                        ['enable-automation'])  # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
        chromedriver_path = "/Users/apple/Downloads/chromedriver 3"
        self.browser = webdriver.Chrome(executable_path=chromedriver_path, options=options)
        self.wait = WebDriverWait(self.browser, 20)  # 超时时长为10s

    def gain_article(self, doi):
        self.browser.get(self.scihub_url)
        search = WebDriverWait(self.browser, 20).until(
            EC.presence_of_element_located((By.XPATH, '''//*[@id="input"]/form/input[2]''')))
        search.send_keys(doi)

        submit = WebDriverWait(self.browser, 20).until(
            EC.presence_of_element_located((By.XPATH, '''//*[@id="open"]/p''')))
        submit.click()

        save = WebDriverWait(self.browser, 20).until(
            EC.presence_of_element_located((By.XPATH, '''//*[@id="buttons"]/ul/li[2]/a''')))
        save.click()

    def download_from_df(self, df):

        # 计数器
        '''count = 0
        while(count<=len(df)):
            count = count + 1
            try:
                self.gain_article(df['DOI'])
                print('successfully download: '+str(count)+' '+doi[count])
            except:
                print(str(count) + +' '+doi[count] + 'download failure')
                print('ARTICLE CANNOT BE FOUND!!!')'''

        for index, row in df.iterrows():
            print(row['Number'], end=' ')
            print(row['DOI'])
            try:
                self.gain_article(df['DOI'])
                print('successfully download: ' + row['Number'] + ' ' + row['DOI'])
            except:
                print(row['Number'] + ' ' + row['DOI'] + 'download failure')
                print('ARTICLE CANNOT BE FOUND!!!')
            print()

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
    filepath = '/Users/apple/Downloads/相关文献doi汇总.txt'
    pattern = r'^(([0-9\.]+)\t.+)$'
    r = Readfile(filepath, pattern)
    df = r.loading_data()
    # print(df)
    a = Article()
    a.download_from_df(df)

    '''a = Article()
    file = '/Users/apple/Downloads/相关文献doi汇总.txt'
    doi = []
    with open(file) as f:
        for line in f:
                number, x = line.strip().split()
                doi.append(x)
                #print(number, ': ', x)'''

