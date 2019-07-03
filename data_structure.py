class Node:
    def __init__(self, coordinates, index):
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.z = coordinates[2]
        self.valid = True
        self.index = index
        self.connection = dict()
        self.path = dict()
        self.category = ''
        self.sequence = None

    def add_connection(self, index, opposite):
        if index not in self.connection.keys():
            self.connection[index] = list()
        self.connection[index].append(opposite)

    def get_num_of_neighbors(self):
        return len(self.connection)

    def set_category(self, category):
        self.category = category

    def set_sequence(self, sequence):
        self.sequence = sequence

    def set_path(self, path_name, step):
        if path_name not in self.path.keys():
            self.path[path_name] = list()
        self.path[path_name].append(step)

    def cancel(self):
        self.valid = False
        self.category = 'regular'

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def set_z(self, z):
        self.z = z


class Line:
    def __init__(self, nodes):
        def extract_position(nodes):
            x = list()
            y = list()
            z = list()
            for node in nodes:
                x.append(node.x)
                y.append(node.y)
                z.append(node.z)
            return x, y, z
        self.x, self.y, self.z = extract_position(nodes)