import pickle
import open3d as o3d
import matplotlib.pyplot as plt
import numpy as np
import plotly.plotly as py
import plotly.graph_objs as go
import ipyvolume as ipv

with open('evecs.pkl', 'rb') as f:
    data = pickle.load(f)
value = data[:, 0]
mesh = o3d.io.read_triangle_mesh('data/bun_zipper.ply')
lines = list(np.asarray(mesh.vertices))

xs = list()
ys = list()
zs = list()
cs = list()
for index, line in enumerate(lines):
    xs.append(line[0])
    ys.append(line[1])
    zs.append(line[2])
    cs.append(value[index]*100)

cs = [[item, item, item] for item in cs]
lines = [list(item) for item in np.asarray(mesh.triangles)]

x = np.linspace(-0.2, 0.2, 100)
y = np.linspace(-0.2, 0.2, 100)
z = np.linspace(-0.2, 0.2, 100)
line = ipv.plot(x, y, z, color='green')

ipv.plot_trisurf(xs, ys, zs, triangles=lines)
ipv.pylab.xlim(-0.2, 0.2)
ipv.pylab.ylim(-0.2, 0.2)
ipv.pylab.zlim(-0.2, 0.2)
ipv.show()