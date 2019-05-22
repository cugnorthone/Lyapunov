import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import random
from sense_eaa import EAA
import numpy as np
from thermo_diagram import ThermoMap
import seaborn as sns

def drawMaxNet(r_p):
  node0 = (1, 2)
  node1 = (2, 1)
  node2 = (2, 3)
  node3 = (3, 3)
  node4 = (3, 4)

  node5 = (6, 1)
  node6 = (5, 2.5)
  node7 = (7, 3.9)
  node8 = (5, 4)
  node9 = (8, 6)
  node10 = (7, 8)
  node11 = (6.5, 7)
  node12 = (5, 5)

  node13 = (4.5, 9.5)
  node14 = (3.5, 10)
  node15 = (2, 9)
  node16 = (3.8, 8)

  node17 = (2.5, 7)

  node18 = (4, 6)

  node_list = [node0, node1, node2, node3, node4, node5, node6,
               node7, node8, node9, node10, node11, node12, node13,
               node14, node15, node16, node17, node18]
  print(node_list)
  r = 0.3
  plt.figure(figsize=(5, 5))

  connect_list = [(0, 2), (1, 2), (2, 4), (3, 4), (4, 18),
                  (5, 6), (6, 8), (7, 8), (8, 12), (9, 11),
                  (10, 11), (11, 12), (12, 18), (13, 16),
                  (14, 16), (15, 16), (16, 18), (17, 18)]

  circle_list = []
  for node in node_list[:-1]:
    circle_list.append(plt.Circle((node[0], node[1]), r, color='y',
                                  fill=True, alpha=r_p[node_list.index(node)]))

  circle_list.append(plt.Circle((node_list[-1][0], node_list[-1][1]),
                                r, color='r', fill=True))

  for connect in connect_list:
    src, des = connect
    xs = (node_list[src][0], node_list[des][0])
    ys = (node_list[src][1], node_list[des][1])
    plt.gcf().gca().add_line(Line2D(xs, ys, linewidth=1, alpha=0.3))

  for circle in circle_list:
    plt.gcf().gca().add_artist(circle)

  # plt.axis('equal')
  plt.xlim(0, 11)
  plt.ylim(0, 11)
  plt.axis('off')
  plt.show()
  # plt.savefig('eaa/19_300_big.jpg')

def sim(steps):
  random.seed(0)
  # connect_map = np.array([[0, 0, 0, 1, 0, 0],
  #                         [0, 0, 0, 1, 0, 0],
  #                         [0, 0, 0, 0, 1, 0],
  #                         [0, 0, 0, 0, 0, 1],
  #                         [0, 0, 0, 0, 0, 1],
  #                         [0, 0, 0, 0, 0, 0]
  #                         ])

  connect_list = [(0, 2), (1, 2), (2, 4), (3, 4), (4, 18),
                  (5, 6), (6, 8), (7, 8), (8, 12), (9, 11),
                  (10, 11), (11, 12), (12, 18), (13, 16),
                  (14, 16), (15, 16), (16, 18), (17, 18)]

  map_shape = (19, 19)
  connect_map = np.zeros(map_shape)
  for connect in connect_list:
    connect_map[connect[0]][connect[1]] = 1

  print(connect_map)

  # utility_type = [1, 1, 1, 1, 1, 0]
  utility_type = [1] * 18 + [0]

  # esa = EAA(connect_map, utility_type,sink_node=5, V=100)
  # print(esa.paraAllocation())
  eaa = EAA(connect_map, utility_type, sink_node=18, V=100)
  eaa.run(steps)
  r_sum = eaa._sim_result.getSumR()
  print(r_sum)
  max_r = max(r_sum)
  r_p = []
  for r in r_sum:
    r_p.append(float(r) / max_r)

  print(r_p)
  return r_p

def dataThermo(steps, edge_len, V = 100):
  random.seed(0)

  thermo = ThermoMap(edge_len=edge_len)
  connect_map = thermo.getMap()
  print(connect_map)
  utility_type = thermo.getUtilityType()
  sink_node = thermo.getSinkNodeId()
  # print(connect_map[13][12])
  eaa = EAA(connect_map, utility_type, sink_node=sink_node, V=V)
  eaa.run(steps)

  r_sum = eaa._sim_result.getSumR()
  print(r_sum)
  max_r = max(r_sum)
  r_p = []
  for r in r_sum:
    r_p.append(float(r) / max_r)

  print(r_p)
  return r_p

def drawThermo(r_p, edge_len):
  thermo_data = np.zeros((edge_len, edge_len))
  for i in range(edge_len):
    for j in range(edge_len):
      ans = r_p[i * edge_len + j]
      thermo_data[i][j] = ans
  sns.heatmap(thermo_data, cmap='Reds')
  plt.show()
  # plt.savefig('eaa/13_13.jpg')


if __name__ == '__main__':
  # drawPic()
  # r_p = sim(300)
  # drawPicture(r_p)
  # drawMaxNet(r_p)
  e_len = 15
  r_p = dataThermo(1000, e_len, V = 100)
  drawThermo(r_p, e_len)