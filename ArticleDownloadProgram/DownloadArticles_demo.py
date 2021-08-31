from selenium import webdriver
from selenium.webdriver.common.by import By #To locate element
from selenium.webdriver.support.ui import WebDriverWait
'''An expectation to locate an element and check if the selection state specified 
is in that state. locator is a tuple of (by, path) is_selected is a boolean'''
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys #模拟键盘

'''
快速下载endnote中的文献

1. 下载paste，从endnote中复制多个文献的doi
2. 将doi放入/Users/apple/Downloads/Second Desktop/2020暑-水中氨基酸类有机物的分类和检测方法/doi.txt文件中
3. 用selenium自动打开sci-hub网站，输入doi并搜索和下载
'''

class Article:
    def __init__(self):
        scihub_url = 'https://sci-hub.pl/'
        self.scihub_url = scihub_url

        options = webdriver.ChromeOptions()
        options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})  # 不加载图片,加快访问速度
        options.add_experimental_option('excludeSwitches',
                                        ['enable-automation'])  # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
        chromedriver_path = "/Users/apple/Downloads/chromedriver"
        self.browser = webdriver.Chrome(executable_path=chromedriver_path, options=options)
        self.wait = WebDriverWait(self.browser, 20)  # 超时时长为10s

    def gain_article(self,doi):
        self.browser.get(self.scihub_url)
        search = WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.XPATH, '''//*[@id="input"]/form/input[2]''')))
        search.send_keys(doi)

        submit = WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.XPATH, '''//*[@id="open"]/p''')))
        submit.click()

        save = WebDriverWait(self.browser, 20).until(
            EC.presence_of_element_located((By.XPATH, '''//*[@id="buttons"]/ul/li[2]/a''')))
        save.click()




if __name__ == "__main__":
    a = Article()
    file = '/Users/apple/Downloads/Second Desktop/2020暑-水中氨基酸类有机物的分类和检测方法/doi.txt'
    doi = []
    with open(file) as f:
        for line in f:
            number, x = line.strip().split()
            doi.append(x)
            #print(number, ': ', x)

    count = 14
    for x in doi:
        count = count + 1
        try:
            a.gain_article(x)
            print('successfully download: '+str(count))
        except:
            print(str(count) + 'error')
            print(x + 'CANNOT FIND!!!')


