import os
from os.path import dirname, abspath


def get_graph_path(model_name):
    dyn_graph_path = {
        'cmu': 'graph/cmu/graph_opt.pb',
        'openpose_quantize': 'graph/cmu/graph_opt_q.pb',
        'mobilenet_thin': 'graph/mobilenet_thin/graph_opt.pb',
        'mobilenet_v2_large': 'graph/mobilenet_v2_large/graph_opt.pb',
        'mobilenet_v2_large_r0.5': 'graph/mobilenet_v2_large/graph_r0.5_opt.pb',
        'mobilenet_v2_large_quantize': 'graph/mobilenet_v2_large/graph_opt_q.pb',
        'mobilenet_v2_small': 'graph/mobilenet_v2_small/graph_opt.pb',
    }

    base_data_dir = dirname(dirname(abspath(__file__)))
    if os.path.exists(os.path.join(base_data_dir, 'models')):
        base_data_dir = os.path.join(base_data_dir, 'models')
    else:
        base_data_dir = os.path.join(base_data_dir, 'tf_pose_data')

    graph_path = os.path.join(base_data_dir, dyn_graph_path[model_name])
    return graph_path


# print(get_graph_path('cmu'))
def to_str(s):
    if not isinstance(s, str):
        return s.decode('utf-8')
    return s


def get_graph_path(model_name):
    dyn_graph_path = {
        'cmu': 'graph/cmu/graph_opt.pb',
        # 'openpose_quantize': 'graph/cmu/graph_opt_q.pb',
        # 'mobilenet_thin': 'graph/mobilenet_thin/graph_opt.pb',
        'mobilenet_v2_large': 'graph/mobilenet_v2_large/graph_opt.pb',
        'mobilenet_v2_large_r0.5': 'graph/mobilenet_v2_large/graph_r0.5_opt.pb',
        'mobilenet_v2_large_quantize': 'graph/mobilenet_v2_large/graph_opt_q.pb',
        'mobilenet_v2_small': 'graph/mobilenet_v2_small/graph_opt.pb',
    }

    # base_data_dir = dirname(dirname(abspath(__file__)))
    # if os.path.exists(os.path.join(base_data_dir, 'models')):
    #     base_data_dir = os.path.join(base_data_dir, 'models')
    # else:
    #     base_data_dir = os.path.join(base_data_dir, 'tf_pose_data')
    base_data_dir = dirname(abspath(__file__))
    base_data_dir = os.path.join(base_data_dir, 'model')
    graph_path = os.path.join(base_data_dir, dyn_graph_path[model_name])
    # if os.path.isfile(graph_path):
    print(graph_path)
    return graph_path
    # raise Exception('Graph file doesn\'t exist, path=%s' % graph_path)


import numpy as np
import cv2
from estimator import TfPoseEstimator
import tensorflow as tf

# 耗时严重 4.7s
# tensorflow小心import 优化到了3.5s
# from networks import get_graph_path, model_wh

# cap = cv2.VideoCapture('cxk.mp4')

# # while(cap.isOpened()):
# ret, frame = cap.read()
modelpath = get_graph_path('mobilenet_v2_large')
# e = TfPoseEstimator(modelpath)


with tf.io.gfile.GFile(modelpath, 'rb') as f:
    graph_def = tf.compat.v1.GraphDef()
    graph_def.ParseFromString(f.read())


tf.compat.v1.import_graph_def(graph_def, name='TfPoseEstimator')
g = tf.compat.v1.get_default_graph()
tensor_image = g.get_tensor_by_name('TfPoseEstimator/image:0')

# 将图从graph_def导入到当前默认图中
# persistent_sess = tf.compat.v1.Session(
# #     graph=graph, config=tf_config)
# for ts in [n.name for n in tf.compat.v1.get_default_graph().as_graph_def().node]:
# print(ts)

# Session提供了Operation执行和Tensor求值的环境
# gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#     cv2.imshow('frame', frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()

# model=
