import pandas as pd
import cv2
import numpy as np


import json

# make json files
made = 1
if made == 0:
    img = cv2.imread('./data/test.jpg')
    img = img.tolist()
    img_json = json.dumps(img)
    with open("./data/db.json", "w") as f:
        json.dump(img, f)
        print("加载入文件完成...")


# load json files
with open("./data/db.json", "r") as f:
    img1 = json.load(f)
    print("加载入文件完成...")

img1 = np.array(img1)
print(img1.shape)
