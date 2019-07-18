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


# find all patches
def get_complex_patches(nodes, saddle_nodes, f_value):
    pairs = get_pairs(saddle_nodes)
    patches = list()
    counter = 0
    for node1, node2, max_end, min_end in pairs:
        # if node1.index == 6165 or node2.index == 6165:
        #     print(node1.path, node2.path)
        boundary = list()
        other_bounaries = list()
        node1_extrema = list()
        node2_extrema = list()
        for key, value in node1.path.items():
            if value[-1] == max_end or value[-1] == min_end:
                node1_extrema.append(key)
                # boundary.extend(value)
        for key, value in node2.path.items():
            if value[-1] == max_end or value[-1] == min_end:
                node2_extrema.append(key)
                # boundary.extend(value)
        if set(node1.path[node1_extrema[0]][:-1]) & set(node2.path[node2_extrema[0]][:-1]):
            for j in range(len(node1.path[node1_extrema[0]][:-1])):
                if node1.path[node1_extrema[0]][j] in node2.path[node2_extrema[0]]:
                    max_end = node1.path[node1_extrema[0]][j]
                    break
        if set(node1.path[node1_extrema[1]][:-1]) & set(node2.path[node2_extrema[1]][:-1]):
            for j in range(len(node1.path[node1_extrema[1]][:-1])):
                if node1.path[node1_extrema[1]][j] in node2.path[node2_extrema[1]]:
                    min_end = node1.path[node1_extrema[1]][j]
                    break
        try:
            boundary.extend(node1.path[node1_extrema[0]][:node1.path[node1_extrema[0]].index(max_end) + 1])
            boundary.extend(node1.path[node1_extrema[1]][:node1.path[node1_extrema[1]].index(min_end) + 1])
            boundary.extend(node2.path[node2_extrema[0]][:node2.path[node2_extrema[0]].index(max_end) + 1])
            boundary.extend(node2.path[node2_extrema[1]][:node2.path[node2_extrema[1]].index(min_end) + 1])
        except ValueError:
            print(node1_extrema, node2_extrema, node1.index, node2.index)
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
        triangles = list()
        all_nodes = boundary + insides
        for node_index in all_nodes:
            for key, values in nodes[node_index].connection.items():
                for oppo in values:
                    if key in all_nodes and oppo in all_nodes and {node_index, key, oppo} not in triangles:
                        ver_in_triangle = {node_index, key, oppo} & {node1, node2, node1.path[node1_extrema[0]][-1], node1.path[node1_extrema[1]][-1]}
                        rest = {node_index, key, oppo} - {node1, node2, node1.path[node1_extrema[0]][-1], node1.path[node1_extrema[1]][-1]}
                        if ((node_index not in boundary or key not in boundary or oppo not in boundary) or
                                len(rest) < 2 or
                                (ver_in_triangle and
                                 len(rest & set(node1.path[node1_extrema[0]])) < 2 and
                                 len(rest & set(node1.path[node1_extrema[1]])) < 2 and
                                 len(rest & set(node2.path[node2_extrema[0]])) < 2 and
                                 len(rest & set(node2.path[node1_extrema[1]])) < 2 )):
                            triangle = {node_index, key, oppo}
                            triangles.append(triangle)
        patches.append((node1, node2, max_end, min_end, boundary, insides, triangles))
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
        if max_end in value:
            node1_extrema[0] = key
        elif min_end in value:
            node1_extrema[1] = key

    for key, value in node2.path.items():
        if max_end in value:
            node2_extrema[0] = key
        elif min_end in value:
            node2_extrema[1] = key
    sequences.append([node1.index] + node1.path[node1_extrema[0]][: node1.path[node1_extrema[0]].index(max_end) + 1])
    sequences.append(node2.path[node2_extrema[0]][: node2.path[node2_extrema[0]].index(max_end) + 1][::-1] + [node2.index])
    sequences.append([node2.index] + node2.path[node2_extrema[1]][: node2.path[node2_extrema[1]].index(min_end) + 1])
    sequences.append([node1.index] + node1.path[node1_extrema[1]][: node1.path[node1_extrema[1]].index(min_end) + 1])
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
    node1, node2, max_end, min_end, boundary, insides, triangles = patch
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


def triangle_area(a, b, c):
    ab = (b[0] - a[0], b[1] - a[1])
    bc = (c[0] - b[0], c[1] - b[1])
    return abs((ab[0] * bc[1] - ab[1] * bc[0]) / 2)


def is_in_triangle(nodes, triangle, p):
    a, b, c = triangle
    a = nodes[a].map_point
    b = nodes[b].map_point
    c = nodes[c].map_point
    abc = triangle_area(a, b, c)
    abp = triangle_area(a, b, p)
    acp = triangle_area(a, c, p)
    bcp = triangle_area(b, c, p)
    sum_other = abp + acp + bcp
    return abs((abc / sum_other) - 1) <= 0.001


def calc_point_coor(nodes, triangle, mesh_point):
    a, b, c = triangle
    a = nodes[a].map_point
    b = nodes[b].map_point
    c = nodes[c].map_point
    s_abc = triangle_area(a, b, c)
    s_pbc = triangle_area(mesh_point, b, c)
    s_pab = triangle_area(mesh_point, a, b)
    s_pac = triangle_area(mesh_point, a, c)
    if s_abc == 0:
        return False, 0, 0, 0
    is_in_triangle(nodes, triangle, mesh_point)
    return True, s_pbc / s_abc, s_pac / s_abc, s_pab / s_abc


