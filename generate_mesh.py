import math
import pickle
import data_structure


# find two saddle nodes, one maximum point and one minimum point
# that constituted a patch
def get_pairs(saddle_nodes):
    pairs = list()
    for i in range(len(saddle_nodes)):
        node_i = saddle_nodes[i]
        for j in range(i+1, len(saddle_nodes)):
            node_j = saddle_nodes[j]
            node_i_max = [node_i.path['maximum1'][-1], node_i.path['maximum2'][-1]]
            node_i_min = [node_i.path['minimum1'][-1], node_i.path['minimum2'][-1]]
            node_j_max = [node_j.path['maximum1'][-1], node_j.path['maximum2'][-1]]
            node_j_min = [node_j.path['minimum1'][-1], node_j.path['minimum2'][-1]]
            inter_max = list(set(node_i_max).intersection(set(node_j_max)))
            inter_min = list(set(node_i_min).intersection(set(node_j_min)))
            if inter_max and inter_min:
                for max_end in inter_max:
                    for min_end in inter_min:
                        pairs.append([node_i, node_j, max_end, min_end])
    return pairs


# find all points inside a patch
def traverse_inside_point(index, nodes, insides, boundary, other_boundary):
    stack = list()
    centers = list()
    stack.append(index)
    i = index
    sequence = list()
    # counter = 0
    while stack:
        if i in other_boundary:
            return False
        node = nodes[i]
        sequence.append(node)
        if i not in insides:
            insides.append(i)
        if i not in centers:
            centers.append(i)
        for key in node.connection.keys():
            if key not in boundary and key not in insides:
                insides.append(key)
        for key in node.connection.keys():
            if key not in boundary and key not in centers and key not in stack:
                stack.append(key)
        i = stack.pop()
    return True
        # counter += 1
        # print(len(stack) + counter)
        # if counter > 280:
        #     sequence = data_structure.Line(sequence)
        #     return sequence


# find all patches
def get_complex_patches(nodes, saddle_nodes, f_value):
    pairs = get_pairs(saddle_nodes)
    patches = list()
    counter = 0
    for node1, node2, max_end, min_end in pairs:
        boundary = list()
        other_bounaries = list()
        node1_extrema = list()
        node2_extrema = list()
        for key, value in node1.path.items():
            if value[-1] == max_end or value[-1] == min_end:
                node1_extrema.append(key)
                boundary.extend(value)
        for key, value in node2.path.items():
            if value[-1] == max_end or value[-1] == min_end:
                node2_extrema.append(key)
                boundary.extend(value)
        boundary.append(node1.index)
        boundary.append(node2.index)
        for node in saddle_nodes:
            if node.index != node1.index and node.index != node2.index:
                for path in node.path.values():
                    other_bounaries.extend(path)
                other_bounaries.append(node.index)
        node1_other_extrema = list(set(node1.path.keys()) - set(node1_extrema))
        node2_other_extrema = list(set(node2.path.keys()) - set(node2_extrema))
        for item in node1_other_extrema:
            other_bounaries.extend(node1.path[item])
        for item in node2_other_extrema:
            other_bounaries.extend(node2.path[item])

        if node1.path[node1_extrema[0]][0] in nodes[node1.path[node1_extrema[1]][0]].connection.keys():
            if node1.index != nodes[node1.path[node1_extrema[1]][0]].connection[node1.path[node1_extrema[0]][0]][0]:
                inside_point = nodes[node1.path[node1_extrema[1]][0]].connection[node1.path[node1_extrema[0]][0]][0]
            else:
                inside_point = nodes[node1.path[node1_extrema[1]][0]].connection[node1.path[node1_extrema[0]][0]][1]
        else:
            start_index = node1.path[node1_extrema[0]][0]
            key = start_index
            end_index = node1.path[node1_extrema[1]][0]
            oppo = node1.connection[start_index][0]
            compare = f_value[node1.index] > f_value[key]
            changes = 0
            appeared = [node1.index, key, oppo]
            while oppo != end_index:
                key = oppo
                i = 0 if node1.connection[key][0] not in appeared else 1
                oppo = node1.connection[key][i]
                appeared.append(oppo)
                if compare != (f_value[node1.index] > f_value[key]):
                    compare = f_value[node1.index] > f_value[key]
                    changes += 1
            if changes > 1:
                inside_point = node1.connection[start_index][1]
            else:
                inside_point = node1.connection[start_index][0]

        insides = list()
        res = traverse_inside_point(inside_point, nodes, insides, boundary, other_bounaries)
        if not res:
            continue
        # traverse_inside_point(inside_point, nodes, insides, boundary)
        # sequence = traverse_inside_point(inside_point, nodes, insides, boundary, other_bounaries)
        # ver_nodes = data_structure.Line((nodes[node1.path[node1_extrema[0]][-1]],
        #                                  nodes[node1.path[node1_extrema[1]][-1]],
        #                                  node1,
        #                                  nodes[inside_point],
        #                                  node1,
        #                                  nodes[node1.path[node1_extrema[0]][-1]],
        #                                  node2,
        #                                  nodes[node1.path[node1_extrema[1]][-1]]))
        # with open('data\\traverse_sequence.pkl', 'wb') as f:
        #     pickle.dump((ver_nodes, sequence), f)
        # the data in boundary and insides is index of node
        patches.append((node1, node2, max_end, min_end, boundary, insides))
        counter += 1
        print(str(counter) + 'th patch obtained')
    return patches


