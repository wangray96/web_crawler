from selenium import webdriver
import pandas as pd
from bs4 import BeautifulSoup
import time
from selenium.webdriver.chrome.options import Options
import warnings
from traceback import print_exc
warnings.filterwarnings('ignore')
param_dict={'419':[{'all':'222','name':'394','stars':'231','times':'266','content':'237','type':'num'}],
            '149':[{'all':'241','name':'401','stars':'250','times':'285','content':'256','type':'num'}],
            '402':[{'all':'205','name':'377','stars':'215','times':'216','content':'220','type':'pic'}],
            '158':[{'all':'437','name':'410','stars':'259','times':'294','content':'265','type':'num'},
                   {'all':'408','name':'382','stars':'231','times':'266','content':'237','type':'num'},
                   {'all':'420','name':'393','stars':'243','times':'244','content':'248','type':'pic'}],
            '391':[{'all':'398','name':'366','stars':'203','times':'238','content':'209','type':'num'}]
            }

def get_google_map_reviews(url,sec):
    chrome_options = Options()  # 啟動無頭模式
    # chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get(url)
    driver.implicitly_wait(3)
    # for p in range(20):#每次載7篇
    scrollable_div = driver.find_element_by_xpath("//div[@class='section-layout section-scrollbox mapsConsumerUiCommonScrollable__scrollable-y mapsConsumerUiCommonScrollable__scrollable-show']")
    sleep_time = 1
    for s in range(int(sec/sleep_time)):
        driver.execute_script('arguments [0] .scrollTop = arguments [0] .scrollHeight',scrollable_div)
        time.sleep(sleep_time)

    driver.execute_script('arguments [0] .scrollTop = 0',scrollable_div)
    time.sleep(2)
    targets_to_click = driver.find_elements_by_xpath("//button[contains(text(),'全文')]")
    # print(len(targets_to_click))
    for t in targets_to_click:
        try:
            t.click()
        except:
            pass
    id_dict_ttl = param_dict[BeautifulSoup(driver.page_source).find('div',{"aria-label":'所有評論'}).get('jstcache')]
    id_dict_len = len(id_dict_ttl)
    for i in range(id_dict_len):
        id_dict=id_dict_ttl[i]
        soup = BeautifulSoup(driver.page_source).find('div',{"aria-label":'所有評論'}).find_all('div',jstcache=id_dict['all'])
        if len(soup)>0:
            break

    name =[]
    stars =[]
    times=[]
    content=[]
    # print('姓名', soup[s].find('div',jstcache='391').get_text())
    # print('星數', soup[s].find('span',jstcache='231').get_text())
    # print('時間', soup[s].find('span', jstcache='266').get_text())
    # print('內容', soup[s].find('span', jstcache='237').get_text())
    # print("===========================")
    for s in range(len(soup)):
        try:
            tmp = soup[s].find('span',jstcache=id_dict['name']).get_text()
        except:
            print_exc()
            tmp =None
        name.append(tmp)

        try:
            if id_dict['type']=='num':
                tmp = soup[s].find('span',jstcache=id_dict['stars']).get_text()
            elif id_dict['type'] == 'pic':
                tmp = soup[s].find('span', jstcache=id_dict['stars']).get('aria-label')
        except:
            tmp =None
        stars.append(tmp)

        try:
            tmp = soup[s].find('span', jstcache=id_dict['times']).get_text()
        except:
            tmp =None
        times.append(tmp)

        try:
            tmp = soup[s].find('span', jstcache=id_dict['content']).get_text()
        except:
            tmp =None
        content.append(tmp)
    df = pd.DataFrame({'姓名':name, '星數':stars, '時間':times, '內容':content})
    driver.quit()
    return df
# file_name = '台北君悅酒店'
# url='https://www.google.com.tw/maps/place/Grand+Hyatt+Taipei/@25.035776,121.5612161,16z/data=!4m10!3m9!1s0x3442abb7a75a2db7:0x44cef53b99be635a!5m2!4m1!1i2!8m2!3d25.0353353!4d121.5627762!9m1!1b1?hl=zh-TW'
target = pd.read_excel('飯店景點爬蟲範圍.xlsx')
for l in range(len(target)):
    file_name = target.loc[l, '名稱']
    url =str(target.loc[l,'Google Map網址'])
    # wait_sec = int(int(target.loc[l, 'Google Map評論數'])*(60/660))
    wait_sec = 240
    if file_name!='nan' and str(url) != 'nan':
        print(str(url))
        # print(get_google_map_reviews(url, 1))
        print(file_name,f'等待{wait_sec}秒', url)
        df= get_google_map_reviews(url,wait_sec)#60s->660篇
        print('共有%s筆'%len(df['姓名']))
        print('--------------------')
        df.to_excel('./GoogleMap/%s_google_map_reviews.xlsx' % file_name, index=False)

