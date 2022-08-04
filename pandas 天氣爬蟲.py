import pandas as pd
import requests
import json
import datetime
from dateutil.relativedelta import relativedelta   # 相對時間
import time
import random
import tqdm

areaID = '71294'
year = '2022'
month = '6'
# 要抓取的網站
url = 'http://tianqi.2345.com/Pc/GetHistory?areaInfo%5BareaId%5D='+ str(areaID)+'&areaInfo%5BareaType%5D=2&date%5Byear%5D='+str(year)+'&date%5Bmonth%5D='+str(month)

list_req = requests.get(url)
getjson = json.loads(list_req.content)
gettable = pd.read_html(getjson['data'],header = 0)
gettable[0]  # 抓到資料

#   取得大量資料，六個月資料
today = datetime.datetime.today()   #datetime.datetime #日期和时间的结合。属性：year, month, day, hour, minute, second, microsecond, and tzinfo

areaID = '71294' # 台北
containar = pd.DataFrame()   # 準備一個容器
for i in tqdm.tqdm(range(6)):
    countDay = today - relativedelta(months=i)   # 相對時間：years, months, days等，帶s結尾
    year = countDay.year
    month = countDay.month
    
    # 要抓取的網站
    url = 'http://tianqi.2345.com/Pc/GetHistory?areaInfo%5BareaId%5D='+ str(areaID)+'&areaInfo%5BareaType%5D=2&date%5Byear%5D='+str(year)+'&date%5Bmonth%5D='+str(month)
    
    print(str(i)+'開始請求')
    list_req = requests.get(url)
    print(str(i)+'請求完成')
    
    getjson = json.loads(list_req.content)
    gettable = pd.read_html(getjson['data'],header = 0)
    
    # 合併資料
    containar = pd.concat([containar, gettable[0]])


    # 休息一下
    time.sleep(random.randint(35,45))

containar.to_csv('台北天氣狀況.csv',encoding= 'utf-8-sig',index=False)    