class Node:
    def __init__(self, coordinates):
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.z = coordinates[2]
        self.connection = dict()
        self.path = dict()


    def add_connection(self, index, opposite):
        if index not in self.connection.keys():
            self.connection[index] = list()
        self.connection[index].append(opposite)


    def get_num_of_neibors(self):
        return len(self.connection)


    def set_type(self, type):
        self.type = type


    def set_sequence(self, sequence):
        self.sequence = sequence

    def set_path(self, path_name, step):
        if path_name not in self.path.keys():
            self.path[path_name] = list()
        self.path[path_name].append(step)