import difflib
import csv
import re
import pandas as pd

user = 'U2'
filename = '/mnt/4T_disk/Lab_News_Consumption/Lab_News_Consumption/split_posts/test_pilot/ocr_U2.csv'
compare_filename = '/mnt/4T_disk/Lab_News_Consumption/Lab_News_Consumption/split_posts/test_pilot/U2'
keyword_filename = 'news_keyword3.txt'

char_repeat = 8



fi = open(keyword_filename, 'r')
lines = fi.readlines()
#print(lines)
text = ""
for i,line in enumerate(lines):
    print(line)
    if i==0:
        text += line[0:-1]
    else:
        text += '|'
        text += line[0:-1]
print(text)



"""
if len(ind)<10:
    continue
if (len(ind)<20):
    if ('讚' in ind) + ('回應' in ind) + ('留言' in ind) + ('分享' in ind) >= 2:
        continue
"""



#print(posts[100][2])








df = pd.read_csv(filename)
df.insert(8, 'outer_link', 0)
df.insert(9, 'code_id', -5)
df.insert(10, 'news', -1)
df.insert(11, 'keyword', -1)
df.insert(12, 'biggest', 0)
#df.insert(9, 'comment', 0)


for i in df.index: 

    df.loc[i,"context"] = str(df.loc[i,"context"])
    df.loc[i,'context'] = df.loc[i,'context'].replace(' ','')
    df.loc[i,'context'] = df.loc[i,'context'].replace('\n','')
    
    if df.loc[i, 'n_main'] == 0:
        if len(df.loc[i,"context"])<char_repeat:
            df.loc[i,"code_id"] = -2

        if df.loc[i, 'n_main'] == 0 and df.loc[i, 'comment'] == 1:
            df.loc[i, 'code_id'] = -2

        #if (len(df.loc[i,"context"])<20):
        #    if ('讚' in df.loc[i,"context"]) + ('回應' in df.loc[i,"context"]) + ('留言' in df.loc[i,"context"]) + ('分享' in df.loc[i,"context"]) >= 2:
        #        df.loc[i,"code_id"] = -2

    match = re.search(text, df.loc[i,"context"])
    if match:

        df.loc[i,"news"] = 1
        df.loc[i,"keyword"] = match.group(0)
    else:
        df.loc[i,"news"] = 0
        df.loc[i,"keyword"] = 0


    if df.loc[i, 'n_main'] == 1:
        df.loc[i, 'outer_link'] = 1 
    elif df.loc[i, 'n_main'] == 2:
        df.loc[i, 'comment'] = 1 

#print(df.iloc[711])


cnt = 0
for i in df.index: 

    group = []
    
    img = df.loc[i,'images'].split('-')
    #print(img)
    time = int(img[4])*3600 + int(img[5])*60 + int(img[6])
    
    group.append(i)
    
    if df.loc[i,"code_id"] != -5:
        continue
    
    if df.loc[i,'n_main'] == 0: 
        

        for j in df.iloc[i+1:].index:
            """
            if j == 1436:
                print(i)
                print(cnt)
                print(group)
            """
            if df.loc[j,"code_id"] != -5:
                continue

            if df.loc[i, 'qid'] != df.loc[j, 'qid']:
                break

            if df.loc[i, 'n_main'] != df.loc[j, 'n_main']:
                continue

            img_tmp = df.loc[j,'images'].split('-')
            time_tmp = int(img_tmp[4])*3600 + int(img_tmp[5])*60 + int(img_tmp[6])
            if time_tmp - time > 60:
                break

            p = difflib.SequenceMatcher(None, df.loc[i,"context"], df.loc[j,"context"]).find_longest_match(0, len(df.loc[i,"context"]), 0, len(df.loc[j,"context"]))

            if p[2]>=char_repeat:
                #print(row['context'][p[0]:p[0]+p[2]])
                group.append(j)
                time = time_tmp

        
    else:
        for j in df.iloc[i+1:].index:
            if df.loc[j,"code_id"] != -5:
                continue

            if df.loc[i, 'qid'] != df.loc[j, 'qid']:
                
                break

            if df.loc[i,'n_main'] == df.loc[j,'n_main']:
                group.append(j)

            else:
                break
                
                
    for k in group:
        df.loc[k,'code_id'] = cnt
    cnt += 1

#print(df.iloc[711])
#print(df.iloc[710])


fig_dataframe = []    
pic_num = 0
df.insert(11, 'picture_number', -1)

for index in df.index:     
    image = df.at[index, 'images']
    if image not in fig_dataframe: #一篇貼文的第一張照片
        pic_num += 1 
        df.loc[index, 'picture_number'] = pic_num 
        fig_dataframe.append(image)
    else:
        df.loc[index, 'picture_number'] = pic_num

