import Quadrangular_Base_Complex
import Optimization
import pickle
import visualization

if __name__ == '__main__':
    node_file_path = 'data/teapot_nodes.txt'
    face_file_path = 'data/teapot_elements.txt'
    ply_file_path = 'data/bun_zipper.ply'
    nodes = Quadrangular_Base_Complex.load_data(ply_file_path)
    # L_matrix, edge_lengths = Quadrangular_Base_Complex.get_Laplacian_matrix(nodes)
    # enginfield = Quadrangular_Base_Complex.get_eigenfield(L_matrix)
    # with open('evecs.pkl', 'wb') as f:
    #     pickle.dump(enginfield, f)
    with open('evecs.pkl', 'rb') as f:
        enginfield = pickle.load(f)
    f_value = enginfield[:, 48]
    Quadrangular_Base_Complex.classify_points(nodes, f_value)
    # s_count = 0
    # i_count = 0
    # a_count = 0
    # for node in nodes:
    #     if node.category == 'saddle':
    #         s_count += 1
    #     elif node.category == 'maximum':
    #         a_count += 1
    #     elif node.category == 'minimum':
    #         i_count += 1
    # print(s_count, i_count, a_count)
    saddle_nodes = Quadrangular_Base_Complex.extract_Morse_Smale_Complex(nodes, f_value)
    Optimization.cancellation(saddle_nodes, nodes, f_value)
    iteration = 5
    coe = 0.1
    Optimization.straighten_path(saddle_nodes, nodes, iteration, coe)
    # visualization.generate_lines(saddle_nodes, nodes)


