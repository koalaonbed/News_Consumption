from PIL import Image, ImageDraw, ImageFont
import os
from pathlib import Path
import pandas as pd
import csv
import json

import io
import re
from google.cloud import vision_v1
from google.cloud.vision_v1 import AnnotateImageResponse

OCR_PATH = '/mnt/4T_disk/Lab_News_Consumption/Lab_News_Consumption/split_posts/test_set/all/'
CONCAT_PATH = '/mnt/4T_disk/Lab_News_Consumption/Lab_News_Consumption/split_posts/test_set/concat/'
RECORD_PATH = '/mnt/4T_disk/Lab_News_Consumption/Lab_News_Consumption/split_posts/test_set/facebook_concat.csv'
RESULT_PATH = '/mnt/4T_disk/Lab_News_Consumption/Lab_News_Consumption/split_posts/test_set/ocr_o.csv'
EDGE_PATH = "/mnt/4T_disk/Lab_News_Consumption/Lab_News_Consumption/split_posts/test_set/first_inference_official-3.csv"
maindir = '/mnt/4T_disk/Lab_News_Consumption/Lab_News_Consumption/split_posts/test_set/original/'
user = 'U2'
conn = ''

credential_path = '/mnt/4T_disk/Lab_News_Consumption/Lab_News_Consumption/split_posts/news-consumption-75e59d31bf22.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

BY_ORIENTATION = False
extra_len = 20

