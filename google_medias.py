from pygooglenews import GoogleNews
import csv
import time



def media(news):
    for new in news['entries']:
        f.write(new['source']['title'])
        f.write('\n')
        for article in new['sub_articles']:
            f.write(article['publisher'])
            f.write('\n')

gn = GoogleNews(lang = 'ch', country = 'TW')

f = open('/home/spencer0929/googlenews/top_news_0712.csv','a', newline='', encoding='utf-8-sig')
writer = csv.writer(f)


#print(top['entries'][0]['sub_articles'][1]['publisher'])

t = time.localtime()
time_now = time.strftime("%Y%m%d-%H%M%S", t)

top = gn.top_news()
#media(top)
#f.write(str(top))
for new in top['entries']:
    print(new['title'])
    print(new['source']['title'])
    #print(str(new))
    writer.writerow([time_now,'headline',new['title'],new['source']['title']])
    
    for i,article in enumerate(new['sub_articles']):
        if i==0:
            continue
        print(article['title'])
        writer.writerow([time_now,'sub',article['title'],article['publisher']])
        #f.write('\n')

f.close()
