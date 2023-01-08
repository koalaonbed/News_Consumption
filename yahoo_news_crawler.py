# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 14:29:55 2020

@author: MUILab-VR
"""
import bs4
from bs4 import BeautifulSoup
import requests
import csv
import re
import time
#import schedule
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

#print(bs4.__version__)


while(1):
#Query How many times
    try:
        with open('yahoo_news10.csv', 'a', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["ID", "Title", "channel", "Publish Time", "comments"])
    
    
        
            options = Options()
            options.add_argument("--disable-notifications")
            options.add_argument("--incognito")
            #Private surfing in chrome
            options.add_argument("--headless")
            #Execute in background
            
            chrome = webdriver.Chrome('/mnt/4T_disk/yahoo_popular_news/chromedriver', options=options)
            chrome.get("https://tw.news.yahoo.com/most-popular")
            # Open the browser and load Yahoo hot news
            time.sleep(1)
            
            
            t = time.localtime()
            time_now = time.strftime("%Y%m%d-%H%M%S", t)
            #title = str(time_now) + "-" + j.zfill
            #newslist.append(time_now)
            #f = open(str(filename),'w',encoding='utf-8')
            #r = requests.get("https://tw.news.yahoo.com/most-popular")
            #r.encoding = 'utf-8'
            
            
            
            # Scroll to the bottom
            for i in range(1,10):
                js = "var q=document.documentElement.scrollTop=100000"
                chrome.execute_script(js)
                time.sleep(2)
            
            
            # Beautiful soup query data
            soup = BeautifulSoup(chrome.page_source, 'html.parser')
            
            NewsTitleList = soup.find_all(class_ = "js-stream-content Pos(r)")
            count =0
            
            for k, NewsTitle in enumerate(NewsTitleList):
                
                
                seq = str(time_now) + "-" + str(count).zfill(3)
                # News sequence in the page
                
                try:
                    title = NewsTitle.select("div div div h3 a")[0].text
                    #print("新聞標題:" + title)
                    #print(NewsTitle.find(class_='Py(14px) Pos(r)').find(class_='Cf').find(class_='Ov(h) Pend(14%) Pend(44px)--sm1024').find(class_='C(#959595) Fz(13px) C($c-fuji-grey-f)! D(ib) Mb(6px)').text)
                    if NewsTitle.find('img'):
                        # News with image
                        brand = NewsTitle.find(class_='Py(14px) Pos(r)').find(class_='Cf').find(class_='Ov(h) Pend(44px) Pstart(25px)').find(class_='C(#959595) Fz(13px) C($c-fuji-grey-f)! D(ib) Mb(6px)').text
                    else:
                        #News without image
                        brand = NewsTitle.find(class_='Py(14px) Pos(r)').find(class_='Cf').find(class_='Ov(h) Pend(14%) Pend(44px)--sm1024').find(class_='C(#959595) Fz(13px) C($c-fuji-grey-f)! D(ib) Mb(6px)').text
                
                    #print("新聞頻道:" + brand)
                    
                    comment_html = NewsTitle.find(class_='Py(14px) Pos(r)').find(class_='Cf').find(class_='Pos(a) T(14px) End(0) W(36px) Ta(c) NoJs_D(n) Mt(20px)').find(class_='comment-btn-link Pos(r) Cur(p) Va(m) Td(n) D(ib) Pb(6px) desktop_W(100%)').get('aria-label')
                    #print(comment_html)
                    comment = comment_html.split('留言。點選')[0]
                    if comment =='':
                        comment = '0'
                    """
                    if NewsTitle.find('img'):
                        # News with image
                        
                        comment_html = NewsTitle.select("div div div")[4].select("a")[0]
                        comment_end = [m.start() for m in re.finditer('留言', str(comment_html))]
                        comment_start = str(comment_html).find("aria-label=\"") + len("aria-label=\"")
                    
                        
                    else:
                        # News without image
                        
                        comment_html = NewsTitle.select("div div div")[2].select("a")[0]
                        comment_end = [m.start() for m in re.finditer('留言', str(comment_html))]
                        comment_start = str(comment_html).find("aria-label=\"") + len("aria-label=\"")
                    """
                        

                    
                   
                        
                    #f.write("新聞標題:" + title + "\n")
                    #f.write("新聞標題:" + title + "\n")
                    #print("留言數:" + str(comment_html)[comment_start: comment_end[1]])
                    #f.write("留言數:" + str(comment_html)[comment_start: comment_end[1]] + "\n")
                    print("-----------------")
                    
                    
                    #f.write("-----------------" + "\n")
                    #newslist.append("新聞標題:" + title + "\n" + "新聞頻道:" + brand + "\n" + "留言數:" + str(comment_html)[comment_start: comment_end[1]])
                except:
                    print("error")
                    continue
                
                
                
                #try:
                    # "3 留言。點選即可檢視" --> "3"
                    #comment_text = str(comment_html)[comment_start: comment_end[1]].split(' ')
                    #comment = int(comment_text[0])
                #except:
                    # "留言。點選即可檢視" -->  "0"
                    #comment = 0
                
                #writer.writerow([seq, title, brand.split('•')[0], brand.split('•')[1], comment])
                #print(seq, title, brand, comment)
                writer.writerow([seq, title, brand.split('•')[0], brand.split('•')[1], comment])
                print(seq, title, brand.split('•')[0], brand.split('•')[1], comment)
                count+=1
                
        
            
            #f.close()
            chrome.close()
            
            t =time.localtime()
            m = int(time.strftime("%M",t))
            s = int(time.strftime("%S",t))
            if m<30:
                time.sleep((30-m)*60-s)
            else:
                time.sleep((60-m)*60-s)
            
    except:
        continue
    
    
    #.close()


'''
t = time.localtime()
time_now = time.strftime("%Y%m%d-%H%M%S", t)
schedule.every(1).minutes.do(crawler, time_now)
'''

'''
while True:
    schedule.run_pending()
    time.sleep(1)
 '''