## JPEG/JFIF supports a maximum image size of 65,535×65,535 pixels
## The 12000 x 6500 image happens to be over this limit.
"""
def concat_images(kind, images, dst_filename):
    width = kind[0]
    height = kind[1]
    orientation = kind[2]
    print(CONCAT_PATH + dst_filename)
    if not os.path.exists(CONCAT_PATH):
        os.makedirs(CONCAT_PATH)
    if orientation:
        if BY_ORIENTATION:
            dst = Image.new('RGB', ((width+extra_len)*len(images), height))
            for i,image_path in enumerate(images):
                #print(image_path)
                dst.paste(Image.open(image_path), (((width+extra_len)*i),0))
            dst.save(CONCAT_PATH + dst_filename + '.jpg')
            imgsize = os.path.getsize(CONCAT_PATH + dst_filename+ '.jpg')
            #print(dst_filename, str(imgsize/1000000))
            return imgsize
        else:
            dst = Image.new('RGB', (width, (height+extra_len)*len(images)))
            for i,image_path in enumerate(images):
                dst.paste(Image.open(image_path), (0,((height+extra_len)*i)))
            dst.save(CONCAT_PATH + dst_filename + '.jpg')
            imgsize = os.path.getsize(CONCAT_PATH + dst_filename+ '.jpg')
            #print(dst_filename, str(imgsize/1000000))
            return imgsize
    else:
        dst = Image.new('RGB', (width, (height+extra_len)*len(images)))
        for i,image_path in enumerate(images):
            dst.paste(Image.open(image_path), (0,((height+extra_len)*i)))
        dst.save(CONCAT_PATH + dst_filename + '.jpg')
        imgsize = os.path.getsize(CONCAT_PATH + dst_filename+ '.jpg')
        #print(dst_filename, str(imgsize/1000000))
        return imgsize
    
    

def get_images(OCR_PATH, CONCAT_PATH, kind, sectors):
    if BY_ORIENTATION:
        if orientation:
            constant = width+extra_len
            one_img_size = (width+extra_len) * height
        else:
            constant = height+extra_len
            one_img_size = width * (height+extra_len)
    else:
        constant = kind[1]+extra_len
        one_img_size = kind[0] * (kind[1]+extra_len)
        

    rows = sectors.get_group(kind).iterrows()
    
    records = []
    
    images = []
    cumulative_len = 0
    cnt = 0
    for index, row in rows:
        print(row.img)
        filename = row.img
        cumulative_len = cumulative_len + constant 

        if cumulative_len >= 65500 or (one_img_size*(len(images)+1)) >= 75000000:
            img_size = concat_images(kind, images , str(kind[1])+'_'+str(kind[0]) +'_' +str(cnt))
            writer.writerow((str(kind[1])+'_'+str(kind[0]) +'_' +str(cnt),';'.join(images), kind[0], kind[1], kind[2], img_size, len(images)))
            #print(str(cumulative_len-constant))
            images = []
            cumulative_len = constant
            cnt = cnt + 1
        images.append(os.path.join(maindir,str(row.qid),filename))
        
    img_size = concat_images(kind, images, str(kind[1])+'_'+str(kind[0]) +'_' +str(cnt))  
    #print(str(kind[1])+'_'+str(kind[0]) +'_' +str(cnt),';'.join(images), kind, img_size, len(images))
    writer.writerow((str(kind[1])+'_'+str(kind[0]) +'_' +str(cnt),';'.join(images), kind[0], kind[1], kind[2], img_size, len(images)))
    
 



#print("File Size In Bytes:- "+str(len(image_file.fp.read()))

def concat_images_by_image_size(OCR_PATH, CONCAT_PATH, sectors):
    
    
    
    for kind in sectors.groups:
        print(kind)
        get_images(OCR_PATH, CONCAT_PATH, kind, sectors)
        
        #for index,row in sectors.get_group(kind).iterrows():
            
    
    return

def OCR(path):
    #Detects text in the file.
    
    client = vision_v1.ImageAnnotatorClient()
    for img in sorted(os.listdir(path)):
        if ".jpg" not in img:
            continue
            
        #print(path+img)
        
        code = 0
        message = ""
        with io.open(path+img, 'rb') as image_file:
            Content = image_file.read()
        image = vision_v1.Image(content=Content)
        
        vision_client = vision_v1.ImageAnnotatorClient()
        #response = vision_client.annotate_image({'image': {'content': Content}, 'image_context':{"language_hints": ["zh-Hant"]}, 'features': [{'type_': vision_v1.Feature.Type.DOCUMENT_TEXT_DETECTION,'model': "builtin/legacy"}]})
        response = client.document_text_detection(image=image)
        texts = response.text_annotations

        filename = img.replace('.jpg', '.json')
        
        if response.error.message:
            raise Exception(
                '{}\nFor more info on error messages, check: '
                'https://cloud.google.com/apis/design/errors'.format(
                    response.error.message))
            code = 1
            message = response.error.message
        
        #cur.execute('UPDATE _ocr_files SET code=? , message=? WHERE filename = ?;',(code, message, img.replace('.jpg', '')))
        #conn.commit()
            
        
        # serialize / deserialize proto (binary)
        serialized_proto_plus = AnnotateImageResponse.serialize(response)
        response = AnnotateImageResponse.deserialize(serialized_proto_plus)
        #print(response.full_text_annotation.text)

        # serialize / deserialize json
        response_json = AnnotateImageResponse.to_json(response)
        response = json.loads(response_json)
        #print(response['fullTextAnnotation']['text'])

        #print json string
        #print(response_json)
        
        if not os.path.exists(os.path.join(path,'ocr')):
            os.makedirs(os.path.join(path,'ocr'))

        with open(os.path.join(path,'ocr',filename), 'w' , encoding='utf8') as output_file:
            json.dump(response, output_file, ensure_ascii=False)
            
        #os.remove(path+img)

#conn = sqlite3.connect(boredom_db)
#Users = select_all_formal_users(conn)

# main
#for user in Users:
    #print('user : '+ user)
#if not os.path.exists(OCR_PATH + user):
    #os.makedirs(OCR_PATH + user)
file = pd.read_csv(EDGE_PATH)
sectors = file.groupby(['width','height','orientation'])

csvFile = open(RECORD_PATH, 'a', encoding="utf-8-sig")
writer = csv.writer(csvFile)

concat_images_by_image_size(OCR_PATH, CONCAT_PATH, sectors)
OCR(CONCAT_PATH)
print('done')
#close the connection
#conn.close()
"""
import numpy as np
import time 
from shapely.geometry import Polygon
from enum import Enum
from types import SimpleNamespace
#import scipy.io as io


class FeatureType(Enum):
    PAGE = 1
    BLOCK = 2
    PARA = 3
    WORD = 4
    SYMBOL = 5

