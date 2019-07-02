import pickle
import open3d as o3d
import matplotlib.pyplot as plt
import numpy as np
import plotly.plotly as py
import plotly.graph_objs as go

with open('evecs.pkl', 'rb') as f:
    data = pickle.load(f)
value = data[:, 0]
mesh = o3d.io.read_triangle_mesh('data/bun_zipper.ply')
mesh.compute_vertex_normals()
o3d.visualization.draw_geometries([mesh])
# lines = list(np.asarray(mesh.vertices))
#
# xs = list()
# ys = list()
# zs = list()
# cs = list()
# for index, line in enumerate(lines):
#     xs.append(line[0])
#     ys.append(line[1])
#     zs.append(line[2])
#     cs.append(value[index]*100)