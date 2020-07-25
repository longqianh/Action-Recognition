from flask import Flask,abort, request, jsonify,make_response
import random
import threading
from watchdog.observers import Observer
from watchdog.events import *
import sys
sys.path.append('MS_G3D')
import json
import torch
import torch.nn.functional as F
from model import msg3d

app = Flask(__name__)

idpool=[]
result={}
path=r"/usr/local/nginx/html/live"
filename = 'outputtest.json' # for test

def init_model():
    model_joint = msg3d.Model(num_class=400, num_point=18, num_person=2, num_gcn_scales=8, num_g3d_scales=8, graph='graph.kinetics.AdjMatrixGraph')
#    model_bone = msg3d.Model(num_class=400, num_point=18, num_person=2, num_gcn_scales=8, num_g3d_scales=8, graph='graph.kinetics.AdjMatrixGraph')
    PATH_joint = './pretrained-models/kinetics-bone.pt'
#    PATH_bone = './pretrained-models/kinetics-joint.pt'
    model_joint.load_state_dict(torch.load(PATH_joint))
#    model_bone.load_state_dict(torch.load(PATH_bone))
    model_joint.eval()
#    model_bone.eval()
    return model_joint
    


def videodetect(model,vedio):
    print("Detecting")
    pred = torch.max(F.softmax(model(vedio), dim=1), dim=1)
    print(f"Action Prediction : {pred}")
    





class MyHandler (FileSystemEventHandler):
    def __init__(self):
        FileSystemEventHandler.__init__(self)

    def on_created(self, event):
        print("file created:{}".format(event.src_path))
        if event.src_path[-2:]=='ts':
            t = threading.Thread(target=self.process, args=(event.src_path,))
            t.start()

    def on_deleted(self, event):
        print("file deleted:{}".format(event.src_path))

    def get_name(self,src):
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
            break;
    idpool.append(ID)
    result[ID]='Hhhhh'
    print(result)
    print(idpool)
    return ID


@app.route('/getresult')
def getresult():
    id=request.args.get("ID")
    ids=result.keys()
    if id in ids:
        return result[id]
    else:
        return "None"

if __name__ == '__main__':
    observer = Observer()
    event_handler= MyHandler()
    observer.schedule(event_handler, path, True)
    observer.start()
    app.run(host='0.0.0.0',port=443)