def cal_intersection_2poly(in1, in2):
    s1 = np.array(in1).reshape(int(len(in1)/2), 2)
    s2 = np.array(in2).reshape(int(len(in2)/2), 2)
    #print(s1)
    poly1 = Polygon(s1).convex_hull
    poly2 = Polygon(s2).convex_hull
    if not poly1.intersects(poly2):
        inter_area = 0
    else:
        inter_area = poly1.intersection(poly2).area
    return inter_area, poly1.intersection(poly2)

def ck_bound(bound, height, width,orientation):
    if orientation:
        if BY_ORIENTATION:
            s = int(bound.vertices[0].x/(width + extra_len))
            for i in range(1, len(bound.vertices)):
                if s != int(bound.vertices[i].x/(width + extra_len)):
                    print('error', bound)
                    break

        else:
            s = int(bound.vertices[0].y/(height + extra_len))
            for i in range(1, len(bound.vertices)):
                if s != int(bound.vertices[i].y/(height + extra_len)):
                    print('error', bound)
                    break

    else:
        s = int(bound.vertices[0].y/(height + extra_len))
        for i in range(1, len(bound.vertices)):
            if s != int(bound.vertices[i].y/(height + extra_len)):
                print('error', bound)
                break

def get_bound_by_image_idx(bound, height, width,orientation):
    if orientation:
        if BY_ORIENTATION:
            s = int(bound[0]/(width + extra_len))
            for i in range(int(len(bound)/2)):
                bound[i*2] = bound[i*2] - (s * (width + extra_len))
            return bound,s

        else:
            s = int(bound[1]/(height + extra_len))
            for i in range(int(len(bound)/2)):
                bound[i*2+1] = bound[i*2+1] - (s * (height + extra_len))
            return bound,s

    else:
        s = int(bound[1]/(height + extra_len))      
        for i in range(int(len(bound)/2)):
            bound[i*2+1] = bound[i*2+1]- (s * (height + extra_len))
        return bound,s
    
    
def convertBoundingBox(bound):
    out = []
    for i in range(len(bound.vertices)):
        out.append(bound.vertices[i].x)
        out.append(bound.vertices[i].y)
    return out
    
