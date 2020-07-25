import argparse
import logging
import time
import json
import cv2
import numpy as np
import sys
sys.path.append('..')
from tf_pose.estimator import TfPoseEstimator
from tf_pose.networks import get_graph_path, model_wh

# fps_time = 0


class detect():

    def __init__(self, video_path):
        self.videopath = video_path

    def video_detect(self):
        logger = logging.getLogger('TfPoseEstimator-Video')
        logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        logger.debug('initialization %s : %s' %
                     ('mobilenet_thin', get_graph_path('mobilenet_thin')))
        w = 432
        h = 368
        e = TfPoseEstimator(get_graph_path(
            'mobilenet_thin'), target_size=(w, h))
        cap = cv2.VideoCapture(self.videopath)
        ret_val, imgs = cap.read()
        if cap.isOpened() is False:
            print("Error opening video stream or file")

        i = 1
        output = {}
        while ret_val:
            j = 1

            humans = e.inference(imgs)

            output_humans = {}
            if len(humans) > 0:

                for h in humans:

                    output_human = {}
                    for k in range(18):
                        if k in h.body_parts.keys():
                            output_human[k] = [h.body_parts[k].x,
                                               h.body_parts[k].y, h.body_parts[k].score]

                    output_human[19] = h.score
                    output_humans[j] = output_human
                    j = j + 1
                output[i] = output_humans

            imgs = np.zeros(imgs.shape)
            # imgs = TfPoseEstimator.draw_humans(imgs, humans, imgcopy=False)
            # videoWriter.write(imgs)
            fps_time = time.time()
            i = i + 1
            ret_val, imgs = cap.read()

        filename = 'outputtest.json'
        with open(filename, 'w') as file_obj:
            json.dump(output, file_obj)

        logger.debug('finished+')


video_path = 'cxk.mp4'


def video_detect(video_path):
    w, h = 432, 368
    e = TfPoseEstimator(get_graph_path(
        'mobilenet_thin'), target_size=(w, h))
    cap = cv2.VideoCapture(video_path)
    if cap.isOpened() is False:
        print("Error opening video stream or file")

    i = 1
    output = {}
    while ret_val:
        j = 1

        humans = e.inference(imgs)

        output_humans = {}
        if len(humans) > 0:

            for h in humans:
                output_human = {}
                for k, item in h.body_parts:

                    # for k in range(18):
                    #     if k in h.body_parts.keys():
                    output_human[k] = [h.body_parts[k].x,
                                       h.body_parts[k].y, h.body_parts[k].score]

                output_human[19] = h.score
                output_humans[j] = output_human
                j = j + 1
            output[i] = output_humans

        imgs = np.zeros(imgs.shape)
        # imgs = TfPoseEstimator.draw_humans(imgs, humans, imgcopy=False)
        # videoWriter.write(imgs)
        fps_time = time.time()
        i = i + 1
        ret_val, imgs = cap.read()

    # filename = 'outputtest.json'
    # with open(filename, 'w') as file_obj:
    #     json.dump(output, file_obj)
    logger.debug('finished+')
    return output


video_detect(video_path)
# i = 1
# output = {}
# while ret_val:
#     j = 1

#     humans = e.inference(imgs)

#     output_humans = {}
#     if len(humans) > 0:

#         for h in humans:

#             output_human = {}
#             for k in range(18):
#                 if k in h.body_parts.keys():
#                     output_human[k] = [h.body_parts[k].x,
#                                        h.body_parts[k].y, h.body_parts[k].score]

#             output_human[19] = h.score
#             output_humans[j] = output_human
#             j = j + 1
#         output[i] = output_humans

#     imgs = np.zeros(imgs.shape)
#     # imgs = TfPoseEstimator.draw_humans(imgs, humans, imgcopy=False)
#     # videoWriter.write(imgs)
#     fps_time = time.time()
#     i = i + 1
#     ret_val, imgs = cap.read()

# filename = 'outputtest.json'
# with open(filename, 'w') as file_obj:
#     json.dump(output, file_obj)

# logger.debug('finished+')
