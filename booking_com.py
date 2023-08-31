from selenium import webdriver
import time
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import warnings
import pandas as pd
warnings.filterwarnings('ignore')

# url ='https://www.booking.com/hotel/tw/grand-hyatt-taipei-taipei50.zh-tw.html?label=gen173nr-1FCAEoggI46AdIM1gEaOcBiAEBmAEwuAEHyAEM2AEB6AEB-AELiAIBqAIDuALklN2EBsACAdICJDkzNWYxNjI5LTY0MmItNDg2YS1hNDEyLWM5MzBlMjJhMjI5ZNgCBuACAQ;sid=2ab02ce540e928dadb64aec3aa531cf6;dest_id=-2637882;dest_type=city;dist=0;group_adults=2;group_children=0;hapos=1;hpos=1;no_rooms=1;room1=A%2CA;sb_price_type=total;sr_order=popularity;srepoch=1620527737;srpvid=f713123c522e0179;type=total;ucfs=1&#tab-reviews'
def get_bookingcom_map_reviews(url):
    chrome_options = Options()  # 啟動無頭模式
    # chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get(url)
    # driver.implicitly_wait(3)
    # driver.find_element_by_xpath("//a[@id='show_reviews_tab']").click()
    # driver.find_element_by_xpath("//section[@class='_3Ddcd6']/a").click()
    driver.implicitly_wait(3)
    time.sleep(2)
    name = []
    stars = []
    times = []
    content_positive = []
    content_negative = []
    country=[]
    title =[]
    tourtype=[]
    while True:
    # for y in range(2):
        soup = BeautifulSoup(driver.page_source).find_all('li',class_='review_list_new_item_block')
        for s in soup:
            # name
            try:
                tmp = s.find('div',class_='c-review-block__row c-review-block__guest').find('span', class_='bui-avatar-block__title').get_text().strip()
            except:
                tmp = None
            name.append(tmp)
            print('name', tmp)
            # stars
            try:
                tmp = s.find('div', class_='bui-review-score__badge').get_text().strip()
            except:
                tmp = None
            stars.append(tmp)
            print('stars', tmp)
            # times
            try:
                tmp = s.find('span', class_='c-review-block__date').get_text().strip()
            except:
                tmp = None
            times.append(tmp)
            print('times', tmp)
            # content_positive
            try:
                tmp = s.find('div', class_='c-review__row').get_text().strip()
            except:
                tmp = None
            content_positive.append(tmp)
            print('content_positive', tmp)

            # content_negative
            try:
                tmp = s.find('div', class_='c-review__row lalala').get_text().strip()
            except:
                tmp = None
            content_negative.append(tmp)
            print('content_negative', tmp)
            # country
            try:
                tmp = s.find('span', class_='bui-avatar-block__subtitle').get_text().strip()
            except:
                tmp = None
            country.append(tmp)
            print('country', tmp)
            # title
            try:
                tmp = s.find('div',class_='bui-grid__column-10').find('h3').get_text().strip()
            except:
                tmp = None
            title.append(tmp)
            print('title', tmp)
            # tourtype
            try:
                tmp = s.find('ul',class_='bui-list bui-list--text bui-list--icon bui_font_caption review-panel-wide__traveller_type c-review-block__row').find('div', class_='bui-list__body').get_text().strip()
            except:
                tmp = None
            tourtype.append(tmp)
            print('tourtype', tmp)
        print('-------------')

        scrollable_div = driver.find_element_by_xpath("//div[@class='sliding-panel-widget-content review_list_block one_col']")
        driver.execute_script('arguments [0] .scrollTop = arguments [0] .scrollHeight', scrollable_div)
        driver.implicitly_wait(3)
        time.sleep(3)
        driver.execute_script('arguments [0] .scrollTop = arguments [0] .scrollHeight', scrollable_div)
        driver.implicitly_wait(3)
        if len(driver.find_elements_by_xpath("//a[@class='pagenext']"))>0:
            driver.find_element_by_xpath("//a[@class='pagenext']").click()
            driver.implicitly_wait(3)
        else:
            break
    df = pd.DataFrame({'姓名': name, '星數': stars, '時間': times, '正面評論': content_positive, '負面評論': content_negative, '簡評': title, '國籍': country, '類型': tourtype})
    driver.quit()
    return df

target = pd.read_excel('飯店景點爬蟲範圍.xlsx')
for l in range(len(target)):
    file_name = target.loc[l, '名稱']
    url = str(target.loc[l, 'Booking.com網址'])
    if file_name != 'nan' and str(url) != 'nan':
        print(file_name, url)
        df = get_bookingcom_map_reviews(url)
        print('共有%s筆' % len(df['姓名']))
        print('--------------------')
        df.to_excel('./Booking_com/%s_booking_com_reviews.xlsx' % file_name, index=False)