def get_bounding_box(flag_fix, jsonObj, height, width,orientation, tag):
    bound = json.loads(json.dumps(jsonObj[tag]), object_hook=lambda d: SimpleNamespace(**d))
    out = convertBoundingBox(bound) 
    if flag_fix:
        #ck_bound(bound, height, width,orientation)   
        if BY_ORIENTATION:
            if orientation:
                s = [int(bound.vertices[0].x/(width + extra_len))]
                for i in range(1, len(bound.vertices)):
                    s_idx = int(bound.vertices[i].x/(width + extra_len))
                    s.append(s_idx)
                cover = list(set(s))
                cover.sort()
                if len(cover) != 1:
                    #print(cover) 
                    max_area = 0

                    for image_idx in cover:
                        v1 = [(width + extra_len)* image_idx, 0]
                        v2 = [(width + extra_len)* image_idx, height]
                        v3 = [(width + extra_len)* image_idx + width-1, 0]
                        v4 = [(width + extra_len)* image_idx + width-1, height ]
                        poly = v1 + v2 + v3 + v4
                        area, b = cal_intersection_2poly(poly,convertBoundingBox(bound))
                        #print(area,b)
                        if area > max_area:
                            max_bound_list = b
                            max_area = area
                    if max_area == 0:
                        out = None
                    else:
                        out = []        
                        for x,y in max_bound_list.exterior.coords:
                            out = out + [x, y]

                else:
                    for i in range(len(bound.vertices)):
                        bound.vertices[i].x = bound.vertices[i].x if (bound.vertices[i].x % (width + extra_len)) < width else int(bound.vertices[i].x / (width + extra_len))*(width + extra_len) +widt-1 
                    out = convertBoundingBox(bound) 
            else:
                s = [int(bound.vertices[0].y/(height + extra_len))]
                for i in range(1, len(bound.vertices)):
                    s_idx = int(bound.vertices[i].y/(height + extra_len))
                    s.append(s_idx)
                cover = list(set(s))
                cover.sort()
                if len(cover) != 1:
                    #print(cover) 
                    max_area = 0

                    for image_idx in cover:
                        v1 = [0, (height + extra_len)* image_idx]
                        v2 = [width, (height + extra_len)* image_idx]
                        v3 = [0, (height + extra_len)* image_idx + height-1]
                        v4 = [width, (height + extra_len)* image_idx + height-1]
                        poly = v1 + v2 + v3 + v4
                        area, b = cal_intersection_2poly(poly,convertBoundingBox(bound))
                        #print(area,b)
                        if area > max_area:
                            max_bound_list = b
                            max_area = area
                    if max_area == 0:
                        out = None
                    else:
                        out = []        
                        for x,y in max_bound_list.exterior.coords:
                            out = out + [x, y]

                else:
                    for i in range(len(bound.vertices)):
                        bound.vertices[i].y = bound.vertices[i].y if (bound.vertices[i].y % (height + extra_len)) < height else int(bound.vertices[i].y / (height + extra_len))*(height + extra_len) +height-1  
                    out = convertBoundingBox(bound) 
        else:
            s = [int(bound.vertices[0].y/(height + extra_len))]
            for i in range(1, len(bound.vertices)):
                s_idx = int(bound.vertices[i].y/(height + extra_len))
                s.append(s_idx)
            cover = list(set(s))
            cover.sort()
            if len(cover) != 1:
                #print(cover) 
                max_area = 0
                
                for image_idx in cover:
                    v1 = [0, (height + extra_len)* image_idx]
                    v2 = [width, (height + extra_len)* image_idx]
                    v3 = [0, (height + extra_len)* image_idx + height-1]
                    v4 = [width, (height + extra_len)* image_idx + height-1]
                    poly = v1 + v2 + v3 + v4
                    area, b = cal_intersection_2poly(poly,convertBoundingBox(bound))
                    #print(area,b)
                    if area > max_area:
                        max_bound_list = b
                        max_area = area
                if max_area == 0:
                    out = None
                else:
                    out = []        
                    for x,y in max_bound_list.exterior.coords:
                        out = out + [x, y]      
            else:
                for i in range(len(bound.vertices)):
                    bound.vertices[i].y = bound.vertices[i].y if (bound.vertices[i].y % (height + extra_len)) < height else int(bound.vertices[i].y / (height + extra_len))*(height + extra_len) +height-1  
                out = convertBoundingBox(bound) 
    return out


def get_document_bounds(flag_fix, filename, feature, height, width, orientation):
    # [START detect_bounds]
    bounds =[]
    with open(CONCAT_PATH+'ocr/'+filename + '.json', encoding='utf8') as f:
        response = json.load(f)
    
    texts = []
    cnt = []
    #print(response)
    if "fullTextAnnotation" in response: 
        document = response['fullTextAnnotation']
        # Collect specified feature bounds by enumerating all document features
        all_texts =[]
        for page in document['pages']:
            page_texts = []
            for block in page['blocks']:
                block_texts = []
                for paragraph in block['paragraphs']:
                    paragraph_texts = []
                    for word in paragraph['words']:
                        #print("".join(s['text'] for s in word['symbols']))
                        word_texts = []
                        for symbol in word['symbols']:
                            word_texts.append(symbol['text'])
                            if (feature == FeatureType.SYMBOL):
                                b = get_bounding_box(flag_fix, symbol, height, width, orientation, 'boundingBox') 
                                if b is None:
                                    continue
                                bounds.append(b)
                                texts.append(symbol['text'])
                                cnt.append(len(symbol['text']))

                        if (feature == FeatureType.WORD):
                            b = get_bounding_box(flag_fix, word, height, width, orientation, 'boundingBox') 
                            if b is None:
                                continue
                            bounds.append(b)
                            texts.append(''.join(word_texts))
                            cnt.append(1)
                        paragraph_texts.append(''.join(word_texts))

                    if (feature == FeatureType.PARA):
                        b = get_bounding_box(flag_fix, paragraph, height, width, orientation, 'boundingBox') 
                        if b is None:
                            continue
                        bounds.append(b)
                        texts.append(' '.join(paragraph_texts))
                        cnt.append(len(paragraph_texts))
                    block_texts.append(' '.join(paragraph_texts))

                if (feature == FeatureType.BLOCK):
                    b = get_bounding_box(flag_fix, block, height, width, orientation, 'boundingBox') 
                    if b is None:
                        continue
                    bounds.append(b)
                    texts.append(' '.join(block_texts))
                    cnt.append(len(block_texts))
                page_texts.append(' '.join(block_texts))

            if (feature == FeatureType.PAGE):
                b = get_bounding_box(flag_fix, block, height, width, orientation, 'boundingBox') 
                if b is None:
                    continue
                bounds.append(b)
                texts.append(' '.join(page_texts))
                cnt.append(len(page_texts))
            all_texts.append(' '.join(page_texts))

    # The list `bounds` contains the coordinates of the bounding boxes.
    # [END detect_bounds]
    return bounds, texts, cnt


