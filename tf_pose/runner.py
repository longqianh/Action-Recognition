import sys
sys.path.append('..')
import base64
import os
import cv2
from functools import lru_cache
from tf_pose import common
from tf_pose import eval
from tf_pose.estimator import TfPoseEstimator
from tf_pose.networks import get_graph_path, model_wh


Estimator = TfPoseEstimator


@lru_cache(maxsize=1)
def get_estimator(model='cmu', resize='0x0'):
    w, h = model_wh(resize)
    if w == 0 or h == 0:
        e = TfPoseEstimator(get_graph_path(model), target_size=(432, 368))
    else:
        e = TfPoseEstimator(get_graph_path(model), target_size=(w, h))

    return e


def infer(image, model='cmu', resize='0x0', resize_out_ratio=4.0):
    """

    :param image:
    :param model:
    :param resize:
    :param resize_out_ratio:
    :return: coco_style_keypoints array

    """
    
    w, h = model_wh(resize)
    
    

    # estimate human poses from a single image !
    image = common.read_imgfile(image, None, None)
    if image is None:
        raise Exception('Image can not be read, path=%s' % image)
    humans = e.inference(image, resize_to_default=(
        w > 0 and h > 0), upsample_size=resize_out_ratio)
    # image_h, image_w = image.shape[:2]
    image = TfPoseEstimator.draw_humans(image, humans, imgcopy=False)
    cv2.imshow('img',image)
    cv2.waitKey(0)
    # 网络传输图片
    # image_str = cv2.imencode(".jpg", image)[1].tostring() 
    # print("\033]1337;File=name=;inline=1:" +
          # base64.b64encode(image_str).decode("utf-8") + "\a")
    # for human in humans:
    #     eval.write_coco_json(human, image_w, image_h)
    
    # return [(eval.write_coco_json(human, image_w, image_h), human.score) for human in humans]
    # return [(eval.write_kps(human, image_w, image_h), round(human.score)) for human in humans]
    return [(eval.write_normkps(human), round(human.score)) for human in humans]

def format_kps(human):
    keypoints = []
    coco_ids = [0, 15, 14, 17, 16, 5, 2, 6, 3, 7, 4, 11, 8, 12, 9, 13, 10]
    for coco_id in coco_ids:
        if coco_id not in human.body_parts.keys():
            keypoints.extend([0, 0, 0])
            continue
        body_part = human.body_parts[coco_id]
        keypoints.extend([body_part.x,
                          body_part.y,body_part.score])
    return keypoints   
    # C, T, V, M = 3, 50, 18, 2 
    # 50,M,18,3

def get_kps(video_path, model='cmu', resize='0x0', resize_out_ratio=4.0):
    videoCapture = cv2.VideoCapture(video_path)
    success=1
    e = get_estimator(model, resize)
    cnt=0
    res=[]
    while success:
        cnt+=1
        if cnt>50:
            break
        success, frame = videoCapture.read()
        w, h = model_wh(resize)
        humans = e.inference(frame, resize_to_default=(
        w > 0 and h > 0), upsample_size=resize_out_ratio)
        # if len(humans)>=1:
        res.append(format_kps(human) for human in humans[:1])
        # else:
        #     res.append(format_kps(humans[0]))
    
    return res

if __name__ == '__main__':
    
    # print(infer('cxk391.jpg'))
    video_path='cxk.mp4'
    import numpy as np

    print(np.array(get_kps(video_path))[0])
    


