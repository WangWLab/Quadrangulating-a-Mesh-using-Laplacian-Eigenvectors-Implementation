import Quadrangular_Base_Complex
import pickle


if __name__ == '__main__':
    node_file_path = 'data/teapot_nodes.txt'
    face_file_path = 'data/teapot_elements.txt'
    ply_file_path = 'data/bun_zipper.ply'
    nodes = Quadrangular_Base_Complex.load_data(ply_file_path)
    # L_matrix= Quadrangular_Base_Complex.get_Laplacian_matrix(nodes)
    # enginfield = Quadrangular_Base_Complex.get_eigenfield(L_matrix)
    # with open('evecs.pkl', 'wb') as f:
    #     pickle.dump(enginfield, f)
    with open('evecs.pkl', 'rb') as f:
        enginfield = pickle.load(f)
    Quadrangular_Base_Complex.classify_points(nodes, enginfield[:, 49])
    # sad_count = 0
    # max_count = 0
    # min_count = 0
    # for node in nodes:
    #     if node.type == 'saddle':
    #         sad_count += 1
    #     elif node.type == 'maximum':
    #         max_count += 1
    #     elif node.type == 'minimum':
    #         min_count += 1
    # print('saddle', sad_count, 'maximum', max_count, 'minimum', min_count)
    saddle_nodes = Quadrangular_Base_Complex.extract_Morse_Smale_Complex(nodes, enginfield[:, 49])

