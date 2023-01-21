SJA
=============


# How to train SJA
1. Scrutinize screenshots to view what kind of unique features is associated to the event you are interested in
2. use labelImg(https://github.com/heartexlabs/labelImg) to annotate image
3. use YOLO to train

# How to build SJA to infer
1. Use YOLO to predict object & OCR to infer texts and their boundaries
2. Apply condition expression to identify event and split media units
3. Each media unit has its text, calculate their similarity to judge if they are the same media units or not
4. Determine the media unit is news or not by searching if it contains the keyword from the whitelist of news organizations
5. output the CSV

# How to implement
1. [first_inference_0912.py](https://github.com/koalaonbed/News_Consumption/blob/main/first_inference_0912.py)
2. [OCR_size.py](https://github.com/koalaonbed/News_Consumption/blob/main/OCR_size.py)
3. [third_split_compare.py](https://github.com/koalaonbed/News_Consumption/blob/main/third_split_compare.py)

# Rules of Facebook screenshots

* Rules

| Events or split | Rules |
| ---------------- | -------------------------------------------------------------- |
| Split posts | The upper boundary of "three_dots" (upper right at every post) |
|  opening external link      |  labeled 6 kinds of external link's headers |
| viewing comments | 上方的 ">" 和 "讚"   &   下方的 "留言框" |


* Labels in Facebook
https://docs.google.com/presentation/d/1qUElYN8_q6ycYiinwAJWs9vJpD1zuEvrSzLonbqFJO4/edit#slide=id.g11da0161188_0_31



# Reference
* https://cloud.google.com/vision/docs/ocr
* https://github.com/AlexeyAB/darknet/tree/darknet_yolo_v3_optimal
