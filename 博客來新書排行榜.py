# -*- coding: utf-8 -*-
"""
Created on Thu Aug  4 12:22:44 2022

@author: shirley
"""

import requests
from bs4 import BeautifulSoup

kindno = 1   # 要下載的書籍分類，預設為第1分類:文學小說
homeurl = "https://www.books.com.tw/web/books_nbtopm_01/?v=1&o=5"
mode = '?v=1&o=5'
url = "http://www.books.com.tw/web/books_nbtopm_"
# 讓網頁判斷我們不是機器人 (下面 headers那行)
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
html = requests.get(homeurl,headers=headers).text
soup = BeautifulSoup(html,'lxml')


# 中文新書分類，取得分類資訊
res = soup.find('div',class_='mod_b type02_l001-1 clearfix')
hrefs = res.select("a")    # 找出所有a
print(hrefs)

kind = hrefs[kindno-1].text
print(kind)

# 算總共有幾頁
def showkind(url,kind):
    html = requests.get(url,headers=headers).text
    soup = BeautifulSoup(html,'html.parser') 
    try:    #有可能只有一頁，避免出錯，所以抓頁碼放try
        pages=int(soup.select('.cnt_page span')[0].text)  # 該分類共有多少頁
        print("共有",pages,"頁")
        for page in range(1,pages+1):
            pageurl=url + '&page=' + str(page).strip()
            print("第",page,"頁",pageurl)
            showpage(pageurl,kind)
    except:    #如無分頁，會執行此函數
        showpage(url,kind)     
    
def showpage(url,kind):
    return

showkind(homeurl,kind)

# 把個位數的分類號碼 前面補0
def twobyte(kindno):
    if kindno < 10:
        kindnostr = '0' + str(kindno)
    else:
        kindnostr = str(kindno)
    return kindnostr

twobyte(9)

def showpage(url, kind):
    html = requests.get(url, headers = headers).text
    sp = BeautifulSoup(html, "lxml")
    #近期新書 在 class = "mod type02_m012 clearfix"中
    res = sp.find_all('div', class_= "mod type02_m012 clearfix")[0]
    items = res.select(".item")     #所有item
#     print(res) 
#     print(items[0])

    n=0   # 計算該分頁共有多少本書
    for item in items:
        msg = item.select('.msg'[0])               # 0 表示取第一個
        src = item.select('a img')[0]["src"]
        title=msg.select("a")[0].text              # 書名
        imgurl=src.split("?i=")[-1].split("&")[0]  # 圖片網址
        author=msg.select("a")[1].text
        publish=msg.select("a")[2].text              
        data=msg.find("span").text.split(":")[-1]    # -1 就是取最後一個  #出版日期
        onsale=item.select(".price .set2")[0].text
        content=item.select(".txt_cont")[0].text.replace(" ","").strip()     #内容 //.replace("空格","")
        print("\n分類:" + kind)
        print("書名: " + title)
        print("圖片網址：" + imgurl)
        print("作者:" +  author)
        print("出版社：" +  publish)
        print("出版日期:" + date)
        print(onsale)    #優惠價
        print("內容:"+content)
        n+=1
        print("n=",n)

# 主程式
list1=[]    
kindno=1  # 要下載的分類，預設為第 1分類：文學小說
homeurl = 'https://www.books.com.tw/web/books_nbtopm_01/?o=5&v=1'
mode="?o=5&v=1" #顯示模式：直式  排序依：暢銷度
url="https://www.books.com.tw/web/books_nbtopm_" 
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
html = requests.get(homeurl,headers=headers).text
soup = BeautifulSoup(html,'html.parser') 

#中文書新書分類，取得分類資訊
res = soup.find('div', class_='mod_b type02_l001-1 clearfix')
hrefs=res.select("a")

kindno=int(input("請輸入要下載的分類："))
if 0 < kindno <= len(hrefs):
    kind=hrefs[kindno-1].text #分類名稱
    print("下載的分類編號：{}   分類名稱：{}" .format(kindno,kind))
    # 下載指定的分類
    kindurl=url + twobyte(kindno) + mode # 分類網址  
    showkind(kindurl,kind) # 顯示該分類所有書籍   
    
    print("資料寫入Excel中，請等侯幾分鐘!")
    workbook=openpyxl.Workbook()
    sheet = workbook.worksheets[0]
    listtitle=["分類","書名","圖片網址","作者","出版社","出版日期","優惠價","內容"]
    sheet.append(listtitle)
    for item1 in list1: #資料
        sheet.append(item1)
        sleep(0.1) # 必須加上適當的 delay  
    workbook.save('books.xlsx')
else:
    print("分類不存在!") 
print("資料儲存完畢!")  

