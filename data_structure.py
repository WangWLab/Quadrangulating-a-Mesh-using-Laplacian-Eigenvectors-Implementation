class Node:
    def __init__(self, coordinates, index):
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.z = coordinates[2]
        # cancle之后设置valie为False
        self.valid = True
        # 在node列表中的索引位置
        self.index = index
        # 相邻结点，key是相邻结点的坐标，value是该node和key的连线所对的两个或一个结点
        self.connection = dict()
        # 如果是鞍点，从该node出发到极值点经过的结点索引
        self.path = dict()
        # 鞍点，常规点，极大极小值点
        self.category = ''
        # sequence是遍历结点相邻结点的顺序
        self.sequence = None
        # angle记录结点和相邻结点组成的边的对角角度
        self.angle = dict()
        # extrema记录结点连接的极值点的索引
        self.extrema = list()
        # map_point记录map到单位正方形之后的坐标
        self.map_point = (0, 0)

    def add_connection(self, index, opposite):
        if index not in self.connection.keys():
            self.connection[index] = list()
        self.connection[index].append(opposite)

    def set_angle(self, key, angle):
        self.angle[key] = angle

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

    def set_extrema(self):
        for value in self.path.values():
            self.extrema.append(value[-1])

    def set_map_point(self, coordinate):
        self.map_point = coordinate

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