#本代码根据已有的文章名搜索文章的引用信息
from selenium import webdriver
from selenium.webdriver.common.by import By #To locate element
from selenium.webdriver.support.ui import WebDriverWait
'''An expectation to locate an element and check if the selection state specified 
is in that state. locator is a tuple of (by, path) is_selected is a boolean'''
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys #模拟键盘

class Reference:
    def __init__(self):
        baidu_url = 'https://xueshu.baidu.com/'
        google_url = 'https://scholar.google.com/'
        self.baidu_url = baidu_url
        self.google_url = google_url

        options = webdriver.ChromeOptions()
        options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})  # 不加载图片,加快访问速度
        options.add_experimental_option('excludeSwitches',
                                        ['enable-automation'])  # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
        chromedriver_path = "/Users/apple/Downloads/chromedriver"
        self.browser = webdriver.Chrome(executable_path=chromedriver_path, options=options)
        self.wait = WebDriverWait(self.browser, 10)  # 超时时长为10s

    def gain_reference(self,article_name):
        self.browser.get(self.baidu_url)
        search = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, '''//*[@id="kw"]''')))
        search.send_keys(article_name)

        submit = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, '''//*[@id="su"]''')))
        submit.click()

        reference = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '''//*[@id="dtl_l"]/div[1]/div[3]/div/a[2]/span''')))
        reference.click()

        #text = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, '''//*[@id="sc_cit0"]''')))
        text = WebDriverWait(self.browser, 10).until(
            EC.visibilityOfElementLocated((By.XPATH, '''//*[@id="sc_cit0"]''')))
        t = text.text
        print(t)

    def gain_reference_google(self,article_name):
        self.browser.get(self.google_url)
        search = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, '''//*[@id="gs_hdr_tsi"]''')))
        search.send_keys(article_name)

        submit = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, '''// *[ @ id = "gs_hdr_tsb"] / span / span[1]''')))
        submit.click()

        #注意⚠️在浏览器上的检查键不一定是目标，要适当调整
        reference = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, '''/html/body/div/div[10]/div[2]/div[2]/div[2]/div[1]/div/div[3]/a[2]/svg/path''')))
        #//*[@id="gs_res_ccl_mid"]/div[1]/div/div[3]/a[2]/svg
        reference.click()

        text = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '''/html/body/div/div[4]/div/div[2]/div/div[1]/table/tbody/tr[1]/td/div''')))
        t = text.text
        print(t)

if __name__ == "__main__":
    r = Reference()
    r.gain_reference_google('Microbiological safety of drinking water')
    #article_list = ['引滦黎河水环境保护及存在问题探讨','引滦工程水库群联合运行问题初探','微生物水质改善原位处理技术在潘家口水库的应用研究']
'''
    article_list = []
    num_list = []
    count = 0
    f = open('/Users/apple/Desktop/article_list.txt')
    for line in f:
        num, article = line.strip().split()
        article_list.append(article)
        num_list.append(num)
    print(article_list)
    print('-'*30)
    r = Reference()
    for article_name in article_list:
        try:
            print('编号'+num_list[count]+':')
            r.gain_reference(article_name)'''
        #except:
            #print('''The article "'''+article_name+'''" is NOT FOUND!!!!!!''')
            #print(article_name)
        #count += 1

