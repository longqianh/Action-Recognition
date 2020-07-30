import onnx
import torch
from model import msg3d
from onnx_tf.backend import prepare


def pt2onnx(model, dummy_input, model_path='./model.onnx'):
    torch.onnx.export(model, dummy_input, model_path, opset_version=12)


def onnx2pb(model, pb_output_path, opset_version=12):
    tf_exp = prepare(onnx_model)  # prepare tf representation
    tf_exp.export_graph(pb_output_path)  # export the model


def do_transfer():
    pt_model_path = './pretrained-models/kinetics-joint.pt'
    onnx_input_path = './msg3d.onnx'
    pb_output_path = './msg3d.pb'

    pt_model = msg3d.Model(num_class=400, num_point=18, num_person=2,
                           num_gcn_scales=8, num_g3d_scales=8, graph='graph.kinetics.AdjMatrixGraph')
    pt_model.load_state_dict(torch.load(pt_model_path))
    dummy_input = torch.randn(3, 50, 18, 2)
    dummy_input = pt_model.init_reshape(dummy_input)
    pt2onnx(pt_model, dummy_input, onnx_input_path)

    # onnx_model = onnx.load(onnx_input_path)
    # onnx2pb(onnx_model, pb_output_path)


if __name__ == "__main__":
    # do_transfer()
    # onnx_input_path = './msg3d.onnx'
    # pb_output_path = './msg3d.pb'
    # onnx_model = onnx.load(onnx_input_path)
    # onnx2pb(onnx_model, pb_output_path)

    import tensorflow as tf
    import numpy as np

    def create_graph(filename="model.pb"):
        graph_def = tf.compat.v1.GraphDef()
        with tf.io.gfile.GFile(filename, 'rb') as f:
            graph_def.ParseFromString(f.read())
            tf.import_graph_def(graph_def, name='')

    def show_nodename():
        tensor_name_list = [
            tensor.name for tensor in tf.compat.v1.get_default_graph().as_graph_def().node]
        for tensor_name in tensor_name_list:
            print(tensor_name)

    def tf_init_reshape(x):
        x = tf.expand_dims(x, 0)
        N, C, T, V, M = 1, 3, 50, 18, 2
        x = tf.keras.backend.permute_dimensions(x, (0, 4, 3, 1, 2))
        x = tf.keras.backend.reshape(x, (N, M * V * C, T))
        return x

    def array_init_reshape(x):
        # x should be ndarray
        # x = np.expand_dims(x, 0)
        C, T, V, M = 3, 50, 18, 2
        return x.transpose(3,2,0,1).reshape(M * V * C, T)

    filename = "msg3d.pb"
    create_graph(filename)
    # show_nodename()

    input_name = 'data_bn.num_batches_tracked:0'
    output_name = 'mul_1:0'

    C, T, V, M = 3, 50, 18, 2
    test_input = np.ones((C, T, V, M))
    test_input = array_init_reshape(test_input)
    print(test_input.shape)

    # test_input = test_input[0, :, 0]
    with tf.compat.v1.Session() as sess:
        input_node = sess.graph.get_tensor_by_name(input_name)
        output_node = sess.graph.get_tensor_by_name(output_name)
        print(input_node)
        # class_id = sess.run(output_node, {input_node: test_input})
        # print(np.argmax(class_id))
