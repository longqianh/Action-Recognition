import torch
import sys
sys.path.append('..')
# json process
import json

filename = 'outputtest.json'
with open(filename, 'r') as file:
  dict_json = json.load(file)

# print(dict_json)
# print(dict_json[str(201)][str(1)][str(5)][2])

# joint data ( ~ json )
N, C, T, V, M = 1, 3, 50, 18, 2
input_joint = torch.zeros(C, T, V, M)
for t in range(T):
  if str(t + 1) in dict_json:
    for m in range(M):
      if not (str(m + 1) in dict_json[str(t + 1)]):
        m = m - 1
      for v in range(V):
        if str(v) in dict_json[str(t + 1)][str(m + 1)]:
          for c in range(C):
            input_joint[c][t][v][m] = dict_json[str(
                t + 1)][str(m + 1)][str(v)][c]
  else:
    break

# print(input_joint)

# joint data ( fake )
# N, C, T, V, M = 1, 3, 50, 18, 2
# input_joint = torch.randn(N, C, T, V, M)

# bone data ( ~ joint data )
bone_pairs = (
    (0, 0), (1, 0), (2, 1), (3, 2), (4, 3), (5,
                                             1), (6, 5), (7, 6), (8, 2), (9, 8), (10, 9),
    (11, 5), (12, 11), (13, 12), (14, 0), (15, 0), (16, 14), (17, 15)
)  # for kinetics only !
C, T, V, M = input_joint.shape
input_bone = torch.zeros(C, T, V, M)
input_bone[:C, :, :, :] = input_joint
for v1, v2 in bone_pairs:
  input_bone[:, :, v1, :] = input_joint[:, :, v1, :] - input_joint[:, :, v2, :]

# '''
import torch.nn.functional as F
from model import msg3d

# choose model
# choose model
model_joint = msg3d.Model(num_class=400, num_point=18, num_person=2,
                          num_gcn_scales=8, num_g3d_scales=8, graph='graph.kinetics.AdjMatrixGraph')
model_bone = msg3d.Model(num_class=400, num_point=18, num_person=2,
                         num_gcn_scales=8, num_g3d_scales=8, graph='graph.kinetics.AdjMatrixGraph')
PATH_joint = './pretrained-models/kinetics-bone.pt'
PATH_bone = './pretrained-models/kinetics-joint.pt'
model_joint.load_state_dict(torch.load(PATH_joint))
model_bone.load_state_dict(torch.load(PATH_bone))
model_joint.eval()
model_bone.eval()


# print(input_joint.shape)
# print(input_bone.shape)
# output
alpha = 0.5  # weight of 2stream

output_joint = model_joint(input_joint)
# print(output_joint)
prediction_joint = torch.max(output_joint, dim=1)
print('Prediction of joint-model : ', prediction_joint.indices)

output_bone = F.softmax(model_bone(input_bone), dim=1)
prediction_bone = torch.max(output_bone, dim=1)
print('Prediction of bone-model : ', prediction_bone.indices)

out = alpha * output_joint + (1 - alpha) * output_bone
# print(out)
res = out.argmax()
print(res)
# prediction_fusion = torch.max(out, dim=1)
# print('Prediction of fusion : ', prediction_fusion.indices)
# '''
