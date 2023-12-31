from selenium import webdriver
import time
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import warnings
import pandas as pd
warnings.filterwarnings('ignore')
#hotel.com會有兩種template

# url='https://tw.hotels.com/ho120725/?pa=1&q-check-out=2021-05-14&tab=reviews&q-room-0-adults=2&YGF=3&q-check-in=2021-05-13&MGT=1&WOE=5&WOD=4&ZSX=0&SYE=3&q-room-0-children=0'
def get_hotelcom_map_reviews(url):
    chrome_options = Options()  # 啟動無頭模式
    # chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get(url)
    driver.implicitly_wait(3)
    # driver.find_element_by_xpath("//a[@class='total-reviews']").click()
    # driver.find_element_by_xpath("//section[@class='_3Ddcd6']/a").click()
    # driver.implicitly_wait(3)
    time.sleep(5)
    name = []
    stars = []
    times = []
    content = []
    country=[]
    title =[]
    tourtype=[]

    next_button = BeautifulSoup(driver.page_source).find('a',class_='cta cta-secondary cta-next')
    while next_button:
        # scrollable_span = driver.find_element_by_xpath("//span[@class='reviewer']")
        # driver.execute_script('arguments [0] .scrollTop = arguments [0] .scrollHeight', scrollable_span)
        soup = BeautifulSoup(driver.page_source).find('div',class_='brand-reviews-listing').find_all('div',class_='review-card')
        # if soup[0].find('div',class_='meta').img.get('src').split('/')[-1].split('.')[0]!='tw':
        #     break
        for s in soup:
            #name
            try:
                tmp = s.find('span',class_='reviewer').get_text()
            except:
                tmp = None
            name.append(tmp)
            # print('name',tmp)
            #stars
            try:
                tmp = s.find('span',class_='rating-score').get_text()
            except:
                tmp = None
            stars.append(tmp)
            # print('stars',tmp)
            #times
            try:
                tmp = s.find('span',class_='date').get_text()
            except:
                tmp = None
            times.append(tmp)
            # print('times',tmp)
            #content
            try:
                tmp = s.find('blockquote',class_='expandable-content description').get_text()
            except:
                tmp = None
            content.append(tmp)
            # print('content',tmp)
            #country
            try:
                tmp = s.find('div',class_='meta').img.get('src').split('/')[-1].split('.')[0]
            except:
                tmp = None
            country.append(tmp)
            # print('country',tmp)
            #title
            try:
                tmp = s.find('span',class_='summary').get_text()
            except:
                tmp = None
            title.append(tmp)
            # print('title',tmp)
            #tourtype
            try:
                tmp = s.find('span',class_='trip-type-nights').get_text()
            except:
                tmp = None
            tourtype.append(tmp)
            # print('tourtype',tmp)
        # print('-------------')

        next_button = BeautifulSoup(driver.page_source).find('a', class_='cta cta-secondary cta-next')
        # print(next_button)
        if next_button!=None:
            # scrollable_div = driver.find_element_by_xpath("//div[@class='widget-overlay reviews-overlay widget-overlay-ajax widget-overlay-active']")
            # driver.execute_script('arguments [0] .scrollTop = arguments [0] .scrollHeight', scrollable_div)
            driver.find_element_by_xpath("//a[contains(text(),'下一頁')]").click()
            driver.implicitly_wait(3)
            time.sleep(5)
        else:
            break
    df = pd.DataFrame({'姓名':name, '星數':stars, '時間':times, '內容':content,'簡評':title,'國籍':country,'類型':tourtype})
    driver.quit()
    return df
target = pd.read_excel('飯店景點爬蟲範圍.xlsx')
for l in range(len(target)):
    file_name = target.loc[l, '名稱']
    url =str(target.loc[l,'Hotel.com網址'])
    if file_name!='nan' and str(url) != 'nan':
        print(file_name, url)
        df= get_hotelcom_map_reviews(url)
        print('共有%s筆' % len(df['姓名']))
        # print('--------------------')
        df.to_excel('./Hotel_com/%s_hotel_com_reviews.xlsx'%file_name,index=False)