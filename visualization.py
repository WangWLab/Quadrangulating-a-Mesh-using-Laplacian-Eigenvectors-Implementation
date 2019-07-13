from data_structure import Line
import pickle


def generate_lines(saddle_nodes, nodes):
    lines = list()
    for node in saddle_nodes:
        for path in node.path.values():
            nodes_for_line = [nodes[item] for item in path]
            nodes_for_line.insert(0, nodes[node.index])
            line = Line(nodes_for_line)
            lines.append(line)

    with open('data\\lines.pkl', 'wb') as f:
        pickle.dump(lines, f)