for i in df.index:
    print(i)
    #if i == 711:
     #   print(df.iloc[711])

    # First post
    if i==0 and df.loc[i, 'code_id'] == -2:
    
        df.loc[i, 'code_id'] = df[df['picture_number'] == df.loc[i, 'picture_number']+1].iloc[0]['code_id']
    
    # Last post
    elif i==df.index[-1] and df.loc[i, 'code_id'] == -2:
        
        df.loc[i, 'code_id'] = df[df['picture_number'] == df.loc[i, 'picture_number']-1].iloc[0]['code_id']

    # bottom post with few words and top post of next pic with few words
    elif df.loc[i, 'code_id'] == -2 and df.loc[i+1, 'code_id'] == -2 and df.loc[i+1, 'pid'] == 0:
        try:
            df.loc[i+1, 'code_id'] = df.loc[i-2, 'code_id']
        except:
            df.loc[i+1, 'code_id'] = cnt
            cnt += 1
        try:
            df.loc[i, 'code_id'] = df.loc[i+2, 'code_id']
        except:
            df.loc[i, 'code_id'] = cnt
            cnt += 1
        

    # Top post with few words
    elif df.loc[i, 'code_id'] == -2 and df.loc[i, 'pid'] == 0:
        
        mask = df['images']==df.loc[i, 'images'] #篩選條件
        
        if df.loc[i, 'qid'] != df[df['picture_number'] == df.loc[i, 'picture_number']-1].iloc[-1]['qid'] :
            df.loc[i, 'code_id'] = df.loc[i+1, 'code_id']

            for j in df.iloc[i+1:].index:
                if df.loc[j, 'code_id'] >= 0:
                    df.loc[j, 'code_id'] += 1
            cnt += 1


        # there is only a post in a picture
        elif df.loc[mask].shape[0] == 1:
            df.loc[i, 'code_id'] = df[df['picture_number'] == df.loc[i, 'picture_number']-1].iloc[-1]['code_id']
        else:
            # Is code_id of next post same as the code_id of last post of previous picture
            if df.loc[i+1, 'code_id'] != df[df['picture_number'] == df.loc[i, 'picture_number']-1].iloc[-1]['code_id']:
                df.loc[i, 'code_id'] = df[df['picture_number'] == df.loc[i, 'picture_number']-1].iloc[-1]['code_id']
            else:
                df.loc[i, 'code_id'] = df[df['picture_number'] == df.loc[i, 'picture_number']-1].iloc[0]['code_id']
    

print(pic_num)


for i in reversed(df.index):
    
    #if i == 53:
    #    print(df.iloc[53])

    
    

    if df.loc[i,'picture_number']==pic_num and df.loc[i, 'code_id'] == -2:
        df.loc[i, 'code_id'] = df[df['picture_number'] == df.loc[i, 'picture_number']-1].iloc[0]['code_id']

    # bottom post with few words
    elif df.loc[i, 'code_id'] == -2 and df.loc[i+1, 'pid'] == 0:
        #print(i,df.loc[i,'picture_number'])
        #print(df[df['picture_number'] == df.loc[i, 'picture_number']+1])
        if df.loc[i, 'qid'] != df[df['picture_number'] == df.loc[i, 'picture_number']+1].iloc[0]['qid'] :
            df.loc[i, 'code_id'] = df.loc[i-1, 'code_id'] + 1

            for j in df.iloc[i+1:].index:
                if df.loc[j, 'code_id'] >= 0:
                    df.loc[j, 'code_id'] += 1
            cnt += 1
        
        # Is code_id of last post same as the top post of next pic
        elif df.loc[i+1, 'code_id'] == df.loc[i-1, 'code_id']:
            df.loc[i, 'code_id'] = df.loc[i+2, 'code_id']
        else:
            df.loc[i, 'code_id'] = df.loc[i+1, 'code_id']

#flag_code = 0

for i in df.index:
    if df.loc[i, 'code_id'] == -3:

        # 留言區的上方就是該則貼文，則 code_id 一樣
        if df.loc[i, 'pid'] != 0 :
            df.loc[i, 'code_id'] = df.loc[i-1, 'code_id']

        else:
            continue


for i in df.index:
    flag_code = 0
    print(i)
    if df.loc[i, 'code_id'] == -3 :
                
        for k in range(1,20):
            if df.loc[i+1+k, 'code_id'] == df.loc[i+1, 'code_id'] and df.loc[i+k, 'n_main'] == 0 and df.loc[i+k, 'comment'] == 1 and df.loc[i+k, 'code_id'] >= 0 :
                df.loc[i, 'code_id'] = df.loc[i+k, 'code_id']
                flag_code = 1
                break

            elif df.loc[i-k-1, 'code_id'] == df.loc[i+1, 'code_id'] and df.loc[i-k-2, 'n_main'] == 0 and df.loc[i-k-2, 'comment'] == 1 and df.loc[i-k-2, 'code_id'] >= 0 :
                df.loc[i, 'code_id'] = df.loc[i-k-2, 'code_id']
                flag_code = 1
                break
        
        if flag_code == 0:
            df.loc[i, 'code_id'] = cnt
            cnt += 1


        
        

        