def construct_grid(d):
    mesh_point = list()
    for i in [item / d for item in range(d+1)]:
        for j in [item / d for item in range(d+1)]:
            mesh_point.append((i, j))
    mesh_quad_index = list()
    for i in range(d):
        for j in range(d):
            mesh_quad_index.append((i * (d + 1) + j,
                                    (i + 1) * (d + 1) + j,
                                    (i + 1) * (d + 1) + j + 1,
                                    i * (d + 1) + j + 1))
            # mesh_quad_index.append((j * d + i, (j + 1) * d + i, (j + 1) * d + i + 1, j * d + i + 1))
    return mesh_point, mesh_quad_index


def map_to_complex_boundary(nodes, sequence, path):
    map_point = dict()
    map_point[sequence[0]] = (nodes[path[0]].x, nodes[path[0]].y, nodes[path[0]].z)
    s = list()
    s.insert(0, calc_length(nodes, path[0], path[1]))
    for i in range(1, len(path) - 1):
        s.append(s[i - 1] + calc_length(nodes, path[i], path[i + 1]))
    for i in range(1, len(sequence)):
        for j in range(len(s)):
            if s[j] / s[-1] > (i / len(sequence)):
                length = calc_length(nodes, path[j], path[j + 1])
                a = s[-1] * i / len(sequence)
                if j > 0:
                    a -= s[j - 1]
                lam = a / length
                map_point[sequence[i]] = (nodes[path[j]].x * (1 - lam) + nodes[path[j + 1]].x * lam,
                                          nodes[path[j]].y * (1 - lam) + nodes[path[j + 1]].y * lam,
                                          nodes[path[j]].z * (1 - lam) + nodes[path[j + 1]].z * lam)
                break
    return map_point


def map_to_complex(nodes, patch, d):
    quad_mesh, mesh_quad_index = construct_grid(d)
    node1, node2, max_end, min_end, boundary, insides, triangles = patch
    point_triangle_dict = dict()
    # find mesh point's corresponding triangle and its coordinate

    for index, mesh_point in enumerate(quad_mesh):
        for triangle in triangles:
            if (mesh_point[0] != 0 and mesh_point[1] != 0 and mesh_point[0] != 1 and mesh_point[1] != 1) and \
                    is_in_triangle(nodes, triangle, mesh_point):
                res, p1, p2, p3 = calc_point_coor(nodes, triangle, mesh_point)
                if not res:
                    continue
                point_triangle_dict[index] = (triangle, p1, p2, p3)

    mesh_points_3d = dict()
    for index, value in point_triangle_dict.items():
        triangle, p1, p2, p3 = value
        triangle = list(triangle)
        point_3d_x = nodes[triangle[0]].x * p1 + nodes[triangle[1]].x * p2 + nodes[triangle[2]].x * p3
        point_3d_y = nodes[triangle[0]].y * p1 + nodes[triangle[1]].y * p2 + nodes[triangle[2]].y * p3
        point_3d_z = nodes[triangle[0]].z * p1 + nodes[triangle[1]].z * p2 + nodes[triangle[2]].z * p3
        mesh_points_3d[index] = (point_3d_x, point_3d_y, point_3d_z)

    # map quad mesh's boundaries to complex's boundaries
    sequence = list()
    for i in range(4):
        sequence.append(list())
    for i in range(d, -1, -1):
        sequence[0].append(i)
    for i in range(d * (d + 1), -1, -d - 1):
        sequence[1].append(i)
    for i in range(d * (d + 1), (d + 1) * (d + 1)):
        sequence[2].append(i)
    for i in range(d, d ** 2 + 2 * d + 1, d + 1):
        sequence[3].append(i)
    node1_extrema = [0, 0]
    node2_extrema = [0, 0]
    for key, path in node1.path.items():
        if max_end in path:
            node1_extrema[0] = key
        if min_end in path:
            node1_extrema[1] = key
    for key, path in node2.path.items():
        if max_end in path:
            node2_extrema[0] = key
        if min_end in path:
            node2_extrema[1] = key
    mesh_points_3d.update(map_to_complex_boundary(nodes, sequence[0], [node1.index] + node1.path[node1_extrema[0]][: node1.path[node1_extrema[0]].index(max_end) + 1]))
    mesh_points_3d.update(map_to_complex_boundary(nodes, sequence[1], [node2.index] + node2.path[node2_extrema[0]][: node2.path[node2_extrema[0]].index(max_end) + 1]))
    mesh_points_3d.update(map_to_complex_boundary(nodes, sequence[2], [node2.index] + node2.path[node2_extrema[1]][: node2.path[node2_extrema[1]].index(min_end) + 1]))
    mesh_points_3d.update(map_to_complex_boundary(nodes, sequence[3], [node1.index] + node1.path[node1_extrema[1]][: node1.path[node1_extrema[1]].index(min_end) + 1]))
    print(len(mesh_points_3d))
    return mesh_points_3d, mesh_quad_index
