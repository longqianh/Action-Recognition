from flask import Flask, abort, request, jsonify, make_response
import random
import threading
from watchdog.observers import Observer
from watchdog.events import *
import sys
sys.path.append('MS_G3D')
import json

app = Flask(__name__)

idpool = []
result = {}
path = r"/usr/local/nginx/html/live"
filename = 'outputtest.json'  # for test


def create_graph(filename="model.pb"):
    graph_def = tf.compat.v1.GraphDef()
    with tf.io.gfile.GFile(filename, 'rb') as f:
        graph_def.ParseFromString(f.read())
        tf.import_graph_def(graph_def, name='')
   
def array_init_reshape(x):
    # x should be ndarray
    # x = np.expand_dims(x, 0)
    C, T, V, M = 3, 50, 18, 2
    return x.transpose(3,2,0,1).reshape(M * V * C, T)[:,0]# bug that need to be fixed

def videodetect(model, vedio):
    import tensorflow as tf
    import numpy as np
    print("Detecting")
    filename = "msg3d.pb"
    create_graph(filename)
    # show_nodename()

    input_name = 'data_bn.bias:0'
    output_name = 'mul_1:0'

    C, T, V, M = 3, 50, 18, 2
    test_input = np.ones((C, T, V, M))
    test_input = array_init_reshape(test_input)
    # print(test_input.shape)

    # test_input = test_input[0, :, 0]
    with tf.compat.v1.Session() as sess:
        input_node = sess.graph.get_tensor_by_name(input_name)
        output_node = sess.graph.get_tensor_by_name(output_name)
        # print(input_node)
        class_id = sess.run(output_node, {input_node: test_input})
        print(np.argmax(class_id))
    return np.argmax(class_id)

class MyHandler (FileSystemEventHandler):
    def __init__(self):
        FileSystemEventHandler.__init__(self)

    def on_created(self, event):
        print("file created:{}".format(event.src_path))
        if event.src_path[-2:] == 'ts':
            t = threading.Thread(target=self.process, args=(event.src_path,))
            t.start()

    def on_deleted(self, event):
        print("file deleted:{}".format(event.src_path))

    def get_name(self, src):
        return src[27:34]

    def process(self, p):
        ID = self.get_name(p)
        print("Processing %s" % ID)
        videodetect(p)


@app.route('/getroom')
def getroom():
    H = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    while 1:
        id = random.sample(H, 7)
        ID = ''.join(id)
        if ID not in idpool:
            break
    idpool.append(ID)
    result[ID] = 'Hhhhh'
    print(result)
    print(idpool)
    return ID


@app.route('/getresult')
def getresult():
    id = request.args.get("ID")
    ids = result.keys()
    if id in ids:
        return result[id]
    else:
        return "None"


if __name__ == '__main__':
    observer = Observer()
    event_handler = MyHandler()
    observer.schedule(event_handler, path, True)
    observer.start()
    app.run(host='0.0.0.0', port=443)