"""
for i in df.index:
    if flag_code > 0 and df.loc[i, 'code_id'] > 0:
        flag_code -= 1
        if flag_code == 0:
            cnt+=1
    if df.loc[i, 'code_id'] == -2 and df.loc[i, 'comment'] == 1:
        if flag_code >0:
            df.loc[i, 'code_id'] = cnt
            flag_code = 8
        else:
            for k in range(10):
                if df.loc[i+k, 'n_main'] == 0 and df.loc[i+k, 'comment'] == 1 and df.loc[i+k, 'code_id'] >= 0:
                    df.loc[i, 'code_id'] = df.loc[i+k, 'code_id']
                    break
                if df.loc[i-k, 'n_main'] == 0 and df.loc[i-k, 'comment'] == 1 and df.loc[i-k, 'code_id'] >= 0:
                    df.loc[i, 'code_id'] = df.loc[i-k, 'code_id']
                    break
    if df.loc[i, 'code_id'] == -2 and df.loc[i, 'comment'] == 1:
        df.loc[i, 'code_id'] = cnt
        flag_code = 8
    
    if i == df.index[-1] and flag_code>0 :
        cnt += 1
"""
        
    

    
for i in df.index:
    if df.loc[i, 'code_id'] < 0:
        df.loc[i]
        print(i, df.loc[i, 'code_id'],  "ERROR!!!!")
        print(df.loc[i])
        
    """
    elif df.loc[i, 'code_id'] == -2 and df.loc[i+1, 'pid'] == 0:
        if df.loc[i+1, 'code_id'] != df[df['picture_number'] == df.loc[i, 'picture_number']-1].iloc[-1]['code_id']:
            df.loc[i, 'code_id'] = df[df['picture_number'] == df.loc[i, 'picture_number']-1].iloc[-1]['code_id']
        else:
            df.loc[i, 'code_id'] = df[df['picture_number'] == df.loc[i, 'picture_number']-1].iloc[0]['code_id']
    """

access = []
max_per = 0
max_row = 0

for i in df.index:
    if df.loc[i,'n_main'] == 0:
        
        if df.loc[i, 'percent'] > max_per:
            max_per = df.loc[i, 'percent']
            max_row = i

        if i == df.index[-1] or df.loc[i, 'images'] != df.loc[i+1, 'images']:
            max_per = 0
            df.loc[max_row, 'biggest'] = 1


        access.append(i)
    else:
        df.loc[i, 'biggest'] = 1

#df = df.drop( df[ (df['n_main']==0) & (df['percent']!=0.74) ].index )





order = [None] * cnt

cnt = 0

# Change code_id into ascending order
for i in df.index:
    
    if order[ df.loc[i, 'code_id'] ] == None:
        order[ df.loc[i, 'code_id'] ] = cnt
        cnt += 1
        #print(df.loc[i, 'code_id'], cnt)

print(order)

for i in df.index:
    df.loc[i, 'code_id'] = order[df.loc[i, 'code_id']]


cnt = 0
start = 0
end = 0
serie = 1
cid = 0
# size = 1000

df.reset_index(inplace=True, drop=True)

for i in df.index:
    cnt += 1
    if df.loc[i, 'code_id'] > cid:
        cid = df.loc[i, 'code_id']
    if serie > 1:
        df.loc[i, 'code_id'] = df.loc[i, 'code_id'] - cid_k
        
    if cnt > 1000 or i==df.index[-1]:
        if i==df.index[-1] or df.loc[i, 'qid'] != df.loc[i+1, 'qid'] :
            end = i
            df[start:end+1].to_csv(compare_filename + '-' + str(serie) + '.csv',index=False, encoding='utf_8_sig')
            serie += 1
            start = i+1
            cnt = 0
            cid_k = cid + 1
            #print(cid_k)
            



#df.to_csv(compare_filename,index=False, encoding='utf_8_sig')


"""

for i,post in enumerate(posts):
    data = []
    img = []
    detail = []
    count = 1
    
    print(i)
    #print(posts[i][2])
    if i in access:
        continue
    img.append(posts[i][1])
    detail.append(str(posts[i][0]) + '_' + str(posts[i][1]) + '_' + str(posts[i][2]))
    for j in range(i+1,len(posts)):
        if j in access:
            continue
        if posts[j][0]!=posts[i][0]:
            break
        p = difflib.SequenceMatcher(None, posts[i][3], posts[j][3]).find_longest_match(0, len(posts[i][3]), 0, len(posts[j][3]))
        #po = difflib.SequenceMatcher(None, posts[i][3], posts[j][3]).quick_ratio
        if p[2]>=18:
            print(posts[i][3][p[0]:p[0]+p[2]])
            count+=1
            access.append(j)
            img.append(posts[j][1])
            detail.append(str(posts[j][0]) + '_' + str(posts[j][1]) + '_' + str(posts[j][2]))
            #data.append(raw[j][3])
            if len(posts[j][3])>len(posts[i][3]):
                posts[i][3] = posts[j][3]
    
    num += 1
    print(num,p)
    data.append(user)
    data.append(int(posts[i][0]))
    data.append('\n'.join(img))
    data.append('\n'.join(detail))
    data.append(posts[i][3])
    data.append(count)

    match = re.search(text, posts[i][3])
    if match:

        data.append(1)
        data.append(match.group(0))
    else:
        data.append('0')
        data.append('0')

    with open(compare_filename, 'a', newline='', encoding="utf-8-sig") as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(data)
    #print(access)
       
"""
   






