# def dot_product(p1, p2):
#     return p1[0] * p2[0] + p1[1] * p2[1]
#
# a = (0, 0)
# b = (1, 0)
# c = (0, 1)
# p = (0.5, 0.6)
# ab = (b[0] - a[0], b[1] - a[1])
# ac = (c[0] - a[0], c[1] - a[1])
# ap = (p[0] - a[0], p[1] - a[1])
# dot00 = dot_product(ac, ac)
# dot01 = dot_product(ac, ab)
# dot02 = dot_product(ac, ap)
# dot11 = dot_product(ab, ab)
# dot12 = dot_product(ab, ap)
# inver_deno = 1 / (dot00 * dot11 - dot01 * dot01)
# u = (dot11 * dot02 - dot01 * dot12) * inver_deno
# v = (dot00 * dot12 - dot01 * dot02) * inver_deno
# if (u >= 0) and (v >= 0) and (u + v <= 1):
#     print('inside')
# else:
#     print('outside')

import generate_mesh
result_path = 'data\\result.pkl'
generate_mesh.convert(result_path)