import data_structure
import numpy as np
import math
import open3d as o3d
from scipy.sparse.linalg import eigsh


def load_data(ply_file_path):
    # load data
    # node data
    mesh = o3d.io.read_triangle_mesh(ply_file_path)
    lines = list(np.asarray(mesh.vertices))
    nodes = list()
    for index, line in enumerate(lines):
        node = data_structure.Node([item for item in line], index)
        nodes.append(node)

    # edge data
    edges = list()
    lines = list(np.asarray(mesh.triangles))
    for line in lines:
        indexes = [item for item in line]
        edges.append((indexes[0], indexes[1]))
        edges.append((indexes[0], indexes[2]))
        edges.append((indexes[1], indexes[2]))
        for i in range(len(indexes)):
            nodes[indexes[i]].add_connection(indexes[(i + 1) % 3], indexes[(i - 1) % 3])
            nodes[indexes[i]].add_connection(indexes[(i - 1) % 3], indexes[(i + 1) % 3])

    return nodes, edges


def get_Laplacian_matrix(nodes):


    #calculate all edges' lengths
    print('---------------calculating all edges lengths---------------')
    length = len(nodes)
    edge_lengths = dict()
    for index, node in enumerate(nodes):
        edge_lengths[index] = dict()
        for key in node.connection.keys():
            edge_lengths[index][key] = math.sqrt(math.pow(node.x - nodes[key].x, 2) +
                                                 math.pow(node.y - nodes[key].y, 2) +
                                                 math.pow(node.z - nodes[key].z, 2))

    # calculate all edges' weights
    print('---------------calculating all edges weights---------------')
    weight = dict()
    for index, node in enumerate(nodes):
        weight[index] = dict()
        for key, values in node.connection.items():
            cots = list()
            for value in values:
                a = edge_lengths[index][key]
                b = edge_lengths[index][value]
                c = edge_lengths[key][value]
                cos_angle = (math.pow(b, 2) + math.pow(c, 2) - math.pow(a, 2)) / (2 * b * c)
                angle = math.acos(cos_angle)
                cots.append(1/math.tan(angle))
            node.set_angle(key, cots)
            weight[index][key] = sum(cots) / len(cots) * -1

    # calculate Laplacian matrix
    print('---------------calculating Laplacian matrix---------------')

    L_dict = dict()
    for i in range(len(nodes)):
        L_dict[i] = dict()
        L_dict[i][i] = sum(weight[i].values())
        for key in nodes[i].connection.keys():
                L_dict[i][key] = -weight[i][key]

    L = np.zeros((length, length))
    for i, connections in L_dict.items():
        for j, value in connections.items():
            L[i][j] = value
    return L, edge_lengths


def get_eigenfield(L):
    print('---------------calculating eigenfield---------------')
    evals_small, evecs_small = eigsh(L, 50, which='SM', tol=1e-2)
    return evecs_small


def classify_points(nodes, f_value):
    for index, node in enumerate(nodes):
        if len(node.connection) == 0:
            node.set_category('regular')
            continue
        sequence = list()
        accessed = list()
        try:
            adj = list(node.connection.keys())[0]
        except IndexError:
            print(index)
        opp = node.connection[adj][0]
        while opp not in accessed:
            sequence.append(adj)
            accessed.append(adj)
            old = adj
            adj = opp
            for item in node.connection[adj]:
                if item != old:
                    opp = item
        sequence.append(adj)
        node.set_sequence(sequence)

        compare = f_value[index] > f_value[sequence[0]]
        changes = 0
        for item in sequence:
            if (f_value[index] > f_value[item]) != compare:
                changes += 1
                compare = f_value[index] > f_value[item]
        if changes == 0:
            if compare == True:
                node.set_category('maximum')
            else:
                node.set_category('minimum')
        elif changes <= 2:
            node.set_category('regular')
        else:
            node.set_category('saddle')


def find_maximum_neighbor(nodes, node, sequence, f_value, path_name):
    max = f_value[sequence[0]]
    max_index = 0
    for index, item in enumerate(sequence):
        if f_value[item] > max:
            max = f_value[item]
            max_index = index
    node.set_path(path_name, sequence[max_index])
    if nodes[sequence[max_index]].category == 'maximum':
        return
    find_maximum_neighbor(nodes, node, nodes[sequence[max_index]].sequence, f_value, path_name)


def find_minimun_neighbor(nodes, node, sequence, f_value, path_name):
    min = f_value[sequence[0]]
    min_index = 0
    for index, item in enumerate(sequence):
        if f_value[item] < min:
            min = f_value[item]
            min_index = index
    node.set_path(path_name, sequence[min_index])
    if nodes[sequence[min_index]].category == 'minimum':
        return
    find_minimun_neighbor(nodes, node, nodes[sequence[min_index]].sequence, f_value, path_name)


def extract_Morse_Smale_Complex(nodes, f_value):
    saddle_nodes = list()
    for index, node in enumerate(nodes):
        if node.category == 'saddle':
            saddle_nodes.append(node)
            compare = f_value[index] > f_value[node.sequence[0]]
            changes = list()
            for neighbor, item in enumerate(node.sequence):
                if (f_value[index] > f_value[item]) != compare:
                    compare = f_value[index] > f_value[item]
                    changes.append(neighbor)
            if len(changes) == 3:
                changes.insert(0, 0)

            if f_value[node.sequence[changes[0]]] > f_value[index]:
                find_maximum_neighbor(nodes, node, node.sequence[changes[0]: changes[1]], f_value, 'maximum1')
                find_maximum_neighbor(nodes, node, node.sequence[changes[2]: changes[3]], f_value, 'maximum2')
                find_minimun_neighbor(nodes, node, node.sequence[changes[1]: changes[2]], f_value, 'minimum1')
                find_minimun_neighbor(nodes, node, node.sequence[changes[3]:] + node.sequence[0: changes[0]],
                                      f_value, 'minimum2')
            else:
                find_maximum_neighbor(nodes, node, node.sequence[changes[1]: changes[2]], f_value, 'maximum1')
                find_maximum_neighbor(nodes, node, node.sequence[changes[3]:] + node.sequence[0: changes[0]],
                                      f_value, 'maximum2')
                find_minimun_neighbor(nodes, node, node.sequence[changes[0]: changes[1]], f_value, 'minimum1')
                find_minimun_neighbor(nodes, node, node.sequence[changes[2]: changes[3]], f_value, 'minimum2')
    return saddle_nodes