def getImageIndexByBoundingBox(bounds, height, width,orientation):
    idxlist = []
    bounds_for_each_image = []
    for i in range(len(bounds)): 
        b, idx = get_bound_by_image_idx(bounds[i], height, width,orientation)
        idxlist.append(idx)
        bounds_for_each_image.append(b)
    return bounds_for_each_image, idxlist

def ck_duplicate(images, bounds, cnt, idx, texts):
    a = []
    for i in range(len(bounds)): 
        a.append(str(idx[i])+'_'+(','.join([str(int) for int in bounds[i]])))
        
    seen = set()
    dupes = []

    for x in a:
        if x in seen:
            dupes.append(x)
        else:
            seen.add(x)
    if len(dupes) > 0:
        print(dupes)            
    for i in range(len(bounds)): 
        t = str(idx[i])+'_'+','.join([str(int) for int in bounds[i]])
        if t in dupes:
            print(texts[i])
        
    
def insert_into_db(conn, PID,  images, bounds, cnt, idx, texts):
    records = []
    ck_duplicate(images, bounds, cnt, idx, texts)
    for i in range(len(bounds)): 
        t = ','.join([str(int) for int in bounds[i]])
        records.append((t, texts[i], cnt[i], images[idx[i]] ))
    
    cur = conn.cursor()
    cur.executemany('INSERT OR IGNORE INTO _ocr_paragraph (PID, record_time, bounding_box, description, word_cnt) SELECT PID, record_time, ? AS bounding_box, ? AS description, ? AS word_cnt  FROM images WHERE images.filename = ? ;',records);

    if not (len(records)) == cur.rowcount:
        print('All records of', PID, 'are', str(len(records)))
        print('And we have inserted', cur.rowcount, 'records to the table.')

    #commit the changes to db           
    conn.commit()
    
    
def get_images(images_path):
    #images = images_path.replace('1/','')
    #images = images.replace('2/','')
    #images = images.replace('3/','')
    #images = images.replace('4/','')
    #images = images.replace('0/','')
    return images_path.split(';')
        