# calculate the weight when doing the harmonic map
def calc_weight(patch_nodes, nodes):
    weight = dict()
    for index in patch_nodes:
        node = nodes[index]
        weight[node.index] = dict()
        for key, angles in node.angle.items():
            weight[node.index][key] = sum(angles)
    return weight


# calculate the distance between two points
def calc_length(nodes, index1, index2):
    node1 = nodes[index1]
    node2 = nodes[index2]
    return math.sqrt(pow((node1.x - node2.x), 2) +
                     pow((node1.y - node2.y), 2) +
                     pow((node1.z - node2.z), 2))


# map the boundary of a comples to a unit square
def map_boundary(nodes, node1, node2, max_end, min_end):

    node1_extrema = [0, 0]
    node2_extrema = [0, 0]
    # extrema[0] stands for maximum1/2
    # extrema[1] stands for minimum1/2
    sequences = list()

    for key, value in node1.path.items():
        if value[-1] == max_end:
            node1_extrema[0] = key
        elif value[-1] == min_end:
            node1_extrema[1] = key

    for key, value in node2.path.items():
        if value[-1] == max_end:
            node2_extrema[0] = key
        elif value[-1] == min_end:
            node2_extrema[1] = key
    sequences.append([node1.index] + node1.path[node1_extrema[0]])
    sequences.append(node2.path[node2_extrema[0]][::-1] + [node2.index])
    sequences.append([node2.index] + node2.path[node2_extrema[1]])
    sequences.append([node1.index] + node1.path[node1_extrema[1]])
    node1.set_map_point((0, 0))
    node2.set_map_point((1, 1))

    path = sequences[0]
    s = list()
    s.insert(0, calc_length(nodes, path[0], path[1]))
    for i in range(1, len(path) - 1):
        s.append(s[i - 1] + calc_length(nodes, path[i], path[i + 1]))
    for i in range(1, len(path)):
        nodes[path[i]].set_map_point((0, s[i - 1]/s[-1]))

    path = sequences[1]
    s = list()
    s.insert(0, calc_length(nodes, path[0], path[1]))
    for i in range(1, len(path) - 1):
        s.append(s[i - 1] + calc_length(nodes, path[i], path[i + 1]))
    for i in range(1, len(path)):
        nodes[path[i]].set_map_point((s[i - 1]/s[-1], 1))

    path = sequences[2]
    s = list()
    s.insert(0, calc_length(nodes, path[0], path[1]))
    for i in range(1, len(path) - 1):
        s.append(s[i - 1] + calc_length(nodes, path[i], path[i + 1]))
    for i in range(1, len(path)):
        nodes[path[i]].set_map_point((1, 1 - s[i - 1]/s[-1]))

    path = sequences[3]
    s = list()
    s.insert(0, calc_length(nodes, path[0], path[1]))
    for i in range(1, len(path) - 1):
        s.append(s[i - 1] + calc_length(nodes, path[i], path[i + 1]))
    for i in range(1, len(path) - 1):
        nodes[path[i]].set_map_point((s[i - 1] / s[-1], 0))


def calc_harmonic_energy(nodes, edges, weight):
    E_f = 0
    for edge in edges:
        E_f += weight[edge[0]][edge[1]] * \
               pow(nodes[edge[0]].map_point[0] - nodes[edge[1]].map_point[0], 2) +\
               pow(nodes[edge[0]].map_point[1] - nodes[edge[1]].map_point[1], 2)
    return E_f


def map_to_quadrilateral(nodes, patch, map_threshold):
    # the data in boundary and insides is index of node
    node1, node2, max_end, min_end, boundary, insides = patch
    patch_nodes = boundary + insides
    map_boundary(nodes, node1, node2, max_end, min_end)
    edges = list()
    for i in patch_nodes:
        node = nodes[i]
        for key in node.connection.keys():
            if (node.index, key) not in edges:
                edges.append((node.index, key))

    weight = calc_weight(patch_nodes, nodes)
    E0 = calc_harmonic_energy(nodes, edges, weight)
    while True:
        for index in insides:
            node = nodes[index]
            weight_sum = 0
            point = [0] * 2
            for neighbor in node.connection.keys():
                weight_sum += weight[node.index][neighbor]
                point[0] += (nodes[neighbor].map_point[0] * weight[node.index][neighbor])
                point[1] += (nodes[neighbor].map_point[1] * weight[node.index][neighbor])
            point[0] /= weight_sum
            point[1] /= weight_sum
            node.set_map_point((point[0], point[1]))
        E1 = calc_harmonic_energy(nodes, edges, weight)
        error = math.fabs(E1 - E0)
        E0 = E1
        if error > map_threshold:
            break

def map_to_complex():
    pass