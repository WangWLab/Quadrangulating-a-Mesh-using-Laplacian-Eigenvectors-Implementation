import copy


def sort_persistence(saddle_nodes, f_value):
    persistence = dict()
    for node in saddle_nodes:
        for path_name, path in node.path.items():
            persistence[str(node.index) + '-' + path_name] = abs(f_value[node.index] - f_value[path[-1]])
    return sorted(persistence.items(), key=lambda d: d[1], reverse=False)


def cancellation(saddle_nodes, nodes, f_value):
    print('---------------executing cancellation---------------')
    persistence = sort_persistence(saddle_nodes, f_value)
    for item in persistence[:int(len(persistence)*0.4)]:
        index, path_name = item[0].split('-')
        index = int(index)
        if nodes[index] in saddle_nodes:
            extrema = path_name[:len(path_name)-1]
            if nodes[index].path[extrema+'1'][-1] != nodes[index].path[extrema+'2'][-1]:
                opposite_path = extrema + ('1' if path_name[-1] == '2' else '2')
                low_p_index = nodes[index].path[path_name][-1]
                high_p_index = nodes[index].path[opposite_path][-1]
                if (extrema == 'maximum' and f_value[low_p_index] < f_value[high_p_index]) or \
                        (extrema == 'minimum' and f_value[low_p_index] > f_value[high_p_index]):
                    saddle_nodes.remove(nodes[index])
                    nodes[index].path[path_name].reverse()
                    nodes[index].cancel()
                    for node in saddle_nodes:
                        for node_path_name, path in node.path.items():
                            if path[-1] == low_p_index:
                                node.path[node_path_name].extend(nodes[index].path[path_name])
                                node.path[node_path_name].append(nodes[index].index)
                                node.path[node_path_name].extend(nodes[index].path[opposite_path])
    # TODO cancle saddle nodes whose two extrema path end at the same extrema point
    extrema = ['maximum', 'minimum']
    for node in saddle_nodes:
        if node.path[extrema[0]+'1'][-1] == node.path[extrema[0]+'2'][-1] or node.path[extrema[1]+'1'][-1] == node.path[extrema[1]+'2'][-1]:
            saddle_nodes.remove(node)


def merge_nearby_saddle(nodes, edge_lengths):
    S = list()
    P = list()
    for i in range(len(nodes)):
        S.append(list())
        P.append(list())
        for j in range(len(nodes)):
            S[i].append(float('inf'))
            P[i].append(0)
    for edge_start, item in edge_lengths.items():
        for edge_end, length in item.items():
            S[edge_start][edge_end] = length
            S[edge_end][edge_start] = length
    for i in range(len(P)):
        for j in range(len(P[0])):
            P[i][j] = j

    for k in range(len(nodes)):
        for i in range(len(S)):
            for j in range(len(S[0])):
                if S[i][j] > S[i][k] + S[k][j]:
                    S[i][j] = S[i][k] + S[k][j]
                    P[i][j] = P[i][k]
    return P
# TODO find the threshold to merge two nearby nodes


def compute_new_position(node, nodes, coe):
    xs = 0
    ys = 0
    zs = 0
    count = 0
    for neighbor in node.connection.keys():
        tmp = nodes[neighbor]
        xs += tmp.x
        ys += tmp.y
        zs += tmp.z
        count += 1
    xs /= count
    ys /= count
    zs /= count
    return node.x + (xs - node.x) * coe, node.y + (ys - node.y) * coe, node.z + (zs - node.z) * coe


def straighten_path(saddle_nodes, nodes, iteration, coe):
    print('---------------straighten path---------------')
    for i in range(iteration):
        new_nodes = copy.deepcopy(nodes)
        for node in saddle_nodes:
            for path_name, path in node.path.items():
                for step in path:
                    x, y, z = compute_new_position(nodes[step], nodes, coe)
                    new_nodes[step].set_x(x)
                    new_nodes[step].set_y(y)
                    new_nodes[step].set_z(z)
        nodes = new_nodes