def parse_OCR_files():      
    #cur = conn.cursor()
    #cur.execute("SELECT filename, merge_from, height, width, orientation FROM _ocr_files WHERE PID = ?", (PID,))
    #rows = cur.fetchall()
    read_file = open(RECORD_PATH, "r",encoding="utf-8-sig")
    rows = csv.reader(read_file)


    edge_df = pd.read_csv(EDGE_PATH)
    edge_df = edge_df.set_index('img')
    print(edge_df)


    with open(RESULT_PATH, 'a', newline='', encoding="utf-8-sig") as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(['user', 'qid', 'images', 'pid', 'context', 'n_main', 'percent', 'comment'])

    
    for row in rows:
        [filename, merge_from, width, height, orientation, size, nums] = row
        width = int(width)
        height = int(height)
        orientation = int(orientation)
        nums = int(nums)
        #print(row)
        #print(filename)
        
        images = get_images(merge_from)
        
        bounds, texts, cnt = get_document_bounds(True, filename, FeatureType.PARA, height, width, orientation)
        #print(texts)
        new_bounds, idx = getImageIndexByBoundingBox(bounds, height, width,orientation)
        #print(new_bounds)

        text_image = [''] * nums
        


        
        

        idx_serie = list(dict.fromkeys(idx))
        #print(idx_serie)
        


        for i, name in enumerate(images):
            print(name)
            flag_comment = -1
            text_one = ''
            #edge_list = edge_df.loc[edge_df['img']==filename,'edge'].values[0]
            edge_str = edge_df.at[name.rsplit('/',2)[2],'edge']

            """
            for j,(ida, bnd) in enumerate(zip(idx,new_bounds)):
                if i==ida:
                    
                    if '2021-03-27-19-16-02'in name:
                        print(texts[j])
                        print(bnd[0],bnd[1],bnd[2],bnd[3],bnd[4],bnd[5],bnd[6],bnd[7])
                        print('讚' in texts[j])
                        print('回覆' in texts[j])
                    
                    try:
                        if ('讚' in texts[j] and '回覆' in texts[j+1]) or ('讚' in texts[j] and '回覆' in texts[j]):
                            print("YESSSSSSS!!!!")
                            #if new_bounds[j+1][0]-new_bounds[j][2]< width/6:
                            print("NOOO!!!!")
                            if edge_str is np.nan:
                                edge_str = str(bnd[1]-90)
                            else:
                                edge_str += '_'+str(bnd[1]-90)
                            flag_comment = bnd[1]-90
                            print(name,texts[j],texts[j+1])
                            print(bnd[0],bnd[1],bnd[2],bnd[3],bnd[4],bnd[5],bnd[6],bnd[7])
                            break
                    except:
                        print('Bottom Warning')
            """
            #print(edge_str)
            if str(edge_str) == 'nan':
                c_flag = 0

                for j,(ida, bnd) in enumerate(zip(idx,new_bounds)):
                    if (bnd[1]+bnd[7])/2 > height*87/100 or (bnd[1]+bnd[7])/2 < height*13/100:
                        continue
                    if i ==ida:
                        text_one += texts[j] + '\n'

                        if texts[j]=='回覆':
                            c_flag += 1


                with open(RESULT_PATH, 'a', newline='', encoding="utf-8-sig") as csvFile:
                    writer = csv.writer(csvFile)
                    
                    writer.writerow([user, name.rsplit('/',2)[1],name.rsplit('/',2)[2], 0, text_one, edge_df.at[name.rsplit('/',2)[2],'n_main'],0.74,0])
            else:
                edge_list = str(edge_str).split('_')
                edge_int = list(map(int, edge_list))
                edge_int.sort()

                edge_int = list(filter(lambda num: num >= height*13/100  and num <= height*87/100, edge_int))

                # check special case
                if len(edge_int) >= 2:
                    for ed in range(1,len(edge_int)):
                        if edge_int[ed] - edge_int[ed-1] < height*0.15:
                            edge_int.pop(ed)
                            break
                
                edge_int.insert(0,height*13/100)
                edge_int.append(height*87/100)
                #print(edge_int)
                

                texts_pid = [''] * (len(edge_int) - 1) 
            
                for j,(ida, bnd) in enumerate(zip(idx,new_bounds)):
                    if (bnd[1]+bnd[7])/2 > height*87/100 or (bnd[1]+bnd[7])/2 < height*13/100:
                        continue
                    if i==ida:
                        #print(texts[j])
                        #print(new_bounds[j])
                        for k in range(len(edge_int)-1):
                            if (bnd[1]+bnd[7])/2 > edge_int[k] and (bnd[1]+bnd[7])/2 <= edge_int[k+1]:
                                texts_pid[k] += texts[j] + '\n'
                            """
                            if k == 0:
                                if (bnd[1]+bnd[7])/2 < edge_int[0]:
                                    texts_pid[k] += texts[j] + '\n'
                            elif k == len(edge_int):
                                if (bnd[1]+bnd[7])/2 > edge_int[k-1]:
                                    texts_pid[k] += texts[j] + '\n'
                            else:
                                if (bnd[1]+bnd[7])/2 > edge_int[k-1] and (bnd[1]+bnd[7])/2 < edge_int[k]:
                                    texts_pid[k] += texts[j] + '\n'
                            """

                #print(len(texts_pid))
                for p in range(len(texts_pid)):
                    with open(RESULT_PATH, 'a', newline='', encoding="utf-8-sig") as csvFile:
                        if flag_comment == -1:
                            writer = csv.writer(csvFile)
                            writer.writerow([user, name.rsplit('/',2)[1],name.rsplit('/',2)[2], p, texts_pid[p], edge_df.at[name.rsplit('/',2)[2],'n_main'], (edge_int[p+1]-edge_int[p])/height,0])
                        
                        elif (edge_int[p+1]>flag_comment and edge_int[p]<flag_comment) or (edge_int[p+1]>flag_comment+90 and edge_int[p]<flag_comment+90):

                            writer = csv.writer(csvFile)
                            writer.writerow([user, name.rsplit('/',2)[1],name.rsplit('/',2)[2], p, texts_pid[p], edge_df.at[name.rsplit('/',2)[2],'n_main'], (edge_int[p+1]-edge_int[p])/height,1])
                        
                        else:

                            writer = csv.writer(csvFile)
                            writer.writerow([user, name.rsplit('/',2)[1],name.rsplit('/',2)[2], p, texts_pid[p], edge_df.at[name.rsplit('/',2)[2],'n_main'], (edge_int[p+1]-edge_int[p])/height,0])
                        
                    """
                    if texts_pid[0] == '':
                        if p == 0:
                            continue
                        elif p == (len(texts_pid)-1):
                            if texts_pid[p] == "":
                                continue
                            with open(RESULT_PATH, 'a', newline='', encoding="utf-8-sig") as csvFile:
                                writer = csv.writer(csvFile)
                                writer.writerow([user, name.rsplit('/',2)[1],name.rsplit('/',2)[2], p-1, texts_pid[p], edge_df.at[name.rsplit('/',2)[2],'n_main'], (height-edge_int[p-1])/height-0.13])
                        elif p == 1:
                            with open(RESULT_PATH, 'a', newline='', encoding="utf-8-sig") as csvFile:
                                writer = csv.writer(csvFile)
                                writer.writerow([user, name.rsplit('/',2)[1],name.rsplit('/',2)[2], p-1, texts_pid[p], edge_df.at[name.rsplit('/',2)[2],'n_main'], edge_int[p]/height-0.13])
                        
                        else:
                            with open(RESULT_PATH, 'a', newline='', encoding="utf-8-sig") as csvFile:
                                writer = csv.writer(csvFile)
                                writer.writerow([user, name.rsplit('/',2)[1],name.rsplit('/',2)[2], p-1, texts_pid[p], edge_df.at[name.rsplit('/',2)[2],'n_main'], (edge_int[p]-edge_int[p-1])/height])
                    else:
                        if p == (len(texts_pid)-1):
                            if texts_pid[p] == "":
                                continue
                            with open(RESULT_PATH, 'a', newline='', encoding="utf-8-sig") as csvFile:
                                writer = csv.writer(csvFile)
                                writer.writerow([user, name.rsplit('/',2)[1],name.rsplit('/',2)[2], p, texts_pid[p], edge_df.at[name.rsplit('/',2)[2],'n_main'], (height-edge_int[p-1])/height-0.13])
                        elif p == 0:
                            with open(RESULT_PATH, 'a', newline='', encoding="utf-8-sig") as csvFile:
                                writer = csv.writer(csvFile)
                                writer.writerow([user, name.rsplit('/',2)[1],name.rsplit('/',2)[2], p, texts_pid[p], edge_df.at[name.rsplit('/',2)[2],'n_main'], edge_int[p]/height-0.13])

                        else:
                            with open(RESULT_PATH, 'a', newline='', encoding="utf-8-sig") as csvFile:
                                writer = csv.writer(csvFile)
                                writer.writerow([user, name.rsplit('/',2)[1],name.rsplit('/',2)[2], p, texts_pid[p], edge_df.at[name.rsplit('/',2)[2],'n_main'], (edge_int[p]-edge_int[p-1])/height])
                    """
            
    return 
# main
parse_OCR_files()
print('done')
