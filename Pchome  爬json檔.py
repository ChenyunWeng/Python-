# -*- coding: utf-8 -*-
import requests
import json
import pandas as pd
import time


key = '化妝品收納架'
url = 'https://ecshweb.pchome.com.tw/search/v3.3/all/results?q=%E5%8C%96%E5%A6%9D%E5%93%81%E6%94%B6%E7%B4%8D%E6%9E%B6&page=1'
list_req = requests.get(url)
#將整個網站的程式碼爬下來
getdata = json.loads(list_req.content)

# 蒐集多頁的資料，打包成csv檔案
alldata = pd.DataFrame() # 準備一個容器

for i in range(1,10):
    # 要抓取的網址
    url = 'https://ecshweb.pchome.com.tw/search/v3.3/all/results?q='+key+'&page='+str(i)
    list_req = requests.get(url)
    #將整個網站的程式碼爬下來
    getdata = json.loads(list_req.content)

    todataFrame = pd.DataFrame(getdata['prods']) # 轉成Dataframe格式
    alldata = pd.concat([alldata, todataFrame]) # 將結果裝進容器
    
    time.sleep(5) #拖延時間
    
# 儲存檔案
alldata.to_csv('PChome.csv', # 名稱
               encoding='utf-8-sig', # 編碼 
               index=False) # 是否保留Index    
