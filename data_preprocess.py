import pandas as pd
import cv2
import numpy as np
# import tensorflow as tf
import json

import os
import sys
from os.path import abspath, join, dirname
sys.path.insert(0, join(abspath(dirname(__file__)), 'data'))
print(sys.path[0])


made = 1
if made == 0:
    img = cv2.imread('test.jpg')
    img = img.tolist()
    img_json = json.dumps(img)
    with open("db.json", "w") as f:
        json.dump(img, f)
        print("加载入文件完成...")


# load json files
with open("./data/outputxytest.json", "r") as f:
    img1 = json.load(f)
    print("加载入文件完成...")
print(img1)
# img1 = np.array(img1)
# print(img1.shape)
# cv2.imshow()
