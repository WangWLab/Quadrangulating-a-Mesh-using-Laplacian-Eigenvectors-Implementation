import Quadrangular_Base_Complex
import Optimization
import pickle
import visualization
import generate_mesh
import time
import data_structure

if __name__ == '__main__':
    # ply_file_path = 'data\\bun_zipper.ply'
    # nodes, edges = Quadrangular_Base_Complex.load_data(ply_file_path)
    # L_matrix, edge_lengths = Quadrangular_Base_Complex.get_Laplacian_matrix(nodes)
    #
    # enginfield = Quadrangular_Base_Complex.get_eigenfield(L_matrix)
    # with open('data\\evecs.pkl', 'wb') as f:
    #     pickle.dump(enginfield, f)
    #
    # with open('data\\evecs.pkl', 'rb') as f:
    #     enginfield = pickle.load(f)
    # f_value = enginfield[:, 48]
    # Quadrangular_Base_Complex.classify_points(nodes, f_value)
    #
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
    #
    # saddle_nodes = Quadrangular_Base_Complex.extract_Morse_Smale_Complex(nodes, f_value)
    # Optimization.cancellation(saddle_nodes, nodes, f_value)
    # iteration = 5
    # coe = 0.1
    # Optimization.straighten_path(saddle_nodes, nodes, iteration, coe)
    # for node in saddle_nodes:
    #     node.set_extrema()
    # with open('data\\data.pkl', 'wb') as f:
    #     data = [nodes, edges, edge_lengths, f_value, saddle_nodes]
    #     pickle.dump(data, f)
    #
    # with open('data\\data.pkl', 'rb') as f:
    #     nodes, edges, edge_lengths, f_value, saddle_nodes = pickle.load(f)
    #
    # visualization.generate_lines(saddle_nodes, nodes)
    # patches = generate_mesh.get_complex_patches(nodes, saddle_nodes, f_value)
    # with open('data\\patch.pkl', 'wb') as f:
    #     pickle.dump(patches, f)
    #
    # with open('data\\patch.pkl', 'rb') as f:
    #     patches = pickle.load(f)
    # map_threshold = 1E-3
    # c = 0
    # for patch in patches:
    #     generate_mesh.map_to_quadrilateral(nodes, patch, map_threshold)
    #     c += 1
    #     print(str(c) + 'th patch mapped')
    # with open('data\\data.pkl', 'wb') as f:
    #     pickle.dump((nodes, edges, edge_lengths, f_value, saddle_nodes, patches), f)
    with open('data\\data.pkl', 'rb') as f:
        nodes, edges, edge_lengths, f_value, saddle_nodes, patches = pickle.load(f)
