import numpy as np


def edge2mat(link, num_node):
    A = np.zeros((num_node, num_node))
    for i, j in link:
        A[j, i] = 1
    return A


def normalize_digraph(A):
    Dl = np.sum(A, 0)
    h, w = A.shape
    Dn = np.zeros((w, w))
    for i in range(w):
        if Dl[i] > 0:
            Dn[i, i] = Dl[i] ** (-1)
    AD = np.dot(A, Dn)
    return AD


def get_spatial_graph(num_node, self_link, inward, outward):
    I = edge2mat(self_link, num_node)
    In = normalize_digraph(edge2mat(inward, num_node))
    Out = normalize_digraph(edge2mat(outward, num_node))
    A = np.stack((I, In, Out))
    return A


def k_adjacency(A, k, with_self=False, self_factor=1):
    assert isinstance(A, np.ndarray)
    I = np.eye(len(A), dtype=A.dtype)
    if k == 0:
        return I
    Ak = np.minimum(np.linalg.matrix_power(A + I, k), 1) \
        - np.minimum(np.linalg.matrix_power(A + I, k - 1),
                     1)  # element-wise minima.
    # 没明白 为什么是k次方 还有个相减？
    if with_self:
        Ak += (self_factor * I)
    return Ak


def normalize_adjacency_matrix(A):
    node_degrees = A.sum(-1)  # 每列相加 i.e. A[1,1]+A[1,2]+A[1,3]
    degs_inv_sqrt = np.power(node_degrees, -0.5)
    norm_degs_matrix = np.eye(len(node_degrees)) * degs_inv_sqrt
    return (norm_degs_matrix @ A @ norm_degs_matrix).astype(np.float32)


# A = np.random.random((3, 3))
# print(A, '\n\n', A.sum(-1))


def get_adjacency_matrix(edges, num_nodes):
    A = np.zeros((num_nodes, num_nodes), dtype=np.float32)
    for edge in edges:
        A[edge] = 1.
    return A


# num_nodes = 3
# edges = ((0, 1), (1, 2))
# for edge in edges:
#     print(edge)
# print(get_adjacency_matrix(edges, num_nodes))
