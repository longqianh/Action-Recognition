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
